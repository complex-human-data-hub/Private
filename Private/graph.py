from __future__ import print_function
from __future__ import absolute_import

import copy
import multiprocessing
import reprlib
import sys
import time
from itertools import permutations, product

import numpy
import numpy.random
from collections import OrderedDict, deque
import logging
import networkx as nx
import graphviz as gv
import Private.s3_helper
from Private.builtins import builtins, prob_builtins, setBuiltinPrivacy, setGlobals, setUserIds, config_builtins, \
    illegal_variable_names, setGlobals2
from Private.graph_constants import pd_key, p_key, d_key, attr_label, attr_color, attr_is_prob, attr_contains, attr_id, \
    attr_last_ts, user_all, compute_key, sampler_key, manifold_key, completed_key, started_key, pt_private, pt_public, \
    pt_unknown, st_stale, st_uptodate, st_computing, st_exception

from Private.redis_reference import RedisReference
import Private.redis_helper as redis_helper
import shutil
import io
import re
import os
import base64
import pymc3 as pm
from dask.distributed import Client
from datetime import datetime
from ordered_set import OrderedSet
from .config import ppservers
import json
_log = logging.getLogger("Private")

numpy.set_printoptions(precision=3)
numpy.set_printoptions(threshold=2000)

privacy_criterion = 15.0   # percent
display_precision = 3


def debug_logger(msg):
    with open("/tmp/monday.log", "a") as fp:
        if not isinstance(msg, str):
            msg = json.dumps(msg, indent=4, default=str)
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        fp.write("[{}][{}] {}\n".format(timestamp, os.getpid(), msg))


def pp_set(s):
    """
    Pretty print a set.
    """
    s = list(s)
    s.sort()
    return " ".join(s)


