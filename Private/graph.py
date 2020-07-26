from __future__ import print_function
from __future__ import absolute_import

import copy
import hashlib
import multiprocessing
import reprlib
import sys
import time
from itertools import permutations, product

import numpy
import numpy.random
from collections import OrderedDict, deque
import logging
import matplotlib.pyplot as plt
import networkx as nx
import graphviz as gv
import Private.s3_helper
from Private.builtins import builtins, prob_builtins, setBuiltinPrivacy, setGlobals, setUserIds, config_builtins, illegal_variable_names, data_builtins, setGlobals2
#from Private.s3_reference import S3Reference
from Private.redis_reference import RedisReference
import Private.redis_helper as redis_helper
import shutil
import io
import re
import traceback
import pprint
import dill as pickle
import os
import base64
import uuid
import pymc3 as pm
from dask.distributed import Client
from datetime import datetime
from ordered_set import OrderedSet
from .config import ppservers, logfile, remote_socket_timeout, local_socket_timeout, numpy_seed, tcp_keepalive_time
import json
#logging.basicConfig(filename=logfile,level=logging.DEBUG)
_log = logging.getLogger("Private")

numpy.set_printoptions(precision=3)
numpy.set_printoptions(threshold=2000)

PrivacyCriterion = 15.0   # percent
display_precision = 3

# inferential dependency graph keys
pd_key = 'p_'
p_key = 'p'
d_key = 'd'
attr_label = 'label'
attr_color = 'color'
attr_is_prob = 'is_prob'
attr_contains = 'sub_graph'
attr_id = 'id'
attr_last_ts = 'last_ts'

# other constants
user_all = 'All'

# time stamp constants
compute_key = 'compute_job'
sampler_key = 'sampler_job'
manifold_key = 'manifold_privacy_job'
completed_key = 'last_completed'
started_key = 'last_started'


def debug_logger(msg):
    with open("/tmp/monday.log", "a") as fp:
        if not isinstance(msg, str):
            msg = json.dumps(msg, indent=4, default=str)
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        fp.write("[{}][{}] {}\n".format(timestamp, os.getpid(), msg ))


def ppset(s):
    """
    Pretty print a set.
    """
    s = list(s)
    s.sort()
    return " ".join(s)