class Graph:

    def __init__(self, events=None, project_id='proj1', shell_id=None, load_demo_events=True, user_ids=None):

        # variable types
        if not shell_id:
            shell_id = 'shell1'
        # clear the cache for the shell
        redis_helper.delete_user_keys(project_id, shell_id)

        self.deterministic = set()
        self.probabilistic = set()
        self.functions = set()
        self.builtins = set(builtins.keys()) | prob_builtins

        # dependencies

        self.dependson = {}  # deterministic dependencies
        self.probdependson = {}  # probabilistic dependencies

        # variables related to values
        if events and type(events) == RedisReference:
            events = events.value()
        self.project_id = project_id
        self.shell_id = shell_id
        self.load_demo_events = load_demo_events
        if user_ids:
            if 'All' not in user_ids:
                user_ids = ['All'] + user_ids
            self.user_ids = OrderedSet(user_ids)
            self.globals = setGlobals2(user_ids)
        else:
            self.globals = setGlobals(events=events, proj_id=self.project_id, shell_id=self.shell_id,
                                      load_demo_events=self.load_demo_events)
            self.user_ids = setUserIds(events=events)

        self.locals = {}  # do we need this?
        self.stale = dict([(u, set()) for u in self.user_ids])
        self.computing = dict([(u, set()) for u in self.user_ids])
        self.exception = dict([(u, set()) for u in self.user_ids])
        self.uptodate = dict([(u, set(builtins.keys()) or prob_builtins) for u in self.user_ids])
        self.samplerexception = dict([(u, {}) for u in self.user_ids])

        # variables related to privacy

        self.private = set()
        self.public = set()
        self.unknown_privacy = set()
        self.privacy_sampler_results = {}
        # the privacy samplers haven't been run since last compute and when they have been run

        # code associated with variables

        self.code = OrderedDict()  # private code for deterministic variables
        self.probcode = OrderedDict()  # private code of probabilistic variables
        self.evalcode = OrderedDict()  # python code for deterministic variables
        self.pyMC3code = OrderedDict()  # pyMC3 code for probabilistic variables
        self.hierarchical = {}  # what is the index variable of this hierarchical variable

        # comments

        self.comment = {}

        # auxiliary variables

        self.lock = multiprocessing.Lock()
        self.whohaslock = None
        self.jobs = {}
        self.log = logging.getLogger("Private")
        self.last_server_connect = 0
        self.server = None
        self.check_dask_connection()
        self.raw_graph = None
        self.i_graph = None
        self.p_graph = None
        self.init_raw_graph()

        # Keep the time stamps [job_type][user][id][last_completed/last_started]
        self.ts = {}
        self.init_ts()

        self.SamplerParameterUpdated = False

        setBuiltinPrivacy(self)  # set privacy of builtins

        if user_ids:
            self.define("Events", "", evalcode="getEvents(project_id, user_id)", dependson=["getEvents"])
            if self.load_demo_events:
                self.define("DemoEvents", "", evalcode="getDemoEvents(project_id, user_id)",
                            dependson=["getDemoEvents"])

    def __repr__(self):
        code_bits = []
        code_width = 50
        value_width = 80
        for name in self.code.keys():
            code_bits.append(name + " = " + str(self.code[name]))
        for name in self.probcode.keys():
            if name in self.hierarchical:
                code_bits.append(name + "[" + self.hierarchical[name] + "] ~ " + str(self.probcode[name]))
            else:
                code_bits.append(name + " ~ " + str(self.probcode[name]))
        if len(code_bits) > 0:
            m = max(len(line) for line in code_bits)
            m = min(m, code_width)
            newcodebits = [line[0:code_width].ljust(m, " ") for line in code_bits]
            value_bits = []
            for name in self.code.keys():
                value_bits.append(self.get_value(name)[0:value_width])
            for name in self.probcode.keys():
                if name in self.samplerexception:
                    value_bits.append(self.samplerexception[name])
                else:
                    value_bits.append(self.get_value(name)[0:value_width])
            comment_bits = []
            for name in self.code.keys():
                comment_bits.append(self.comment.get(name, ""))
            for name in self.probcode.keys():
                comment_bits.append(self.comment.get(name, ""))
            unsatisfied_depends = []
            for name in self.code.keys():
                unsatisfied_depends.append(
                    ", ".join(self.dependson[name] - (self.deterministic | self.probabilistic | self.builtins)))
            for name in self.probcode.keys():
                unsatisfied_depends.append(
                    ", ".join(self.probdependson[name] - (self.deterministic | self.probabilistic | self.builtins)))
            return "\n".join("  ".join([codebit, valuebit, commentbit, unsatisfied_depend]) for
                             codebit, valuebit, commentbit, unsatisfied_depend in
                             zip(newcodebits, value_bits, comment_bits, unsatisfied_depends))
        else:
            return ""

    def check_dask_connection(self):

        if self.server is None:
            self.server = Client(f'{Private.config.dask_scheduler_ip}:{Private.config.dask_scheduler_port}')

        return None

    def acquire(self, who):
        self.lock.acquire()
        self.whohaslock = who
        self.log.debug(who + " just got lock")

    def release(self):
        self.log.debug(self.whohaslock + " just released lock")
        self.whohaslock = None
        self.lock.release()

    def show_sets(self):
        result = ""
        result += "deterministic: " + pp_set(self.deterministic) + "\n"
        result += "probabilistic: " + pp_set(self.probabilistic) + "\n"
        result += "builtin: " + pp_set(self.builtins) + "\n"
        result += "\n"
        result += "uptodate: " + pp_set(self.uptodate["All"]) + "\n"
        result += "computing: " + pp_set(self.computing["All"]) + "\n"
        result += "exception: " + pp_set(self.exception["All"]) + "\n"
        result += "stale: " + pp_set(self.stale["All"]) + "\n"
        result += "\n"
        result += "private: " + pp_set(self.private) + "\n"
        result += "public: " + pp_set(self.public) + "\n"
        result += "unknown_privacy: " + pp_set(self.unknown_privacy) + "\n"
        result += "\n"
        result += "locals: " + pp_set(self.locals.keys()) + "\n"
        result += "globals: " + pp_set(self.globals["All"].keys()) + "\n"
        return result

    def show_globals(self):
        result = ""
        result += "All: " + str(self.globals["All"].get("r", "Not here")) + "\n"
        for user in self.user_ids:
            result += user + ": " + str(self.globals[user].get("r", "Not here")) + "\n"
        return result

    def show_jobs(self):
        """
        Returns a list of jobs currently running, divided into compute, sampler and manifold

        :return: String(list of jobs)
        """
        job_keys = self.jobs.keys()
        sampler_jobs = 0
        compute_jobs = 0
        manifold_jobs = 0

        sampler_vars = set()
        compute_vars = set()
        manifold_vars = set()

        for job_id in job_keys:
            job_type = job_id.split(" ")[0]
            job_var = job_id.split(" ")[-1]
            if job_type == 'Compute:':
                compute_jobs += 1
                compute_vars.add(job_var)
            elif job_type == 'Sampler:':
                sampler_jobs += 1
                sampler_vars.add(job_var)
            elif job_type == 'Manifold:':
                manifold_jobs += 1
                manifold_vars.add(job_var)
        result = f"Total jobs: {compute_jobs + sampler_jobs + manifold_jobs}\n" \
            f"Compute Jobs: {compute_jobs}\t{compute_vars if compute_vars else ''}\n" \
            f"Sampler Jobs: {sampler_jobs}\n" \
            f"Manifold Privacy Jobs: {manifold_jobs}\t{manifold_vars if manifold_vars else ''}"
        return result

    def eval_command_line_expression(self, code, user="All"):
        self.acquire("eval_command_line_expression")
        result = ""

        if code not in (self.deterministic | self.probabilistic | self.builtins):
            result += code + " is undefined  "
        elif code not in self.uptodate[user]:
            result += code + " is not uptodate  "
        elif code not in (self.public | self.unknown_privacy):
            result += code + " is private  "
        elif code not in self.public:
            result += code + " is of unknown privacy  "
        elif type(self.globals[user][code]) == RedisReference:
            result += code + " is too big to print  "
        else:
            val = self.globals[user][code]
            if type(val) == io.BytesIO:
                result = "data:image/png;base64, " + base64.b64encode(val.getvalue()).decode()
            else:
                result = str(val)
        self.release()
        return result

    def show_sampler_results(self):
        res = str(len(self.privacy_sampler_results)) + " results\n"
        for k in self.privacy_sampler_results.keys():
            res += k + ": " + self.get_privacy_sampler_result(k) + " " + str(
                len(self.privacy_sampler_results[k])) + "\n"
        return res

    def compute_privacy(self, node, lock=True):

        if lock:
            self.acquire("computePrivacy")

        # set all variables except builtins to unknown_privacy
        self.set_all_unknown(node)
        node_contains = [n for n in node[attr_contains] if not n.startswith(pd_key)]
        for name in node_contains:
            self.compute_graph_privacy(name)
        self.compute_probabilistic_privacy(node)
        for name in node_contains:
            self.compute_graph_privacy(name)
        if lock:
            self.release()

    def compute_graph_privacy(self, name):
        """
        Starting from the name, traverse the privacy graph

        :param name: String, name of the node. Note that privacy graph has raw nodes.
        """
        predecessors = [p for p in self.p_graph.predecessors(name) if not p.startswith(pd_key)]
        if all([self.get_privacy(parent) == pt_public for parent in predecessors]):
            new_privacy = pt_public
        elif any([self.get_privacy(parent) == pt_private for parent in predecessors]):
            new_privacy = pt_private
        else:
            new_privacy = pt_unknown
        self.set_privacy(name, new_privacy)

        successors = [s for s in self.p_graph.successors(name) if not s.startswith(pd_key)]
        for child in successors:
            self.compute_graph_privacy(child)

    def compute_probabilistic_privacy(self, i_node):
        """
        Check the privacy sampler results to see if we can fill in variables
        We don't want to overwrite the values calculated directly from the graph, so we do this if privacy unknown only
        :param i_node: node from inferential graph
        """
        for name in i_node[attr_contains]:
            if name in self.unknown_privacy:
                if name in self.privacy_sampler_results:
                    self.set_privacy(name, self.get_privacy_sampler_result(name))

    def change_state(self, user, node, new_state):
        for name in node[attr_contains]:
            self.log.debug("Change state of %s to %s for user %s." % (name, new_state, user))
            self.uptodate[user].discard(name)
            self.computing[user].discard(name)
            self.exception[user].discard(name)
            self.stale[user].discard(name)
            if new_state == st_uptodate:  # whenever a variable changes to be uptodate the privacy could have changed
                self.uptodate[user].add(name)
            elif new_state == st_computing:  # when a variable changes to be computing its privacy is unknown
                self.computing[user].add(name)
            elif new_state == st_exception:  # when a variable changes to be exception its privacy is unknown
                self.exception[user].add(name)
            elif new_state == st_stale:  # when a variable changes to be stale its privacy is unknown
                self.stale[user].add(name)
            else:
                raise Exception("Exception: " + "Unknown state %s in changeState" % new_state)

        # Set all to children to stale
        if new_state == st_stale:
                for child in self.i_graph.successors(node[attr_id]):
                    self.change_state(user, child, new_state)

    def set_all_unknown(self, node):
        # set all variables except builtins to unknown privacy
        for name in (set(node[attr_contains]) & (self.deterministic | self.probabilistic)):
            self.set_privacy(name, pt_unknown)

    def set_privacy(self, name, privacy):
        self.private.discard(name)
        self.public.discard(name)
        self.unknown_privacy.discard(name)

        if privacy == pt_private:
            self.private.add(name)
        elif privacy == pt_public:
            self.public.add(name)
        elif privacy == pt_unknown:
            self.unknown_privacy.add(name)
        else:
            self.log.error("Unexpected privacy type in setPrivacy: " + privacy)

    def get_privacy(self, name):
        if name in self.private:
            return pt_private
        elif name in self.public:
            return pt_public
        elif name in self.unknown_privacy:
            return pt_unknown
        else:
            self.log.error("Privacy value of %s is not set." % name)

    def add_comment(self, name, the_comment):
        self.comment[name] = the_comment

    def check_cyclic_dependencies(self, name, dependents):
        if dependents == set():
            return False
        elif name in dependents:
            return True
        else:
            for dependent in dependents:
                dependent_dependents = self.dependson.get(dependent, set()) | self.probdependson.get(dependent, set())
                if self.check_cyclic_dependencies(name, dependent_dependents):
                    return True

    def get_value(self, name, long_format=False):
        res = ""
        formatter_string = "%%.%sf" % display_precision
        if name in self.deterministic | self.probabilistic:
            if name in self.stale["All"]:
                res += "Stale"
            elif name in self.computing["All"]:
                res += "Computing"
            elif name in self.exception["All"]:
                res += "Exception: " + str(self.globals["All"][name])
            elif name in self.private:
                res += "Private"
            elif name in self.unknown_privacy:
                if name in self.uptodate["All"] and isinstance(self.globals['All'].get(name), str) and self.globals[
                 'All'].get(name) == "Not retained.":
                    res += "Not retained."
                else:
                    res += "Privacy Unknown"
            elif name in self.uptodate["All"]:
                if type(self.globals["All"][name]) == io.BytesIO:  # write image to file
                    res += "[PNG Image]"
                elif type(self.globals["All"][name]) == RedisReference:
                    res += self.globals["All"][name].display_value
                elif type(self.globals["All"][name]) == numpy.ndarray:
                    if long_format:
                        res += str(self.globals["All"][name])
                    else:
                        s = self.globals["All"][name].shape
                        res += "[" * len(s) + formatter_string % self.globals["All"][name].ravel()[
                            0] + " ... " + formatter_string % self.globals["All"][name].ravel()[-1] + "]" * len(s)
                elif type(self.globals["All"][name]) == float or type(self.globals["All"][name]) == numpy.float64:
                    res += str((formatter_string % self.globals["All"][name]))
                else:
                    if long_format:
                        res += json.dumps(self.globals["All"][name], indent=4)
                    else:
                        res += reprlib.repr(self.globals["All"][name])
            else:
                raise Exception("Exception: " + name + " is not stale, computing, exception or uptodate.")
        elif name in self.builtins:
            if name in self.public:
                if long_format:
                    res += str(self.globals["All"][name])
                else:
                    res += reprlib.repr(self.globals["All"][name])
            else:
                res += "Private"
        else:
            raise Exception("Exception: Unknown variable in getValue " + name)
        return res

    def show_values(self):
        valuewidth = 120
        valuebits = []
        for name in self.code.keys():
            valuebits.append(name + " = " + self.get_value(name)[0:valuewidth])
        for name in self.probcode.keys():
            if name in self.samplerexception:
                valuebits.append(name + " ~ " + self.samplerexception[name])
            else:
                valuebits.append(name + " ~ " + self.get_value(name)[0:valuewidth])
        return "\n".join(valuebits)

    def show_code(self):
        codebits = []
        for name in self.code.keys():
            if name in self.functions:
                codebits.append(self.evalcode[name].replace("\t", "    "))
            else:
                codebits.append(name + " = " + str(self.code[name]))
        for name in self.probcode.keys():
            if name in self.hierarchical:
                codebits.append(name + "[" + self.hierarchical[name] + "] ~ " + str(self.probcode[name]))
            else:
                codebits.append(name + " ~ " + str(self.probcode[name]))
        if len(codebits) > 0:
            commentbits = []
            for name in self.code.keys():
                commentbits.append(self.comment.get(name, ""))
            for name in self.probcode.keys():
                commentbits.append(self.comment.get(name, ""))
            return "\n".join("  ".join([codebit, commentbit]) for codebit, commentbit in zip(codebits, commentbits))
        else:
            return ""

    def show_eval_code(self):
        codebits = []
        for name in self.code.keys():
            codebits.append(name + " = " + str(self.evalcode[name]))
        for name in self.probcode.keys():
            codebits.append(name + " ~ " + str(self.pyMC3code[name]))
        if len(codebits) > 0:
            commentbits = []
            for name in self.code.keys():
                commentbits.append(self.comment.get(name, ""))
            for name in self.probcode.keys():
                commentbits.append(self.comment.get(name, ""))
            return "\n".join("  ".join([codebit, commentbit]) for codebit, commentbit in zip(codebits, commentbits))
        else:
            return ""

    def show_dependencies(self):
        res = ""
        for name in self.code.keys():
            res += name + " = "
            if name not in self.private:
                res += self.code[name][0:60]
            else:
                res += "Private"
            if name in self.dependson:
                if self.dependson[name] != set([]):
                    res += "    " + repr(list(self.dependson[name]))
            res += "\n"
        for name in self.probcode.keys():
            if name in self.hierarchical:
                res += name + "[" + self.hierarchical[name] + "] ~ "
            else:
                res += name + " ~ "
            if name not in self.private:
                res += self.probcode[name][0:60]
            else:
                res += "Private"
            if name in self.probdependson:
                if self.probdependson[name] != set([]):
                    res += "    " + repr(list(self.probdependson[name]))
            res += "\n"
        return res[0:-1]

    def topological_sort(self):
        order, enter, state = deque(), self.probabilistic | self.deterministic, {}
        enter = OrderedSet(sorted(list(enter)))
        gray, black = 0, 1

        def dfs(node):
            state[node] = gray
            for k in sorted(list(self.dependson.get(node, set()) | self.probdependson.get(node, set()))):
                sk = state.get(k, None)
                try:
                    if sk == gray:
                        raise ValueError("cycle")
                except Exception:
                    _log.debug("topological_sort GREY")
                    _log.debug(self.dependson.get(node))
                    _log.debug(self.probdependson.get(node))
                    raise ValueError("cycle 2")
                if sk == black:
                    continue
                enter.discard(k)
                dfs(k)
            order.appendleft(node)
            state[node] = black

        while enter:
            dfs(enter.pop())
        result = [name for name in order if name in self.probabilistic - self.deterministic]
        result.reverse()
        return result

    def get_privacy_sampler_result(self, name):
        public_count = 0
        for user in self.privacy_sampler_results[name]:
            if name in self.uptodate[user] and self.privacy_sampler_results[name][user] == 'private':
                return 'private'
            elif name in self.uptodate[user] and self.privacy_sampler_results[name][user] == 'public':
                public_count += 1
        if public_count == len(self.user_ids) - 1:
            return 'public'
        else:
            return 'unknown_privacy'

    def get_globals(self, names, user):
        user_globals = self.globals[user]
        job_globals = {'user_id': user, 'project_id': self.project_id}
        deps = set()
        for name in names:
            if name in self.dependson:
                deps = deps.union(self.dependson[name])
            if name in self.probdependson:
                deps = deps.union(self.probdependson[name])
        deps = self.get_all_required_dependents(deps)
        for key in user_globals.keys():
            if key in deps:
                if type(user_globals[key]) == RedisReference:
                    job_globals[key] = copy.copy(user_globals[key])
                else:
                    job_globals[key] = user_globals[key]
        return job_globals

    def get_all_required_dependents(self, names):
        to_visit = names
        final_set = set()
        while to_visit != set():
            new_additions = set()
            for vname in to_visit:
                final_set.add(vname)
                if vname in self.dependson and vname in self.functions:
                    new_additions = new_additions.union(self.dependson[vname])
                if vname in self.probdependson:
                    new_additions = new_additions.union(self.probdependson[vname])
            to_visit = to_visit.union(new_additions)
            to_visit = to_visit.difference(final_set)

        return final_set

    # Core functions
    def define(self, name, code, evalcode=None, dependson=None, prob=False, hier=None, pyMC3code=None):
        self.log.debug("Define {name}, {code}, {dependson}, {prob}, {pyMC3code}".format(**locals()))
        if name in prob_builtins | illegal_variable_names:
            raise Exception("Exception: Illegal Identifier '" + name + "' is a Private Built-in")
        self.acquire("define " + name)
        if not dependson:
            dependson = []
        else:
            if self.check_cyclic_dependencies(name, set(dependson)):
                self.release()
                raise Exception("Exception: Cyclic Dependency Found, " + name)

        if prob:
            self.probabilistic.add(name)
            self.probcode[name] = code
            self.pyMC3code[name] = pyMC3code
            if dependson:
                self.probdependson[name] = set(dependson)
            if hier:
                self.hierarchical[name] = hier
        else:
            self.deterministic.add(name)
            self.code[name] = code
            self.evalcode[name] = evalcode
            self.dependson[name] = set(dependson)
        if name not in {'Events', 'DemoEvents'}:
            self.add_to_inf_graph(name, dependson, hier, prob)
        node = self.get_node(name, prob)
        for user in self.user_ids:
            self.change_state(user, node, "stale")
        # set the timestamp for node define
        node[attr_last_ts] = int(time.time() * 1000)
        # need computePrivacy before compute so we don't compute public variables for each participant
        self.compute_privacy(node, lock=False)
        if name not in self.public:
            for user in self.user_ids:
                self.start_computation(user, node, lock=False)
        else:
            self.start_computation(user_all, node, lock=False)
        self.release()

        self.compute_privacy(node)  # every definition could change the privacy assignments

    def define_function(self, name, code, evalcode, dependson, defines, arguments):
        if name in prob_builtins | illegal_variable_names:
            raise Exception("Exception: Illegal Identifier '" + name + "' is a Private Built-in")
        self.acquire("define " + name)
        if not dependson:
            dependson = set()
        else:
            if self.check_cyclic_dependencies(name, dependson):
                self.release()
                raise Exception("Exception: Cyclic Dependency Found, " + name)
        self.deterministic.add(name)
        self.functions.add(name)
        self.code[name] = code
        self.evalcode[name] = evalcode
        self.dependson[name] = dependson.difference(defines).difference(arguments)
        self.add_to_inf_graph(name, dependson, {}, False)
        node = self.i_graph.nodes[name]
        for user in self.user_ids:
            self.change_state(user, node, "stale")
        # need computePrivacy before compute so we don't compute public variables for each participant
        self.compute_privacy(node, lock=False)
        if name not in self.public:
            for user in self.user_ids:
                self.start_computation(user, node, lock=False)
        else:
            self.start_computation(user_all, node, lock=False)
        self.release()
        self.compute_privacy(node)

    def delete(self, name):
        self.acquire("delete " + name)
        if name in self.probabilistic | self.deterministic:
            node = self.get_node(name, name in self.probabilistic)

            for user in self.user_ids:
                self.change_state(user, node, "stale")
                self.globals[user].pop(name, None)
                self.stale[user].discard(name)

            self.deterministic.discard(name)
            self.probabilistic.discard(name)
            self.private.discard(name)
            self.public.discard(name)
            self.unknown_privacy.discard(name)

            self.code.pop(name, None)
            self.probcode.pop(name, None)
            self.pyMC3code.pop(name, None)
            self.hierarchical.pop(name, None)

            self.dependson.pop(name, None)
            self.probdependson.pop(name, None)
            self.comment.pop(name, None)
            self.del_from_raw_graph(name)
            res = ""
        else:
            res = name + " not found."

        self.release()
        # self.compute_privacy(self.get_sub_graphs(name)) # every delete could change the privacy assignments
        return res

    def construct_pymc3_code(self, node, user=None):
        #try:
            locals = {}
            sub_graph = node[attr_contains] + list(self.i_graph.predecessors(node[attr_id]))
            loggingcode = """
try:
    logging = __import__("logging")
    logging.basicConfig(level=logging.DEBUG)
    _log = logging.getLogger("Private")
    #logging.disable(100)
    _log.debug("Running PyMC3 Code")
    json = __import__("json")
    def debug_logger(msg):
        if not isinstance(msg, str):
            msg = json.dumps(msg, indent=4, default=str)
        with open("/tmp/private-worker.log", "a") as fp:
            fp.write(msg + "\\n")

    debug_logger("Running PyMC3 Code")
"""

            code = loggingcode

            # extract index variables

            for index_variable in list(set(self.hierarchical.values()) & set(sub_graph)):
                code += "    global __%s_Dict \n" % index_variable
                code += "    __%s_Dict = dict((key, val) for val, key in enumerate(set(%s))) \n" % (
                 index_variable, index_variable)
                code += "    __%s_Indices = [__%s_Dict[__private_index__] for __private_index__ in %s]\n" % (
                 index_variable, index_variable, index_variable)
                if user:
                    locals[index_variable] = self.globals[user][index_variable]

            code += """
    exception_variable = "No Exception Variable"
    pymc3 = __import__("pymc3")
    dot = __import__("theano").tensor.tensordot
    softmax = __import__("theano").tensor.nnet.nnet.softmax
    traceback = __import__("traceback")

    numpy = __import__("numpy") 
    numpy.random.seed(987654321)
    basic_model = pymc3.Model()

    
    with basic_model:

"""

            # pyMC3 requires that these are ordered so that things that are dependent come later
            probabilistic_only_names = self.topological_sort()
            if sub_graph:
                probabilistic_only_names = [n for n in probabilistic_only_names if n in sub_graph]

            for name in probabilistic_only_names:
                code += '        exception_variable = "%s"\n' % name
                if name in self.hierarchical:
                    shape_code = ", shape = len(__%s_Dict)" % self.hierarchical[name]
                    code += "        " + self.pyMC3code[name] % shape_code + "\n"
                else:
                    code += "        " + self.pyMC3code[name] % ""+ "\n"

            observed_names = list(self.probabilistic & self.deterministic & set(sub_graph))
            for name in observed_names:
                code += '        exception_variable = "%s"\n' % name
                obs_name = "__private_%s_observed" % name
                code += "        " + self.pyMC3code[name] % (", observed=%s" % obs_name) + "\n"
                if user:
                    if name in self.globals[user]:
                        locals[obs_name] = self.globals[user][name]
                    else:
                        locals[obs_name] = self.globals["All"][name]
                else:
                    locals = None

            code += """
        __private_result__ = (pymc3.sample({NumberOfSamples}, tune={NumberOfTuningSamples}, chains={NumberOfChains}, random_seed=987654321, progressbar = False), "No Exception Variable", basic_model)
        _log.debug("Finished PyMC3 Code")
        with open("/tmp/private-worker.log", "a") as fp:
            fp.write("Finished PyMC3 Code\\n")

except Exception as e:
    try:
        # remove stuff after the : as that sometimes reveals private information
        _log.debug("PyMC3 Code Exception: " + str(e))
        with open("/tmp/private-worker.log", "a") as fp:
            fp.write("Error " + str(e) + "\\n")

        estring = e.args[0]
        newErrorString = estring[estring.rfind("\\n")+1:]
        # Need to create a new Exception here 
        # some exceptions were cpickle when pp passed the result back to the master
        return_exception = Exception(newErrorString)
        __private_result__ = (return_exception, exception_variable, None)
        with open("/tmp/private-worker.log", "a") as fp:
            fp.write(traceback.format_exc() + "\\n")
            fp.write("Finished processing Error \\n")
    except Exception as e2:
        with open("/tmp/private-worker.log", "a") as fp:
            fp.write("Error2 " + str(e2) + "\\n")
            fp.write(traceback.format_exc() + "\\n")
        __private_result__ = (e2, exception_variable, None)
        with open("/tmp/private-worker.log", "a") as fp:
            fp.write("Finished processing Error2 \\n")

        

""".format(NumberOfSamples=self.globals["All"]["NumberOfSamples"], NumberOfChains=self.globals["All"]["NumberOfChains"], NumberOfTuningSamples=self.globals["All"]["NumberOfTuningSamples"])

            return locals, code

    def start_computation(self, user, node, lock=True):
        """
        Start computation for the given node for the given user

        :param user: String
        :param node: Dict {'id': a, 'contains': [c, d], 'is_prob':False ...}
        :param lock: Boolean, if this method need to run in a lock
        :return:
        """
        node = copy.deepcopy(node)
        if lock:
            self.acquire("compute")
        n_id = node[attr_id]
        node_ts = node[attr_last_ts]
        if n_id.startswith(pd_key) or not self.is_node_computable(user, n_id):
            if lock:
                self.release()
            return
        else:
            job_globals = self.get_globals(node[attr_contains], user)
            self.change_state(user, node, "computing")
            if node[attr_is_prob]:
                success = self.reg_ts(sampler_key, user, n_id, started_key, node_ts)
                if success:
                    job_name = "Sampler:  " + user + ", " + str(node[attr_label])
                    job_locals, sampler_code = self.construct_pymc3_code(node, user)
                    self.reset_privacy_results(node, user)
                    self.jobs[job_name] = self.server.submit(sampler_job, job_name, user, node, sampler_code,
                                                             job_globals,
                                                             job_locals, resources={'process': 1})
                    self.jobs[job_name].add_done_callback(self.sampler_callback)
            else:
                success = self.reg_ts(compute_key, user, n_id, started_key, node_ts)
                if success:
                    job_name = "Compute:  " + user + " " + n_id
                    user_func = [self.evalcode[func_name] for func_name in self.functions]
                    self.jobs[job_name] = self.server.submit(job, job_name, node, user, self.evalcode[n_id],
                                                             job_globals,
                                                             self.locals, user_func, self.project_id, self.shell_id)
                    self.jobs[job_name].add_done_callback(self.callback)
        if lock:
            self.release()

    def start_mp_job(self, user, node):
        names = node[attr_contains]
        node_ts = node[attr_last_ts]
        for name in names:
            if self.get_privacy_sampler_result(name) != 'private' and not (
                    isinstance(self.globals[user].get(name), str) and self.globals[user].get(name) == "Not retained."):
                # Some variables (e.g., logs of SDs) are returned from the sampler, but are not variables in our code.
                if name in self.globals[user].keys() and name in self.globals["All"].keys():
                    # if shape is affected by dropping a user then this variable is private
                    if self.globals[user][name].shape != self.globals["All"][name].shape:
                        self.privacy_sampler_results[name][user] = 'private'
                    else:
                        success = self.reg_ts(manifold_key, user, name, started_key, node_ts)
                        if success:
                            jobname = "Manifold: " + user + " " + name
                            self.jobs[jobname] = self.server.submit(mp_job, jobname, node, name, user,
                                                                    self.globals[user][name],
                                                                    self.globals["All"][name])
                            self.jobs[jobname].add_done_callback(self.mp_callback)

    def callback(self, return_value):
        return_value = return_value.result()
        self.acquire("callback")
        debug_logger("In callback")
        job_name, node, user, value = return_value
        name = node[attr_id]
        node_ts = node[attr_last_ts]
        try:
            if isinstance(value, Exception):
                if user == "All":
                    debug_logger(["callback Exception", user, name, value])
                    self.globals[user][name] = str(value)
                    self.change_state(user, node, "exception")
            elif self.ts[compute_key][user][name][started_key] == node_ts:
                original_value = self.globals[user].get(name, '')
                self.globals[user][name] = value
                self.change_state(user, node, "uptodate")
                self.reg_ts(compute_key, user, name, completed_key, node_ts)
                if user == "All":
                    if name in config_builtins:
                        builtins.get(name)(value)
                    if name in ["NumberOfSamples", "NumberOfChains", "NumberOfTuningSamples"]:
                        if name == "NumberOfSamples":
                            if value > 4000:
                                self.comment[name] = "# Maximum Number of Samples is 4000"
                                self.globals[user][name] = original_value
                        self.SamplerParameterUpdated = True
                    if type(value) == io.BytesIO:  # write image to file
                        value.seek(0)
                        with open(name + '.png', 'wb') as f:
                            shutil.copyfileobj(value, f)
            if job_name in self.jobs:
                del self.jobs[job_name]
            else:
                self.log.debug("Trying to delete job %s that is not in self.jobs" % job_name)
                self.log.debug(self.jobs)
        except Exception as e:
            self.log.debug(str(e))

        self.release()
        self.compute_privacy(node)
        for u in self.i_graph.successors(name):
            successor = self.i_graph.nodes[u]
            successor[attr_last_ts] = node_ts
            self.start_computation(user, successor)
        self.compute_privacy(node)

    def sampler_callback(self, return_value):
        return_value = return_value.result()
        self.acquire("sampler_callback")
        job_name, user, node, value, exception_variable, stats = Private.s3_helper.read_results_s3(
            return_value) if Private.config.s3_integration else return_value
        names = node[attr_contains]
        n_id = node[attr_id]
        node_ts = node[attr_last_ts]
        if isinstance(value, Exception):
            self.log.debug("Exception in sampler callback %s %s" % (user, str(value)))
            for name in names:
                # ** Might need to remove the Exception message here
                self.globals[user][name] = str(value)
                debug_logger(["sampler_callback Exception", user, name, value])
            self.change_state(user, node, "exception")
            if exception_variable != "No Exception Variable":
                m = re.match(r"__init__\(\) takes at least (\d+) arguments \(\d+ given\)", str(value))
                if m:
                    value = str(int(m.group(1)) - 1) + " arguments required."
                self.samplerexception[user][exception_variable] = str(value)
            else:
                for name in names:
                    self.samplerexception[user][name] = str(value)
            self.log.debug("Exception in sampler callback %s %s ...done" % (user, str(value)))
        elif self.ts[sampler_key][user][n_id][started_key] == node_ts:  # successful sampler return
            try:
                self.log.debug("sampler_callback: name in names ")
                for name in names:
                    if name in value.varnames:
                        name_long = int("".join(map(str, [ord(c) for c in name])))
                        # 4294967291 seems to be the largest prime under 2**32 (int limit)
                        seed = name_long % 4294967291
                        debug_logger("name_seed {}: {} ({})".format(name, seed, name_long))
                        numpy.random.seed(seed)
                        self.globals[user][name] = numpy.random.permutation(
                            value[name])  # permute to break the joint information across variables
                    else:  # manifold privacy is applied to individual variables
                        # so there could be more information in the joint information
                        self.globals[user][name] = "Not retained."
                self.change_state(user, node, "uptodate")

                self.log.debug("sampler_callback: name in names ...done ")
                self.reg_ts(sampler_key, user, n_id, completed_key, node_ts)

                complete_users = [u for u in self.user_ids if u != "All" and set(names).issubset(self.uptodate[u])]

                # if this is All then initiate comparisons with all of the users that have already returned
                if user == "All":
                    if stats:
                        for stat_key in stats["rhat"]:
                            self.globals[user]['rhat'][stat_key] = numpy.array(stats["rhat"][stat_key]).tolist()
                            self.globals[user]['ess'][stat_key] = numpy.array(stats["ess"][stat_key]).tolist()
                            self.globals[user]['waic'][stat_key] = stats["waic"]
                            self.globals[user]['loo'][stat_key] = stats["loo"]
                    for u in complete_users:
                        self.start_mp_job(u, node)

                else:  # else compare All to this users samples using manifold privacy calculation
                    self.log.debug("sampler_callback: complete_users - Users ")
                    if set(names).issubset(self.uptodate[user_all]):
                        self.start_mp_job(user, node)
            except Exception as e:
                self.log.debug("in samplercallback when assigning values " + str(e))

        self.log.debug("sampler_callback: delete jobs ")

        try:
            del self.jobs[job_name]
        except Exception as e:
            self.log.debug("trying to del job " + str(e))

        self.log.debug("sampler_callback: delete jobs ...done")

        self.release()
        self.compute_privacy(node)
        for u in self.i_graph.successors(node[attr_id]):
            self.start_computation(user, self.i_graph.nodes[u])
        self.compute_privacy(node)

    def mp_callback(self, return_value):
        return_value = return_value.result()
        sample_size = self.globals['All']['NumberOfSamples'] * self.globals['All']['NumberOfChains']
        step_size = max(int(sample_size / Private.config.max_sample_size), 1)
        self.acquire("mp_callback")
        job_name, node, name, user, d = return_value
        node_ts = node[attr_last_ts]
        print('at mp callback ', name, user, node_ts)
        if self.ts[manifold_key][user][node[attr_id]][started_key] == node_ts:
            try:
                self.log.debug(
                    "mp_callback: " + user + ": " + name + ": " + str(d) + " " + str(d < privacy_criterion))
                if self.get_privacy_sampler_result(name) != 'private':
                    if d > privacy_criterion:
                        self.privacy_sampler_results[name][user] = "private"

                        self.globals['All'][name] = self.globals['All'][name][::step_size][
                                                    :Private.config.max_sample_size]
                        self.log.debug("mp_callback: " + user + ": " + name + ": " + str(d) + " " + str(
                            d < privacy_criterion) + ": PRIVATE")
                    else:
                        self.log.debug("manifoldprivacycallback: " + user + ": " + name + ": " + str(d) + " " + str(
                            d < privacy_criterion) + ": UNKNOWN_PRIVACY")
                        self.privacy_sampler_results[name][user] = "public"

                if self.get_privacy_sampler_result(name) == 'public':
                    self.globals['All'][name] = self.globals['All'][name][::step_size][:Private.config.max_sample_size]
                    self.log.debug("manifoldprivacycallback: " + user + ": " + name + ": PUBLIC")
                self.reg_ts(manifold_key, user, name, completed_key, node_ts)

            except Exception as e:
                self.log.debug("manifold privacy " + str(e))

        try:
            del self.jobs[job_name]
        except Exception as e:
            self.log.debug("trying to del job " + str(e))
        self.release()
        self.compute_privacy(node)

    # New graph methods

    def init_raw_graph(self):
        """
        This method initializes the inferential graph.
        Creates empty arrays (graph attributes) to hold the deterministic nodes and the probabilistic nodes
        """
        self.raw_graph = nx.DiGraph()
        self.raw_graph.graph[d_key] = []
        self.raw_graph.graph[p_key] = []

    def add_to_inf_graph(self, name, linked_nodes, h_node, is_prob):
        """
        Adds a node to the inferential graph (i_graph)
        :param name: String, Node name
        :param linked_nodes: Array of Strings, Other linked nodes (depends_on)
        :param h_node: String, hierarchical nodes, if any
        :param is_prob: Boolean, if it's a probabilistic node
        :return:
        """

        # Add a new node. It get automatically added, when adding a edge but we need to set the id
        if name not in self.raw_graph.nodes:
            self.raw_graph_add_node(name, is_prob)
        else:
            # identifying probabilistic and deterministic nodes
            if is_prob and name in self.raw_graph.graph[d_key]:
                linked_nodes.append(name)
                name = pd_key + name
                self.raw_graph_add_node(name, is_prob)
            elif (not is_prob) and name in self.raw_graph.graph[p_key]:
                nx.relabel_nodes(self.raw_graph, {name: pd_key + name}, copy=False)
                self.raw_graph_add_node(pd_key + name, True)
                self.raw_graph.graph[p_key].remove(name)
                self.raw_graph.graph[p_key].append(pd_key + name)
                self.raw_graph_add_node(name, is_prob)
                self.raw_graph.add_edge(name, pd_key + name)

        # Add the linked nodes as well
        for node in linked_nodes:
            if node not in self.raw_graph.nodes:
                self.raw_graph_add_node(node, False)

        # Adding the edges
        if is_prob:
            self.raw_graph.graph[p_key].append(name)
            edges = [(a, name) for a in set(linked_nodes)]
            self.raw_graph.add_edges_from(edges)
        else:
            self.raw_graph.graph[d_key].append(name)
            edges = [(a, name) for a in set(linked_nodes) - {h_node}]
            self.raw_graph.add_edges_from(edges)

        # update i_graph and p_graph
        self.i_graph = self.modified_inferential_graph()
        self.p_graph = self.modified_privacy_graph()

    def raw_graph_add_node(self, name, is_prob):
        """
        Adds a node to the raw graph and defined all its properties

        :param name: String, variable name
        :param is_prob: Boolean, is probabilistic
        """
        if name not in self.raw_graph.nodes:
            self.raw_graph.add_node(name)
        self.raw_graph.nodes[name][attr_label] = name
        self.raw_graph.nodes[name][attr_contains] = [name]
        self.raw_graph.nodes[name][attr_is_prob] = is_prob
        self.raw_graph.nodes[name][attr_id] = name
        self.raw_graph.nodes[name][attr_last_ts] = 0

    def del_from_raw_graph(self, name):
        """
        Delete a node from the inferential graph (i_graph), **Yet to implement
        :param name: String, name of the node
        """
        self.raw_graph.remove_node(name)

        # update i_graph and p_graph
        self.i_graph = self.modified_inferential_graph()
        self.p_graph = self.modified_privacy_graph()

        return name

    def modified_inferential_graph(self):
        """
        Original raw_graph keeps the nodes in more ground level with more information.
        We are getting a abstract representation by modifying it.

        :return: networkX graph
        """
        # Generating modified inferential graph
        i_graph = copy.deepcopy(self.raw_graph)
        p_nodes = self.raw_graph.graph[p_key]
        if len(p_nodes) > 1:
            edge_permutations = set(permutations(p_nodes, 2))
            edges_to_remove = edge_permutations.intersection(set(i_graph.edges))
            while edges_to_remove:
                e = edges_to_remove.pop()
                node_0 = i_graph.nodes[e[0]][attr_label]
                node_1 = i_graph.nodes[e[1]][attr_label]
                node_0_graph = i_graph.nodes[e[0]][attr_contains]
                node_1_graph = i_graph.nodes[e[1]][attr_contains]
                sub_graph = []
                if node_0.startswith(pd_key):
                    node_label = node_1
                    sub_graph.extend(node_1_graph)
                elif node_1.startswith(pd_key):
                    node_label = node_0
                    sub_graph.extend(node_0_graph)
                else:
                    node_label = node_0 + ', ' + node_1
                    sub_graph.extend(node_0_graph)
                    sub_graph.extend(node_1_graph)

                i_graph = nx.contracted_edge(i_graph, e, self_loops=False)
                i_graph.nodes[e[0]][attr_label] = node_label
                i_graph.nodes[e[0]][attr_color] = 'red'
                i_graph.nodes[e[0]][attr_is_prob] = True
                i_graph.nodes[e[0]][attr_contains] = sub_graph

                edges_to_remove = edge_permutations.intersection(set(i_graph.edges))

        return i_graph

    def modified_privacy_graph(self):
        """
        Original raw_graph keeps the nodes in more ground level with more information.
        We are getting a privacy by modifying it.

        :return: networkX graph
        """
        # Generating modified privacy graph
        p_graph = copy.deepcopy(self.raw_graph)
        p_nodes = self.raw_graph.graph[p_key]
        pd_nodes = []
        for p_node in p_nodes:
            if p_node.startswith(pd_key):
                pd_nodes.append(p_node)
        if len(pd_nodes) > 0:
            edge_permutations = set(product((set(p_nodes) - set(pd_nodes)), pd_nodes))
            # These are the edges between pd_nodes and p_nodes
            edges_to_remove = edge_permutations.intersection(set(p_graph.edges))
            # We add the dependencies of each pd_nodes to adjacent p_nodes
            for e in edges_to_remove:
                # get in edges to the pd_node
                pd_in_edges = set(p_graph.in_edges(e[1]))
                pd_in_edges = pd_in_edges.difference(edges_to_remove)
                for pd_in_edge in pd_in_edges:
                    p_graph.add_edge(pd_in_edge[0], e[0])
            # Finally remove the pd_nodes
            for pd_node in pd_nodes:
                p_graph.remove_node(pd_node)

        return p_graph

    def reset_privacy_results(self, node, user):
        for name in node[attr_contains]:
            if name in self.privacy_sampler_results and user != user_all:
                self.privacy_sampler_results[name][user] = 'unknown_privacy'
            else:
                self.privacy_sampler_results[name] = {}

    def init_ts(self):
        for job_type in [compute_key, sampler_key, manifold_key]:
            self.ts[job_type] = {}
            for user in self.user_ids:
                self.ts[job_type][user] = {}

    def reg_ts(self, job_key, user, n_id, ts_key, ts):
        if n_id not in self.ts[job_key][user]:
            self.ts[job_key][user][n_id] = {}
        current_ts = self.ts[job_key][user][n_id].get(ts_key, 0)
        if current_ts < ts:
            self.ts[job_key][user][n_id][ts_key] = ts
            return True
        else:
            return False

    def is_node_computable(self, user, n_id):
        """
        Given the node check if the node is computable based on the inferential graph
        :param user: String
        :param n_id: String, node name (as in graph)
        :return: Boolean
        """
        is_computable = True
        for u in self.i_graph.predecessors(n_id):
            if (u not in self.builtins) and (u not in self.uptodate[user]):
                is_computable = False
                break
        return is_computable

    def get_node(self, var_name, prob):
        """
        Return the node id related to the variable name in the inferential graph
        :param var_name: String, variable name
        :param prob: Boolean, is probabilistic
        :return: (node id, node data)
        """
        # if deterministic, node id is same as the variable name
        if not prob:
            return self.i_graph.nodes[var_name]
        for n, ip in self.i_graph.nodes(data=attr_is_prob):
            if ip and (var_name in self.i_graph.nodes[n][attr_contains] or
                       pd_key + var_name in self.i_graph.nodes[n][attr_contains]):
                return self.i_graph.nodes[n]
        return None

    def draw_inferential_graph(self, graph_name='inferential_graph'):
        """
        Draws the modified inferential graph

        :return: graph as a base 64 string
        """
        nx.drawing.nx_pydot.write_dot(self.i_graph, graph_name)
        gv.render('dot', 'png', graph_name)
        result = "data:image/png;base64, " + base64.b64encode(open(f"{graph_name}.png", "rb").read()).decode()
        return result

    def draw_privacy_graph(self, graph_name='privacy_graph'):
        """
        Draws the modified privacy graph

        :return: graph as a base 64 string
        """
        p_graph = self.modified_privacy_graph()
        nx.drawing.nx_pydot.write_dot(p_graph, graph_name)
        gv.render('dot', 'png', graph_name)
        result = "data:image/png;base64, " + base64.b64encode(open(f"{graph_name}.png", "rb").read()).decode()
        return result

    def draw_generative_graph(self, graph_name='generative_graph'):
        g_graph = nx.DiGraph()
        visited, stack = set(), list(self.probabilistic | self.deterministic)
        while stack:
            vertex = stack.pop()
            g_graph.add_node(vertex)
            if vertex not in visited:
                visited.add(vertex)
                for k in self.dependson.get(vertex, set()) | self.probdependson.get(vertex, set()):
                    g_graph.add_edge(vertex, k)
                    stack.append(k)
        nx.drawing.nx_pydot.write_dot(g_graph, graph_name)
        gv.render('dot', 'png', graph_name)
        result = "data:image/png;base64, " + base64.b64encode(open(f"{graph_name}.png", "rb").read()).decode()
        return result
        # pos = nx.spring_layout(g_graph, scale=2)
        # nx.draw_networkx(g_graph, pos, node_color='cornflowerblue', node_size=100, with_labels=False)
        # if len(pos) > 1:
        #     for p in pos:  # raise text positions
        #         pos[p][1] += 0.15
        # nx.draw_networkx_labels(g_graph, pos, font_size=10)
        # buf = io.BytesIO()
        # plt.savefig(buf, format="png")
        # result = "data:image/png;base64, " + base64.b64encode(buf.getvalue()).decode()
        # plt.savefig('generative_graph.png')
        # plt.clf()
        # plt.close()
        # return result


def job(job_name, node, user, code, globals, locals, user_func, project_id, shell_id):
    name = node[attr_id]
    redis_key = redis_helper.get_redis_key(user, name, project_id, shell_id)
    name_long = int("".join(map(str, [ord(c) for c in name])))
    # 4294967291 seems to be the largest prime under 2**32 (int limit)
    seed = name_long % 4294967291
    numpy.random.seed(seed)
    s3_var_globals = retrieve_s3_vars(globals)
    for func in user_func:
        try:
            exec(func, s3_var_globals)
        except Exception as e:
            e = Exception("Error in User Function: " + func[4:10] + "...")
            return job_name, name, user, e
    try:
        if code.startswith("def"):
            value = "User Function"
        else:
            value = eval(code, s3_var_globals, locals)
        if get_size(value) > 1e6:
            # if True:
            value = RedisReference(redis_key, value)

        return job_name, node, user, value
    except Exception as e:
        return job_name, node, user, e


def sampler_job(job_name, user, node, code, globals, locals):
    numpy.random.seed(Private.config.numpy_seed)
    try:
        s3vars = retrieve_s3_vars(globals)
        exec(code, s3vars, locals)
        value, exception_variable, model = locals["__private_result__"]
        stats = None
        if user == "All":  # if this is All then initiate comparisons with all of the users that have already returned
            stats = {}
            # For loop is here to make sure failure of one computation doesn't impact the other.
            # Exceptions are handled for all at once
            for stat_name in ["rhat", "ess", "waic", "loo"]:
                try:
                    if stat_name == "rhat":
                        stats[stat_name] = pm.stats.rhat(value)
                    elif stat_name == "ess":
                        stats[stat_name] = pm.stats.ess(value)
                    elif stat_name == "waic":
                        stats[stat_name] = pm.stats.waic(value, model)
                    elif stat_name == "loo":
                        stats[stat_name] = pm.stats.loo(value, model)
                except Exception as e:
                    stats[stat_name] = "Exception: " + str(e)
        data = (job_name, user, node, value, exception_variable, stats)
        return data
    except Exception as e:
        return job_name, user, node, e, "No Exception Variable", None


def mp_job(job_name, node, name, user, first_array, second_array):
    from Private.manifoldprivacy import distManifold
    debug_logger("mp_job : {} [{}] Shape user: {} \nall {}".format(name, user, first_array.shape,
                                                                   second_array.shape))
    debug_logger(
        "mp_job : {} [{}] Sum user: {} \nall {}".format(name, user, first_array.sum(), second_array.sum()))

    d = distManifold(first_array, second_array) * 100.
    return job_name, node, name, user, d


def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size


def retrieve_s3_vars(var_dict):
    ret_dict = {}
    for key in var_dict.keys():
        if type(var_dict[key]) == RedisReference:
            ret_dict[key] = var_dict[key].value()
        else:
            ret_dict[key] = var_dict[key]

    return ret_dict