class graph:

    def __init__(self, events=None, project_id='proj1', shell_id=None, load_demo_events=True, user_ids=None):

        # variable types
        if not shell_id:
            shell_id='shell1'
        # clear the cache for the shell
        redis_helper.delete_user_keys(project_id, shell_id)

        self.deterministic = set()
        self.probabilistic = set()
        self.functions = set()
        self.builtins = set(builtins.keys()) | prob_builtins

        # dependencies

        self.dependson = {} # deterministic dependencies
        self.probdependson = {} # probabilistic dependencies

        # variables related to values
        if events and type(events) == RedisReference:
            events = events.value()
        self.project_id = project_id
        self.shell_id = shell_id
        self.load_demo_events = load_demo_events
        if user_ids:
            if not 'All' in user_ids:
                user_ids = ['All'] + user_ids
            self.userids = OrderedSet(user_ids)
            self.globals = setGlobals2(user_ids)
        else:
            self.globals = setGlobals(events=events, proj_id=self.project_id, shell_id=self.shell_id, load_demo_events=self.load_demo_events)
            self.userids = setUserIds(events=events)

        self.locals = {}   # do we need this?
        self.stale = dict([(u, set() ) for u in self.userids])
        self.computing = dict([(u, set() ) for u in self.userids])
        self.exception = dict([(u, set() ) for u in self.userids])
        self.uptodate = dict([(u, set(builtins.keys()) or prob_builtins) for u in self.userids])
        self.samplerexception = dict([(u, {}) for u in self.userids])

        # variables related to privacy

        self.private = set()
        self.public = set()
        self.unknown_privacy = set()
        self.privacy_sampler_results = {} # this holds results from privacy samplers so we know the difference between when
                                        # the privacy samplers haven't been run since last compute and when they have been run

        # code associated with variables

        self.code = OrderedDict()   # private code for deterministic variables
        self.probcode = OrderedDict() # private code of probabilistic variables
        self.evalcode = OrderedDict() # python code for determinitisitc variables
        self.pyMC3code = OrderedDict() # pyMC3 code for probabilistic variables
        self.hierarchical = {} # what is the index variable of this hierarchical variable

        # comments

        self.comment = {}

        # auxiliary variables

        self.lock = multiprocessing.Lock()
        self.whohaslock = None
        self.prettyprinter = pprint.PrettyPrinter()
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

        setBuiltinPrivacy(self) # set privacy of builtins

        if user_ids:
            self.define("Events", "", evalcode="getEvents(project_id, user_id)", dependson=["getEvents"])
            if self.load_demo_events:
                self.define("DemoEvents", "", evalcode="getDemoEvents(project_id, user_id)", dependson=["getDemoEvents"])

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
        result += "deterministic: "+ ppset(self.deterministic) + "\n"
        result += "probabilistic: "+ ppset(self.probabilistic) + "\n"
        result += "builtin: "+ ppset(self.builtins) + "\n"
        result += "\n"
        result += "uptodate: "+ ppset(self.uptodate["All"]) + "\n"
        result += "computing: "+ ppset(self.computing["All"]) + "\n"
        result += "exception: "+ ppset(self.exception["All"]) + "\n"
        result += "stale: "+ ppset(self.stale["All"]) + "\n"
        result += "\n"
        result += "private: "+ ppset(self.private) + "\n"
        result += "public: "+ ppset(self.public) + "\n"
        result += "unknown_privacy: "+ ppset(self.unknown_privacy) + "\n"
        result += "\n"
        result += "locals: "+ ppset(self.locals.keys()) + "\n"
        result += "globals: "+ ppset(self.globals["All"].keys()) + "\n"
        return result

    def showGlobals(self):
        result = ""
        result += "All: "+ str(self.globals["All"].get("r", "Not here")) + "\n"
        for user in self.userids:
            result += user + ": "+ str(self.globals[user].get("r", "Not here")) + "\n"
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

    def checkPickling(self):
        for key, value in self.globals["All"].items():
            try:
                f = open(os.devnull, "w")
                pickle.dump(value, f)
            except:
                print("Pickle error with: ", key)

    def showPrivacy(self):
        res = "Private: " + " ".join(self.private - self.builtins) + " Public: " + " ".join(self.public - self.builtins) + " Unknown: " + " ".join(self.unknown_privacy - self.builtins)
        return res

    def showSamplerResults(self):
        res = str(len(self.privacy_sampler_results)) + " results\n"
        for k in self.privacy_sampler_results.keys() & self.probabilistic:
            res += k + ": " + self.get_privacy_sampler_result(k) + " " + str(len(self.privacy_sampler_results[k])) + "\n"
        return res

    def checkPrivacyUp(self, name):
        if name not in self.unknown_privacy:
            return self.getPrivacy(name) == "public"
        else:
            probParents = self.probabilisticParents(name)
            if len(probParents) == 0:
                return False
            else:
                return all(self.checkPrivacyUp(parent) for parent in probParents)

    def checkPrivacyDown(self, name):
        if name not in self.unknown_privacy:
            return self.getPrivacy(name) == "public"
        else:
            probChildren = self.probabilisticChildren(name)
            if len(probChildren) == 0:
                return False
            else:
                return all(self.checkPrivacyDown(child) for child in probChildren)

    def compute_privacy(self, node, lock=True):

        if lock:
            self.acquire("computePrivacy")

        # set all variables except builtins to unknown_privacy
        self.set_all_unknown(node)

        self.compute_graph_privacy()
        self.computeProbabilisticPrivacy(node)
        self.compute_graph_privacy()
        if lock:
            self.release()

    def compute_graph_privacy(self):

        something_changed = True

        while something_changed:

            something_changed = False

            #tmpUnknownPrivacy = self.unknown_privacy.copy()

            for name in self.deterministic | self.probabilistic:
                #self.log.debug("Considering " + name)

                oldPrivacy = self.getPrivacy(name)

                # if determinisitic children are all public set to public

                if name in self.deterministic:
                    if all(child in self.public for child in self.deterministicChildren(name)):
                        self.setPrivacy(name, "public")

                # if name has a private deterministic child set to private

                if any(child in self.private for child in self.deterministicChildren(name)):
                    self.setPrivacy(name, "private")

                # check probabilistic variables to see if they are public because the variables above and below them are public

                if name in self.probabilistic - self.deterministic:
                    if self.checkPrivacyUp(name) and self.checkPrivacyDown(name):
                        self.setPrivacy(name, "public")

                # determine if privacy changed

                if self.getPrivacy(name) != oldPrivacy:
                    something_changed = True
                    #self.log.debug("Something changed")
                else:
                    #self.log.debug("Nothing changed")
                    pass

    def computeProbabilisticPrivacy(self, node):

        # check the privacySamplerResults to see if we can fill in variables
        # only do this if we don't know the privacy already as we don't want to overwrite the values calculated directly from the graph
        node_ts = node[attr_last_ts]
        for name in self.deterministic | self.probabilistic:
            if name in self.unknown_privacy:
                #self.log.debug( "looking at privacySamplerResults: " + name)
                #self.log.debug( "unknown: " + str(self.unknown_privacy))
                if name in self.privacy_sampler_results:
                    self.setPrivacy(name, self.get_privacy_sampler_result(name))

    def changeState(self, user, name, newstate):
        self.log.debug("Change state of %s to %s for user %s." % (name, newstate, user))
        self.uptodate[user].discard(name)
        self.computing[user].discard(name)
        self.exception[user].discard(name)
        self.stale[user].discard(name)
        if newstate == "uptodate":   # whenever a variable changes to be uptodate the privacy could have changed
            self.uptodate[user].add(name)
        elif newstate == "computing": # when a variable changes to be computing its privacy is unknown
            self.computing[user].add(name)
        elif newstate == "exception": # when a variable changes to be exception its privacy is unknown
            self.exception[user].add(name)
        elif newstate == "stale": # when a variable changes to be stale its privacy is unknown
            self.stale[user].add(name)
            # check dependencies to see if other variables need to be made stale
            #print name, self.deterministicParents(name)
            for parent in self.deterministicParents(name): # parents via deterministic links
                # print name, " det ", self.deterministicParents(name)
                if parent not in self.stale[user]:
                    self.changeState(user, parent, "stale")
            for child in self.probabilisticChildren(name): # children via probabilistic links
                # print name, " prob ", self.probabilisticChildren(name)
                if child not in self.stale[user] and child not in self.builtins and child not in (self.deterministic & self.uptodate[user]):
                    self.changeState(user, child, "stale")
        else:
            raise Exception("Exception: " + "Unknown state %s in changeState" % newstate)

    def setAllPublic(self):
        self.log.debug("All variables except builtins become public")

        # set all variables except builtins to public

        for name in self.deterministic | self.probabilistic:
            self.private.discard(name)
            self.public.discard(name)
            self.unknown_privacy.discard(name)
            self.public.add(name)

    def set_all_unknown(self, node):

        # set all variables except builtins to unknown privacy
        # for sub_graph in sub_graphs.values():
        for name in (set(node[attr_contains]) & (self.deterministic | self.probabilistic)):
            self.private.discard(name)
            self.public.discard(name)
            self.unknown_privacy.discard(name)
            self.unknown_privacy.add(name)

    def setPrivacy(self, name, privacy):
        self.private.discard(name)
        self.public.discard(name)
        self.unknown_privacy.discard(name)

        if privacy == "private":
            self.private.add(name)
        elif privacy == "public":
            self.public.add(name)
        elif privacy == "unknown_privacy":
            self.unknown_privacy.add(name)
        else:
            self.log.error("Unexpected privacy type in setPrivacy: " + privacy)

    def getPrivacy(self, name):
        if name in self.private:
            return "private"
        elif name in self.public:
            return "public"
        elif name in self.unknown_privacy:
            return "unknown_privacy"
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
                dependent_dependents = self.getChildren(dependent)
                if self.check_cyclic_dependencies(name, dependent_dependents):
                    return True

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
        for n in node[attr_contains]:
            for user in self.userids:
                self.changeState(user, n, "stale")
        # set the timestamp for node define
        node[attr_last_ts] = int(time.time() * 1000)
        # need computePrivacy before compute so we don't compute public variables for each participant
        self.compute_privacy(node, lock=False)
        if name not in self.public:
            for user in self.userids:
                self.start_computation(user, node, lock=False)
        else:
            self.start_computation(user_all, node, lock=False)
        self.release()

        self.compute_privacy(node) # every definition could change the privacy assignments

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
        self.code[name] = "User Function"
        self.evalcode[name] = evalcode
        self.dependson[name] = dependson.difference(defines).difference(arguments)
        for user in self.userids:
            self.changeState(user, name, "stale")
        self.release()
        node = self.i_graph.nodes[name]
        self.compute_privacy(node)  # need computePrivacy before compute so we don't compute public variables for each participant
        if name not in self.public:
            for user in self.userids:
                self.start_computation(user, node)
        else:
            self.start_computation(user_all, node)
        self.compute_privacy(node)

    def delete(self, name):
        self.acquire("delete "+name)
        if name in self.probabilistic | self.deterministic:

            for user in self.userids:
                self.changeState(user, name, "stale")
                self.globals[user].pop(name, None)

            self.deterministic.discard(name)
            self.probabilistic.discard(name)
            self.stale[user].discard(name)
            self.private.discard(name)
            self.public.discard(name)
            self.unknown_privacy.discard(name)
            #self.computing_privacy.discard(name)

            self.code.pop(name, None)
            self.probcode.pop(name, None)
            self.pyMC3code.pop(name, None)
            self.hierarchical.pop(name, None)

            self.dependson.pop(name, None)
            self.probdependson.pop(name, None)
            self.comment.pop(name, None)
            self.del_from_inf_graph(name)
            res = ""
        else:
            res = name + " not found."

        self.release()
        # self.compute_privacy(self.get_sub_graphs(name)) # every delete could change the privacy assignments
        return res

    def getValue(self, name, longFormat = False):
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
                if type(self.globals["All"][name]) == io.BytesIO:   # write image to file
                #res += reprlib.repr(self.globals["All"][name])
                    res += "[PNG Image]"
                elif type(self.globals["All"][name]) == RedisReference:
                    res += self.globals["All"][name].display_value
                elif type(self.globals["All"][name]) == numpy.ndarray:
                    if longFormat:
                        res += str(self.globals["All"][name])
                    else:
                        s = self.globals["All"][name].shape
                        res += "[" * len(s) + formatter_string % self.globals["All"][name].ravel()[
                            0] + " ... " + formatter_string % self.globals["All"][name].ravel()[-1] + "]" * len(s)
                elif type(self.globals["All"][name]) == float or type(self.globals["All"][name]) == numpy.float64:
                    res += str((formatter_string % self.globals["All"][name]))
                else:
                    if longFormat:
                        res += json.dumps(self.globals["All"][name], indent=4)
                    else:
                        res += reprlib.repr(self.globals["All"][name])
            else:
                raise Exception("Exception: " + name + " is not stale, computing, exception or uptodate.")
        elif name in self.builtins:
            if name in self.public:
                if longFormat:
                    res += str(self.globals["All"][name])
                else:
                    res += reprlib.repr(self.globals["All"][name])
            else:
                res += "Private"
        else:
            raise Exception("Exception: Unknown variable in getValue " + name)
        return res

    def __repr__(self):
        codebits = []
        codewidth = 50
        valuewidth = 80
        for name in self.code.keys():
            codebits.append(name + " = " + str(self.code[name]))
        for name in self.probcode.keys():
            if name in self.hierarchical:
                codebits.append(name + "[" + self.hierarchical[name] + "] ~ " + str(self.probcode[name]))
            else:
                codebits.append(name + " ~ " + str(self.probcode[name]))
        if len(codebits) > 0:
            m = max(len(line) for line in codebits)
            m = min(m, codewidth)
            newcodebits = [line[0:codewidth].ljust(m, " ") for line in codebits]
            valuebits = []
            for name in self.code.keys():
                valuebits.append(self.getValue(name)[0:valuewidth])
            for name in self.probcode.keys():
                if name in self.samplerexception:
                    valuebits.append(self.samplerexception[name])
                else:
                    valuebits.append(self.getValue(name)[0:valuewidth])
            commentbits = []
            for name in self.code.keys():
                commentbits.append(self.comment.get(name, ""))
            for name in self.probcode.keys():
                commentbits.append(self.comment.get(name, ""))
            unsatisfied_depends = []
            for name in self.code.keys():
                unsatisfied_depends.append(", ".join(self.dependson[name] - ((self.deterministic | self.probabilistic | self.builtins))))
            for name in self.probcode.keys():
                unsatisfied_depends.append(", ".join(self.probdependson[name] - ((self.deterministic | self.probabilistic | self.builtins))))
            return "\n".join("  ".join([codebit, valuebit, commentbit, unsatisfied_depend]) for codebit, valuebit, commentbit, unsatisfied_depend in zip(newcodebits, valuebits, commentbits, unsatisfied_depends))
        else:
            return ""

    def show_values(self):
        valuewidth = 120
        valuebits = []
        for name in self.code.keys():
            valuebits.append(name + " = " + self.getValue(name)[0:valuewidth])
        for name in self.probcode.keys():
            if name in self.samplerexception:
                valuebits.append(name + " ~ " + self.samplerexception[name])
            else:
                valuebits.append(name + " ~ " + self.getValue(name)[0:valuewidth])
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

    def checkup(self, user, name):
        parents = self.getParents(name) 
        if parents == set([]):
            return False
        nonuptodateparents = parents & (self.probabilistic - self.uptodate[user])
        if nonuptodateparents == set([]):
            return True
        else:
            return all(self.checkup(user, p) for p in nonuptodateparents)

    def checkdown(self, user, name):
        if name not in self.dependson and name not in self.probdependson:
            return False

        nonuptodatechildren = self.getChildren(name) - self.uptodate[user] - prob_builtins
        if nonuptodatechildren == set([]):
            return True
        else:
            return all(self.checkdown(user, p) for p in nonuptodatechildren)

    def getParents(self, name):
        parents = set([])
        for parent in self.probabilistic:
            if parent in self.probdependson:
                if name in self.probdependson[parent]:
                    parents.add(parent)
        for parent in self.deterministic:
            if parent in self.dependson:
                if name in self.dependson[parent]:
                    parents.add(parent)
        return(parents)

    def deterministicParents(self, name):
        parents = set([])
        for parent in self.deterministic:
            if parent in self.dependson:
                if name in self.dependson[parent]:
                    parents.add(parent)
        return(parents)

    def probabilisticParents(self, name):
        parents = set([])
        for parent in self.probabilistic:
            if parent in self.probdependson:
                if name in self.probdependson[parent]:
                    parents.add(parent)
        return(parents)

    def getChildren(self, name):
        return self.dependson.get(name, set([])) | self.probdependson.get(name, set([]))

    def probabilisticChildren(self, name):
        return self.probdependson.get(name, set([]))

    def deterministicChildren(self, name):
        return self.dependson.get(name, set([]))

    def topological_sort(self):
        order, enter, state = deque(), self.probabilistic | self.deterministic, {}
        enter = OrderedSet( sorted(list(enter)) )
        GRAY, BLACK = 0, 1

        def dfs(node):
            state[node] = GRAY
            for k in sorted( list( self.dependson.get(node, set()) | self.probdependson.get(node, set()))):
                sk = state.get(k, None)
                try:
                    if sk == GRAY: raise ValueError("cycle")
                except Exception as e:
                    _log.debug("topological_sort GREY")
                    _log.debug(self.dependson.get(node ))
                    _log.debug(self.probdependson.get(node))
                    raise ValueError("cycle 2")
                if sk == BLACK: continue
                enter.discard(k)
                dfs(k)
            order.appendleft(node)
            state[node] = BLACK

        while enter: dfs(enter.pop())
        result =  [name for name in order if name in self.probabilistic - self.deterministic]
        result.reverse()
        return result

    def topological_sort_bak(self):
        result = []
        seen = set()
        prob_only = self.probabilistic - self.deterministic
        node = list(prob_only)[0]

        def recursive_helper(node):
            for neighbor in self.dependson.get(node, []):
                if neighbor not in seen:
                    seen.add(neighbor)
                    recursive_helper(neighbor)
            result.insert(0, node)

        recursive_helper(node)
        return result

    def constructPyMC3code(self, node, user=None):
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

            for indexvariable in list(set(self.hierarchical.values()) & set(sub_graph)):
                code += "    global __%s_Dict \n" % indexvariable
                code += "    __%s_Dict = dict((key, val) for val, key in enumerate(set(%s))) \n" % (indexvariable, indexvariable)
                code += "    __%s_Indices = [__%s_Dict[__private_index__] for __private_index__ in %s]\n" % (indexvariable, indexvariable, indexvariable)
                #code += "    debug_logger(['%s', __%s_Dict])" % (indexvariable, indexvariable)
                if user:
                    locals[indexvariable] = self.globals[user][indexvariable]

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

            probabilistic_only_names = self.topological_sort() # pyMC3 requires that these are ordered so that things that are dependent come later
            if sub_graph:
                probabilistic_only_names = [n for n in probabilistic_only_names if n in sub_graph]

            for name in probabilistic_only_names:
                #code += '        debug_logger(["probabilistic_only_names", "%s"])' % (name) 
                code += '        exception_variable = "%s"\n' % name
                if name in self.hierarchical:
                    shapecode = ", shape = len(__%s_Dict)" % self.hierarchical[name]
                    code += "        " + self.pyMC3code[name] % shapecode + "\n"
                else:
                    code += "        " + self.pyMC3code[name] % ""+ "\n"

            observed_names = list(self.probabilistic & self.deterministic & set(sub_graph))
            for name in observed_names:
                #code += '        debug_logger(["observed_names_names", "%s"])' % (name) 
                code += '        exception_variable = "%s"\n' % name
                obsname = "__private_%s_observed" % name
                code += "        " + self.pyMC3code[name] % (", observed=%s" % obsname) + "\n"
                if user:
                    if name in self.globals[user]:
                        locals[obsname] = self.globals[user][name]
                    else: 
                        locals[obsname] = self.globals["All"][name]
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
        #ind = min( e.args[0].find(":"), e.args[0].find("\\n"))
        #ind = e.args[0].find(":")
        #if ind != -1:
        #    estring = e.args[0][0:ind]
        #else:
        #    estring = e.args[0]
        #newErrorString = estring   # do we need to do this?

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

    def have_samples(self, user, sub_graph):
        # have to allow for possibility that some probabilistic variables are not retained and
        # therefore won't have samples
        # so see if any of the probabilistic variables have samples
        return any(isinstance(self.globals[user].get(aname, None), numpy.ndarray) for aname in
                   (self.probabilistic & set(sub_graph)))

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
                    self.changeState(user, name, "exception")
            elif self.ts[compute_key][user][name][started_key] == node_ts:
                original_value = self.globals[user].get(name, '')
                self.globals[user][name] = value
                self.changeState(user, name, "uptodate")
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
                    if type(value) == io.BytesIO:   # write image to file
                        value.seek(0)
                        with open(name+'.png', 'wb') as f:
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
        myname, user, node, value, exception_variable, stats = Private.s3_helper.read_results_s3(
            return_value) if Private.config.s3_integration else return_value
        names = node[attr_contains]
        n_id = node[attr_id]
        node_ts = node[attr_last_ts]
        print('at sampler callback ', names, user, node_ts)
        if isinstance(value, Exception):
            self.log.debug("Exception in sampler callback %s %s" % (user, str(value)))
            for name in names:
                # ** Might need to remove the Exception message here
                self.globals[user][name] = str(value)
                debug_logger(["samplercallback Exception", user, name, value])
                self.changeState(user, name, "exception")
            if exception_variable != "No Exception Variable":
                m = re.match("__init__\(\) takes at least (\d+) arguments \(\d+ given\)", str(value))
                if m:
                    value = str(int(m.group(1)) - 1) + " arguments required."
                self.samplerexception[user][exception_variable] = str(value)
            else:
                for name in names:
                    self.samplerexception[user][name] = str(value)
            self.log.debug("Exception in sampler callback %s %s ...done" % (user, str(value)))
        elif self.ts[sampler_key][user][n_id][started_key] == node_ts:  # successful sampler return
            try:
                self.log.debug("samplercallback: name in names ")
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
                        self.globals[user][
                            name] = "Not retained."  # so there could be more information in the joint information
                    self.changeState(user, name, "uptodate")

                self.log.debug("samplercallback: name in names ...done ")
                self.reg_ts(sampler_key, user, n_id, completed_key, node_ts)

                complete_users = [u for u in self.userids if u != "All" and set(names).issubset(self.uptodate[u])]

                if user == "All":  # if this is All then initiate comparisons with all of the users that have already returned
                    if stats:
                        for stat_key in stats["rhat"]:
                            self.globals[user]['rhat'][stat_key] = numpy.array(stats["rhat"][stat_key]).tolist()
                            self.globals[user]['ess'][stat_key] = numpy.array(stats["ess"][stat_key]).tolist()
                            self.globals[user]['waic'][stat_key] = stats["waic"]
                            self.globals[user]['loo'][stat_key] = stats["loo"]
                    for u in complete_users:
                        # go through variables if we already know they are private do nothing else initiate manifold privacy calculation
                        for name in names:
                            if self.get_privacy_sampler_result(name) != 'private' and not (
                                    isinstance(self.globals[user].get(name), str) and self.globals[user].get(
                                    name) == "Not retained."):
                                if name in self.globals[u].keys() and name in self.globals["All"].keys():
                                    if self.globals[u][name].shape != self.globals["All"][
                                     name].shape:  # if shape is affected by dropping a user then this variable is private
                                        self.privacy_sampler_results[name][u] = 'private'
                                    else:
                                        success = self.reg_ts(manifold_key, u, name, started_key, node_ts)
                                        if success:
                                            jobname = "Manifold: " + u + " " + name
                                            self.jobs[jobname] = self.server.submit(mp_job, jobname, node, name, u,
                                                                                    self.globals[u][name],
                                                                                    self.globals["All"][name])
                                            self.jobs[jobname].add_done_callback(self.mp_callback)
                                            print('started job ', jobname, node_ts)


                else:  # else compare All to this users samples using manifold privacy calculation
                    self.log.debug("samplercallback: complete_users - Users ")
                    if self.have_samples("All", names):
                        # go through variables if we already know they are private do nothing else initiate manifold privacy calculation
                        for name in names:
                            if self.get_privacy_sampler_result(name) != 'private' and not (
                                    isinstance(self.globals[user].get(name), str) and self.globals[user].get(
                                    name) == "Not retained."):
                                if name in self.globals[user].keys() and name in self.globals["All"].keys():
                                    if self.globals[user][name].shape != self.globals["All"][
                                     name].shape:  # if shape is affected by dropping a user then this variable is private
                                        self.privacy_sampler_results[name][user] = 'private'
                                    else:
                                        success = self.reg_ts(manifold_key, user, name, started_key, node_ts)
                                        if success:
                                            jobname = "Manifold: " + user + " " + name
                                            self.jobs[jobname] = self.server.submit(mp_job, jobname, node, name, user,
                                                                                    self.globals[user][name],
                                                                                    self.globals["All"][name])
                                            self.jobs[jobname].add_done_callback(self.mp_callback)
                                            print('started job ', jobname, node_ts)
                                else:
                                    # Some variables (e.g., logs of SDs) are returned from the sampler, but are not variables in our code.
                                    pass
            except Exception as e:
                self.log.debug("in samplercallback when assigning values " + str(e))

        self.log.debug("sampler_callback: delete jobs ")

        try:
            del self.jobs[myname]
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
        jobname, node, name, user, d = return_value
        node_ts = node[attr_last_ts]
        print('at mp callback ', name, user, node_ts)
        if self.ts[manifold_key][user][node[attr_id]][started_key] == node_ts:
            try:
                self.log.debug("manifoldprivacycallback: " + user + ": " + name + ": " + str(d) + " " + str(d < PrivacyCriterion))
                if self.get_privacy_sampler_result(name) != 'private':
                    print("d:", d)
                    if d > PrivacyCriterion:
                        print(name, " marked as private")
                        self.privacy_sampler_results[name][user] = "private"

                        self.globals['All'][name] = self.globals['All'][name][::step_size][:Private.config.max_sample_size] ##
                        self.log.debug("manifoldprivacycallback: " + user + ": " + name + ": " + str(d) + " " + str(d < PrivacyCriterion) + ": PRIVATE")
                    else:
                        self.log.debug("manifoldprivacycallback: " + user + ": " + name + ": " + str(d) + " " + str(d < PrivacyCriterion) + ": UNKNOWN_PRIVACY")
                        self.privacy_sampler_results[name][user] = "public"

                    print(self.privacy_sampler_results[name])

                if self.get_privacy_sampler_result(name) == 'public':
                    self.globals['All'][name] = self.globals['All'][name][::step_size][:Private.config.max_sample_size]
                    self.log.debug("manifoldprivacycallback: " + user + ": " + name + ": PUBLIC")
                self.reg_ts(manifold_key, user, name, completed_key, node_ts)

            except Exception as e:
                self.log.debug("manifold privacy " + str(e))
                print("manifold privacy " + str(e))
        
        try:
            del self.jobs[jobname]
        except Exception as e:
            self.log.debug("trying to del job " + str(e))
        self.release()
        self.compute_privacy(node)

    def get_privacy_sampler_result(self, name):
        public_count = 0
        for user in self.privacy_sampler_results[name]:
            if name in self.uptodate[user] and self.privacy_sampler_results[name][user] == 'private':
                return 'private'
            elif name in self.uptodate[user] and self.privacy_sampler_results[name][user] == 'public':
                public_count += 1
        if public_count == len(self.userids) -1:
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

    def del_from_inf_graph(self, name):
        """
        Delete a node from the inferential graph (i_graph), **Yet to implement
        :param name: String, name of the node
        """
        return

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
                    # sub_graph.extend(node_1_graph)
                elif node_1.startswith(pd_key):
                    node_label = node_0
                    # sub_graph.extend(node_0_graph)
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

    def start_computation(self, user, node, lock=True):
        """
        Start computation for the given node for the given user

        :param user: String
        :param node: Dict {'id': a, 'contains': [c, d], 'is_prob':False ...}
        :return:
        """
        node = copy.deepcopy(node)
        if lock:
            self.acquire("compute")
        n_id = node[attr_id]
        node_ts = node[attr_last_ts]
        if not self.is_node_computable(user, n_id):
            if lock:
                self.release()
            return
        else:
            job_globals = self.get_globals(node[attr_contains], user)
            for name in node[attr_contains]:
                self.changeState(user, name, "computing")
            if node[attr_is_prob]:
                success = self.reg_ts(sampler_key, user, n_id, started_key, node_ts)
                if success:
                    job_name = "Sampler:  " + user + ", " + str(node[attr_label])
                    job_locals, sampler_code = self.constructPyMC3code(node, user)
                    self.reset_privacy_results(node, user)
                    self.jobs[job_name] = self.server.submit(sampler_job, job_name, user, node, sampler_code, job_globals,
                                                             job_locals, resources={'process': 1})
                    self.jobs[job_name].add_done_callback(self.sampler_callback)
                    print('started job ', job_name, node_ts)
            else:
                success = self.reg_ts(compute_key, user, n_id, started_key, node_ts)
                if success:
                    job_name = "Compute:  " + user + " " + n_id
                    user_func = [self.evalcode[func_name] for func_name in self.functions]
                    self.jobs[job_name] = self.server.submit(job, job_name, node, user, self.evalcode[n_id], job_globals,
                                                             self.locals, user_func, self.project_id, self.shell_id)
                    self.jobs[job_name].add_done_callback(self.callback)
        if lock:
            self.release()

    def reset_privacy_results(self, node, user):
        for name in node[attr_contains]:
            if name in self.privacy_sampler_results and user != user_all:
                self.privacy_sampler_results[name][user] = 'unknown_privacy'
            else:
                self.privacy_sampler_results[name] = {}

    def init_ts(self):
        for job_type in [compute_key, sampler_key, manifold_key]:
            self.ts[job_type] = {}
            for user in self.userids:
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

    def draw_generative_graph(self):
        G = nx.DiGraph()
        visited, stack = set(), list(self.probabilistic | self.deterministic)
        while stack:
            vertex = stack.pop()
            G.add_node(vertex)
            if vertex not in visited:
                visited.add(vertex)
                for k in self.dependson.get(vertex, set()) | self.probdependson.get(vertex, set()):
                    G.add_edge(vertex, k)
                    stack.append(k)
        pos = nx.spring_layout(G, scale=2)
        nx.draw_networkx(G, pos, node_color='cornflowerblue', node_size=100, with_labels=False)
        if len(pos) > 1:
            for p in pos:  # raise text positions
                pos[p][1] += 0.15
        nx.draw_networkx_labels(G, pos, font_size=10)
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        result = "data:image/png;base64, " + base64.b64encode(buf.getvalue()).decode()
        plt.savefig('generative_graph.png')
        plt.clf()
        plt.close()
        return result


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
            exec (func, s3_var_globals)
        except Exception as e:
            e = Exception("Error in User Function: " + func[4:10] + "...")
            return ((job_name, name, user, e))
    try:
        if code.startswith("def"):
            value = "User Function"
        else:
            value = eval(code, s3_var_globals, locals)
        if get_size(value) > 1e6:
        #if True:
            value = RedisReference(redis_key, value)

        return (job_name, node, user, value)
    except Exception as e:
        return((job_name, node, user, e))


def sampler_job(job_name, user, node, code, globals, locals):
    numpy.random.seed(Private.config.numpy_seed)
    try:
        s3vars = retrieve_s3_vars(globals)
        exec (code, s3vars, locals)
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
        return (job_name, user, node, e, "No Exception Variable", None)


def mp_job(jobname, node, name, user, firstarray, secondarray):
    from Private.manifoldprivacy import distManifold
    debug_logger("manifoldprivacyjob : {} [{}] Shape sminus: {} \nSall {}".format(name, user, firstarray.shape, secondarray.shape) )
    debug_logger("manifoldprivacyjob : {} [{}] Sum sminus: {} \nSall {}".format(name, user, firstarray.sum(), secondarray.sum()) )

    d = distManifold(firstarray, secondarray) * 100.
    return jobname, node, name, user, d


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
