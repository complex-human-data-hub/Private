import copy
import multiprocessing
import reprlib
import sys
import traceback
import time
from itertools import permutations

import numpy
import numpy.random
from collections import OrderedDict, deque
import logging
import networkx as nx
import graphviz as gv
import Private
from Private.builtins import builtins, prob_builtins, set_builtin_privacy, set_globals, config_builtins, \
    illegal_variable_names, keep_private_variables
from Private.graph_constants import pd_key, p_key, d_key, attr_label, attr_color, attr_is_prob, attr_contains, \
    attr_id, attr_last_ts, user_all, compute_key, sampler_key, manifold_key, completed_key, started_key, pt_private, \
    pt_public, pt_unknown, st_stale, st_uptodate, st_computing, st_exception, graph_folder, attr_pd_node, st_not_retained

from Private.reference import Reference
import Private.redis_helper as redis_helper
import shutil
import io
import re
import os
import base64
import pymc3 as pm
from dask.distributed import Client
from ordered_set import OrderedSet
import json
from .config import config_logger

config_logger()
logger = logging.getLogger("Private")

numpy.set_printoptions(precision=3)
numpy.set_printoptions(threshold=2000)

privacy_criterion = 15.0   # percent
display_precision = 3


def pp_set(s):
    """
    Pretty print a set.
    """
    s = list(s)
    s.sort()
    return " ".join(s)


class PrivateGraphException(Exception):
    """
    Allows us to separate private exceptions from more generic exceptions
    """
    pass


class Graph:

    def __init__(self, events=None, project_id='proj1', shell_id=None, load_demo_events=True, user_ids=None):
        logger.info("Graph init")
        if not user_ids:
            raise PrivateGraphException("No user_ids provided")

        # variable types
        if not shell_id:
            shell_id = 'shell1'
        # clear the cache for the shell

        logger.debug("Graph delete_user_keys")
        redis_helper.delete_user_keys(project_id, shell_id)
        logger.debug("Graph delete_user_keys ...done")

        self.deterministic = set()
        self.probabilistic = set()
        self.functions = set()
        self.builtins = set(builtins.keys()) | prob_builtins

        # dependencies

        self.dependson = {}  # deterministic dependencies
        self.probdependson = {}  # probabilistic dependencies

        # variables related to values
        if events and type(events) == Reference:
            events = events.value()
        self.project_id = project_id
        self.shell_id = shell_id
        self.load_demo_events = load_demo_events
        logger.debug("Graph set_globals")
        if 'All' not in user_ids:
            user_ids = ['All'] + user_ids
        self.user_ids = OrderedSet(user_ids)
        self.globals = set_globals(user_ids)
        logger.debug("Graph set_globals ...done")

        self.locals = {}  # do we need this?
        self.stale = dict([(u, set()) for u in self.user_ids])
        self.computing = dict([(u, set()) for u in self.user_ids])
        self.exception = dict([(u, set()) for u in self.user_ids])
        self.uptodate = dict([(u, set(builtins.keys()) or prob_builtins) for u in self.user_ids])
        self.sampler_exception = dict([(u, {}) for u in self.user_ids])

        # variables related to privacy

        self.private = set()
        self.public = set()
        self.unknown_privacy = set()
        self.privacy_sampler_results = {}
        # the privacy samplers haven't been run since last compute and when they have been run

        # code associated with variables

        self.code = OrderedDict()  # private code for deterministic variables
        self.prob_code = OrderedDict()  # private code of probabilistic variables
        self.eval_code = OrderedDict()  # python code for deterministic variables
        self.py_mc3_code = OrderedDict()  # pyMC3 code for probabilistic variables
        self.hierarchical = {}  # what is the index variable of this hierarchical variable

        # comments

        self.comment = {}

        # auxiliary variables

        self.lock = multiprocessing.Lock()
        self.who_has_lock = None
        self.jobs = {}
        self.log = logging.getLogger("Private")
        self.last_server_connect = 0
        self.server = None
        self.check_dask_connection()
        self.raw_graph = None
        self.i_graph = None
        self.p_graph = None

        logger.debug("Graph init_raw_graph")
        self.init_raw_graph()
        logger.debug("Graph init_raw_graph ...done")

        # Keep the time stamps [job_type][user][id][last_completed/last_started]
        logger.debug("Graph init_ts")
        self.ts = {}
        self.init_ts()
        logger.debug("Graph init_ts ...done")

        self.sampler_parameter_updated = False

        logger.debug("Graph set_builtin_privacy")
        set_builtin_privacy(self)  # set privacy of builtins
        logger.debug("Graph set_builtin_privacy ...done")

        logger.debug("Graph init define")
        self.define("Events", "", eval_code="getEvents(project_id, user_id)", depends_on=["getEvents"],
                    skip_name_check=True)
        
        if self.load_demo_events:
            self.define("DemoEvents", "", eval_code="getDemoEvents(project_id, user_id)",
                        depends_on=["getDemoEvents"], skip_name_check=True)

        self.define("NumberOfTuningSamples", "", eval_code="getNumberOfTuningSamples()",
                    depends_on=["getNumberOfTuningSamples"])
        self.define("NumberOfChains", "", eval_code="getNumberOfChains()", depends_on=["getNumberOfChains"])
        self.define("NumberOfSamples", "", eval_code="getNumberOfSamples()", depends_on=["getNumberOfSamples"])
        self.define("rhat", "", eval_code="{}", skip_name_check=True)
        self.define("ess", "", eval_code="{}", skip_name_check=True)
        self.define("loo", "", eval_code="{}", skip_name_check=True)
        self.define("waic", "", eval_code="{}", skip_name_check=True)

        logger.debug("Graph init define done")

    def check_dask_connection(self):

        if self.server is None:
            self.server = Client(f'{Private.config.dask_scheduler_ip}:{Private.config.dask_scheduler_port}')

        return None

    def cancel_all_jobs(self):
        for future in self.jobs.values():
            future.cancel()

    def acquire(self, who):
        self.lock.acquire()
        self.who_has_lock = who
        self.log.debug(who + " just got lock")

    def release(self):
        self.log.debug(self.who_has_lock + " just released lock")
        self.who_has_lock = None
        self.lock.release()

    # Helper functions

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
                    logger.debug("topological_sort GREY")
                    logger.debug(self.dependson.get(node))
                    logger.debug(self.probdependson.get(node))
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

    def get_globals(self, node, user):
        all_globals = self.globals[user_all]
        user_globals = self.globals[user]
        job_globals = {'user_id': user, 'project_id': self.project_id}
        deps = set()
        predecessors = self.get_dep_predecessors(node[attr_id])
        for p_id in predecessors:
            predecessor = self.i_graph.nodes[p_id]
            is_prob = predecessor[attr_is_prob]
            deps = deps.union(set([p for p in predecessor[attr_contains] if not p.startswith(pd_key)]))
            for key in set([p for p in predecessor[attr_contains] if not p.startswith(pd_key)]):
                globals_edited = all_globals if key in self.public else user_globals
                if key in globals_edited.keys() and key not in job_globals.keys():
                    value = globals_edited[key]
                    if type(value) == Reference:
                        job_globals[key] = copy.copy(value)
                    else:
                        if is_prob and type(value) == numpy.ndarray:
                            sample_size = all_globals['NumberOfSamples'] * all_globals['NumberOfChains']
                            # Thinning the samples if used for further calculations
                            if value.size > Private.config.max_sample_size:
                                step_size = max(int(sample_size / Private.config.max_sample_size), 1)
                                value = value[::step_size][:Private.config.max_sample_size]
                        job_globals[key] = value
        return job_globals

    # Privacy manipulations

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
        is_prob = self.p_graph.nodes[name][attr_is_prob]
        if all([self.get_privacy(parent) == pt_public for parent in predecessors]):
            self.set_privacy(name, pt_public)
        elif any([self.get_privacy(parent) == pt_private for parent in predecessors]) and not is_prob:
            self.set_privacy(name, pt_private)

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
            if name in self.unknown_privacy and name in self.privacy_sampler_results:
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
                raise PrivateGraphException(f"Exception: Unknown state {new_state} in changeState")

        # Set all to children to stale
        if new_state == st_stale:
                for child in self.i_graph.successors(node[attr_id]):
                    self.change_state(user, self.i_graph.nodes[child], new_state)

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

    def reset_privacy_results(self, node, user):
        for name in node[attr_contains]:
            if name in self.privacy_sampler_results and user != user_all:
                self.privacy_sampler_results[name][user] = pt_unknown
            else:
                self.privacy_sampler_results[name] = {}

    def get_privacy_sampler_result(self, name):
        public_count = 0
        for user in self.privacy_sampler_results[name]:
            if name in self.uptodate[user] and self.privacy_sampler_results[name][user] == pt_private:
                return pt_private
            elif name in self.uptodate[user] and self.privacy_sampler_results[name][user] == pt_public:
                public_count += 1
        if public_count == len(self.user_ids) - 1:
            return pt_public
        else:
            return pt_unknown

    # Core functions
    def define(self, name, code, eval_code=None, depends_on=None, prob=False, h_var=None, py_mc3_code=None,
               skip_name_check=False):
        if not skip_name_check and name in prob_builtins | illegal_variable_names:
            raise PrivateGraphException(f"Exception: Illegal Identifier '{name}' is a Private Built-in")

        self.acquire("define " + name)

        # check if the exact thing already defined
        if (name in self.probabilistic and self.prob_code[name] == code) or (
                name in self.deterministic and self.code[name] == code):
            self.release()
            return

        if not depends_on:
            depends_on = []
        else:
            if self.check_cyclic_dependencies(name, set(depends_on)):
                self.release()
                raise PrivateGraphException("Exception: Cyclic Dependency Found, " + name)

        if prob:
            self.probabilistic.add(name)
            self.prob_code[name] = code
            self.py_mc3_code[name] = py_mc3_code
            if depends_on:
                self.probdependson[name] = set(depends_on)
            if h_var:
                self.hierarchical[name] = h_var
        else:
            self.deterministic.add(name)
            self.code[name] = code
            self.eval_code[name] = eval_code
            self.dependson[name] = set(depends_on)


        self.add_to_raw_graph(name, depends_on, h_var, prob)
        node = self.get_node(name, prob)
        # set the timestamp for node define
        node[attr_last_ts] = int(time.time() * 1000000)
        # need computePrivacy before compute so we don't compute public variables for each participant
        self.compute_privacy(node, lock=False)
        if name not in self.public:
            for user in self.user_ids:
                self.change_state(user, node, "stale")
            for user in self.user_ids:
                self.start_computation(user, node, lock=False)
        else:
            self.change_state(user_all, node, "stale")
            self.start_computation(user_all, node, lock=False)
        self.compute_privacy(node, lock=False)
        self.release()

    def define_function(self, name, code, evalcode, dependson, defines, arguments):
        if name in prob_builtins | illegal_variable_names:
            raise PrivateGraphException("Exception: Illegal Identifier '" + name + "' is a Private Built-in")
        self.acquire("define " + name)

        # check if the exact thing already defined
        if name in self.deterministic and self.code[name] == code and self.eval_code[name] == evalcode:
            self.release()
            return

        if not dependson:
            dependson = set()
        else:
            if self.check_cyclic_dependencies(name, dependson):
                self.release()
                raise PrivateGraphException("Exception: Cyclic Dependency Found, " + name)
        self.deterministic.add(name)
        self.functions.add(name)
        self.code[name] = code
        self.eval_code[name] = evalcode
        self.dependson[name] = dependson.difference(defines).difference(arguments)
        self.add_to_raw_graph(name, dependson.difference(defines).difference(arguments), None, False)
        node = self.i_graph.nodes[name]
        for user in self.user_ids:
            self.change_state(user, node, "stale")

        node[attr_last_ts] = int(time.time() * 1000000)
        # need computePrivacy before compute so we don't compute public variables for each participant
        self.compute_privacy(node, lock=False)
        if name not in self.public:
            for user in self.user_ids:
                self.start_computation(user, node, lock=False)
        else:
            self.start_computation(user_all, node, lock=False)
        self.compute_privacy(node, lock=False)
        self.release()

    def delete(self, name, is_prob=True):
        self.acquire("delete " + name)
        
        if name in keep_private_variables:
            res = name + " cannot be deleted"
        elif name in self.probabilistic | self.deterministic:

            node = self.get_node(name, is_prob)
            pd_node = False

            for user in self.user_ids:
                self.change_state(user, node, "stale")

            if name in self.deterministic and name in self.probabilistic:
                self.set_all_unknown(node)
                pd_node = True
            else:
                for user in self.user_ids:
                    self.globals[user].pop(name, None)
                    self.stale[user].discard(name)
                self.private.discard(name)
                self.public.discard(name)
                self.unknown_privacy.discard(name)
                self.comment.pop(name, None)

            if is_prob:
                self.probabilistic.discard(name)
                self.prob_code.pop(name, None)
                self.py_mc3_code.pop(name, None)
                self.hierarchical.pop(name, None)
                self.probdependson.pop(name, None)
            else:
                self.deterministic.discard(name)
                self.code.pop(name, None)
                self.dependson.pop(name, None)
                self.functions.discard(name)

            self.raw_graph_del_node(name, is_prob)
            node_ts = int(time.time() * 1000000)
            self.del_ts(node[attr_id], node_ts)

            # if deterministic node of the pd-node is deleted
            if pd_node and not is_prob:
                successor = self.get_node(name, True)
                if successor:
                    successor[attr_last_ts] = int(time.time() * 1000000)
                    self.start_computation(user_all, successor, lock=False)

            # if a node belongs to a probabilistic node is deleted
            elif len(node[attr_contains]) > 1:
                if not pd_node:
                    node[attr_contains].remove(name)
                contains = {}
                for c in node[attr_contains]:
                    new_node = self.get_node(c, True)
                    if new_node and new_node[attr_id] not in contains:
                        new_node[attr_last_ts] = int(time.time() * 1000000)
                        contains[new_node[attr_id]] = new_node
                for new_node in contains.values():
                    self.start_computation(user_all, new_node, lock=False)
            res = ""

        else:
            res = name + " not found."

        self.release()
        return res

    def construct_pymc3_code(self, node, user=None):
        #try:
            locals = {}
            sub_graph = node[attr_contains] + list(self.i_graph.predecessors(node[attr_id]))
            loggingcode = """
try:
    logging = __import__("logging")
    FORMAT = '[%(asctime)s] %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    logger = logging.getLogger("Private")
    #logging.disable(100)
    logger.info("Running PyMC3 Code")
    json = __import__("json")
"""

            code = loggingcode

            # extract index variables

            for index_variable in list(set(self.hierarchical.values()) & set(sub_graph)):
                code += "    global __%s_Dict \n" % index_variable
                code += "    __%s_Dict = dict((key, val) for val, key in enumerate(sorted(set(%s)))) \n" % (
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
                    code += "        " + self.py_mc3_code[name] % shape_code + "\n"
                else:
                    code += "        " + self.py_mc3_code[name] % "" + "\n"

            observed_names = list(self.probabilistic & self.deterministic & set(sub_graph))
            for name in observed_names:
                code += '        exception_variable = "%s"\n' % name
                obs_name = "__private_%s_observed" % name
                code += "        " + self.py_mc3_code[name] % (", observed=%s" % obs_name) + "\n"
                if user:
                    if name in self.globals[user]:
                        locals[obs_name] = self.globals[user][name]
                    else:
                        locals[obs_name] = self.globals["All"][name]
                else:
                    locals = None

            code += """
        __private_result__ = (pymc3.sample({NumberOfSamples}, tune={NumberOfTuningSamples}, chains={NumberOfChains}, random_seed=987654321, progressbar = False), "No Exception Variable", basic_model)
        logger.info("Finished PyMC3 Code")
        with open("/tmp/private-worker.log", "a") as fp:
            fp.write("Finished PyMC3 Code\\n")

except Exception as e:
    try:
        # remove stuff after the : as that sometimes reveals private information
        logger.debug("PyMC3 Code Exception: " + str(e))
        with open("/tmp/private-worker.log", "a") as fp:
            fp.write("Error " + str(e) + "\\n")

        estring = e.args[0]
        newErrorString = estring[estring.rfind("\\n")+1:]
        if 'Bad initial energy' in newErrorString:
            newErrorString +=  "\\n" + str(basic_model.check_test_point()) + "\\n\\n" + json.dumps(basic_model.test_point, indent=4, default=str)

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

        

""".format(NumberOfSamples=self.globals["All"]["NumberOfSamples"], NumberOfChains=self.globals["All"]["NumberOfChains"],
            NumberOfTuningSamples=self.globals["All"]["NumberOfTuningSamples"])

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
        if n_id.startswith(pd_key) or not self.is_node_computable(user, node):
            if lock:
                self.release()
            return
        else:
            job_globals = self.get_globals(node, user)
            if node[attr_is_prob]:
                success = self.reg_ts(sampler_key, user, n_id, started_key, node_ts)
                if success:
                    self.change_state(user, node, "computing")
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
                    self.change_state(user, node, "computing")
                    job_name = "Compute:  " + user + " " + n_id
                    user_func = [self.eval_code[func_name] for func_name in self.functions]
                    self.jobs[job_name] = self.server.submit(job, job_name, node, user, self.eval_code[n_id],
                                                             job_globals,
                                                             self.locals, user_func, self.project_id, self.shell_id)
                    self.jobs[job_name].add_done_callback(self.callback)
        if lock:
            self.release()

    def start_mp_job(self, user, node):
        names = node[attr_contains]
        node_ts = node[attr_last_ts]
        for name in names:
            if self.get_privacy_sampler_result(name) != pt_private and not (
                    isinstance(self.globals[user].get(name), str) and self.globals[user].get(name) == st_not_retained) \
                    and name in self.globals[user].keys() and name in self.globals["All"].keys():
                # Some variables (e.g., logs of SDs) are returned from the sampler, but are not variables in our code.
                # if shape is affected by dropping a user then this variable is private
                if self.globals[user][name].shape != self.globals["All"][name].shape:
                    self.privacy_sampler_results[name][user] = pt_private
                else:
                    success = self.reg_ts(manifold_key, user, name, started_key, node_ts)
                    if success:
                        job_name = "Manifold: " + user + " " + name
                        self.jobs[job_name] = self.server.submit(mp_job, job_name, node, name, user,
                                                                 self.globals[user][name],
                                                                 self.globals["All"][name])
                        self.jobs[job_name].add_done_callback(self.mp_callback)

    def callback(self, return_value):
        return_value = return_value.result()
        self.acquire("callback")
        logger.debug("In callback")
        job_name, node, user, value = return_value
        name = node[attr_id]
        node_ts = node[attr_last_ts]
        valid_node = name in self.i_graph.nodes and (
                    set(self.i_graph.nodes[name][attr_contains]) == set(node[attr_contains]))
        successful_return = valid_node and name in self.ts[compute_key][user] and self.ts[compute_key][user][name][
            started_key] == node_ts
        try:
            if isinstance(value, Exception):
                if user == "All":
                    logger.debug(["callback Exception", user, name, value])
                    logger.error("callback Exception")
                    function_stack = [s.name for s in traceback.extract_tb(value.__traceback__)[2:]]
                    self.globals[user][name] = str(value) + ' in ' + ' > '.join(function_stack)
                    self.change_state(user, node, "exception")
            elif successful_return:
                original_value = self.globals[user].get(name, '')
                self.globals[user][name] = value
                self.change_state(user, node, "uptodate")
                self.reg_ts(compute_key, user, name, completed_key, node_ts)
                if user == "All":
                    if name in config_builtins:
                        builtins.get(name)(value)
                    if name in ["NumberOfSamples", "NumberOfChains", "NumberOfTuningSamples"]:
                        if name == "NumberOfSamples" and value > 4000:
                            self.comment[name] = "# Maximum Number of Samples is 4000"
                            self.globals[user][name] = original_value
                        self.sampler_parameter_updated = True
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

        if successful_return:
            self.compute_privacy(node, lock=False)
            for n in self.i_graph.successors(name):
                successor = self.i_graph.nodes[n]
                successor[attr_last_ts] = int(time.time() * 1000000)
                successor_contains = successor[attr_contains]
                all_public = all([p in self.public for p in successor_contains if not p.startswith(pd_key)])
                node_public = node[attr_id] in self.public
                if not node_public:
                    self.start_computation(user, successor, lock=False)
                else:
                    if all_public:
                        self.start_computation(user, successor, lock=False)
                    else:
                        for u in self.user_ids:
                            self.start_computation(u, successor, lock=False)
            self.compute_privacy(node, lock=False)
        self.release()

    def sampler_callback(self, return_value):
        return_value = return_value.result()
        self.acquire("sampler_callback")
        job_name, user, node, value, exception_variable, stats = return_value
        names = node[attr_contains]
        n_id = node[attr_id]
        node_ts = node[attr_last_ts]
        valid_node = n_id in self.i_graph.nodes and (
                    set(self.i_graph.nodes[n_id][attr_contains]) == set(node[attr_contains]))
        successful_return = valid_node and n_id in self.ts[sampler_key][user] and self.ts[sampler_key][user][n_id][
            started_key] == node_ts
        if isinstance(value, Exception):
            self.log.debug("Exception in sampler callback %s %s" % (user, str(value)))
            for name in names:
                # ** Might need to remove the Exception message here
                self.globals[user][name] = str(value)
                logger.debug(["sampler_callback Exception", user, name, value, exception_variable])
                logger.error("sampler_callback Exception")
            self.change_state(user, node, "exception")
            if exception_variable != "No Exception Variable":
                m = re.match(r"__init__\(\) takes at least (\d+) arguments \(\d+ given\)", str(value))
                if m:
                    value = str(int(m.group(1)) - 1) + " arguments required."
                ## ** Changing to use name instead of exception_variable          ##
                ## ** May have unwanted side effect, but I can't see it           ##
                ## ** So leaving this ugly message for now                        ## 
                #self.sampler_exception[user][exception_variable] = str(value)    
                self.sampler_exception[user][name] = str(value)
            else:
                for name in names:
                    self.sampler_exception[user][name] = str(value)
            self.log.debug("Exception in sampler callback %s %s ...done" % (user, str(value)))
        elif successful_return:
            try:
                self.log.debug("sampler_callback: name in names ")
                for name in names:
                    if name in value.varnames:
                        name_long = int("".join(map(str, [ord(c) for c in name])))
                        # 4294967291 seems to be the largest prime under 2**32 (int limit)
                        seed = name_long % 4294967291
                        logger.debug("name_seed {}: {} ({})".format(name, seed, name_long))
                        numpy.random.seed(seed)
                        self.globals[user][name] = numpy.random.permutation(
                            value[name])  # permute to break the joint information across variables
                    else:  # manifold privacy is applied to individual variables
                        # so there could be more information in the joint information
                        self.globals[user][name] = st_not_retained
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

        if successful_return:
            self.compute_privacy(node, lock=False)
            for u in self.i_graph.successors(node[attr_id]):
                successor = self.i_graph.nodes[u]
                successor[attr_last_ts] = int(time.time() * 1000000)
                self.start_computation(user, successor, lock=False)
            self.compute_privacy(node, lock=False)
        self.release()

    def mp_callback(self, return_value):
        return_value = return_value.result()
        self.acquire("mp_callback")
        job_name, node, name, user, d = return_value
        node_ts = node[attr_last_ts]
        successful_return = node[attr_id] in self.ts[manifold_key][user] and self.ts[manifold_key][user][node[attr_id]][
            started_key] == node_ts
        if successful_return:
            try:
                self.log.debug(f"mp_callback: {user}: {name}: {d}")
                if self.get_privacy_sampler_result(name) != pt_private:
                    if d > privacy_criterion:
                        self.privacy_sampler_results[name][user] = pt_private
                    else:
                        self.privacy_sampler_results[name][user] = pt_public

                if self.get_privacy_sampler_result(name) == pt_public:
                    self.log.debug("mp_callback: " + user + ": " + name + ": PUBLIC")
                self.reg_ts(manifold_key, user, name, completed_key, node_ts)

            except Exception as e:
                self.log.debug("manifold privacy " + str(e))

        try:
            del self.jobs[job_name]
        except Exception as e:
            self.log.debug("trying to del job " + str(e))
        self.release()
        if successful_return:
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

    def del_ts(self, n_id, ts):
        for job_key in self.ts.keys():
            for user in self.ts[job_key].keys():
                if n_id in self.ts[job_key][user]:
                    for ts_key in self.ts[job_key][user][n_id].keys():
                        current_ts = self.ts[job_key][user][n_id].get(ts_key, 0)
                        if current_ts < ts:
                            self.ts[job_key][user][n_id][ts_key] = ts

    def add_to_raw_graph(self, name, linked_nodes, h_node, is_prob):
        """
        Adds a node to the inferential graph (i_graph)
        :param name: String, Node name
        :param linked_nodes: Array of Strings, Other linked nodes (depends_on)
        :param h_node: String, hierarchical nodes, if any
        :param is_prob: Boolean, if it's a probabilistic node
        :return:
        """
        # if a re-define
        if (is_prob and (name in self.raw_graph.graph[p_key] or pd_key + name in self.raw_graph.graph[p_key])) or (
                (not is_prob) and name in self.raw_graph.graph[d_key]):
            # delete the existing node before adding
            if is_prob and name in self.raw_graph.graph[d_key]:
                edges = list(self.raw_graph.in_edges(pd_key + name))
                self.raw_graph.remove_edges_from(edges)
            else:
                edges = list(self.raw_graph.in_edges(name))
                self.raw_graph.remove_edges_from(edges)

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
                # for all the depends on pd node, trasfer to the d node
                out_nodes = set(self.raw_graph.successors(pd_key + name))
                for out_node in out_nodes:
                    self.raw_graph.remove_edge(pd_key + name, out_node)
                    self.raw_graph.add_edge(name, out_node)
            else:
                # it might be a normal node that is added as a linked node
                self.raw_graph.nodes[name][attr_is_prob] = is_prob

        # Add the linked nodes as well
        for node in linked_nodes:
            if node not in self.raw_graph.nodes:
                self.raw_graph_add_node(node, False)

        # Adding the edges
        if is_prob:
            if name not in self.raw_graph.graph[p_key]:
                self.raw_graph.graph[p_key].append(name)
            edges = [(a, name) for a in set(linked_nodes)]
            self.raw_graph.add_edges_from(edges)
        else:
            if name not in self.raw_graph.graph[d_key]:
                self.raw_graph.graph[d_key].append(name)
            edges = [(a, name) for a in set(linked_nodes) - {h_node}]
            self.raw_graph.add_edges_from(edges)

        # update i_graph and p_graph
        self.update_graphs()

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
        if name.startswith(pd_key):
            self.raw_graph.nodes[name][attr_pd_node] = name
        else:
            self.raw_graph.nodes[name][attr_pd_node] = None

    def raw_graph_del_node(self, name, is_prob):
        """
        Delete a node from the inferential graph (i_graph), **Yet to implement
        :param name: String, name of the node
        :param is_prob: is probabilistic
        """
        if is_prob and name in self.raw_graph.graph[d_key]:
            name = pd_key + name
        if is_prob:
            self.raw_graph.graph[p_key].remove(name)
        else:
            self.raw_graph.graph[d_key].remove(name)

        in_edges = list(self.raw_graph.in_edges(name))
        out_edges = list(self.raw_graph.out_edges(name))
        p_node = pd_key + name
        # if the deterministic definition of the pd node
        if (not is_prob) and p_node in self.raw_graph.graph[p_key]:
            # add all out edges it currently have to the prob node
            for out_edge in out_edges:
                if out_edge[1] != p_node:
                    self.raw_graph.add_edge(p_node, out_edge[1])
            self.raw_graph.remove_node(name)
            nx.relabel_nodes(self.raw_graph, {p_node: name}, copy=False)
            self.raw_graph_add_node(name, True)
            self.raw_graph.graph[p_key].remove(pd_key + name)
            self.raw_graph.graph[p_key].append(name)
        elif not out_edges:
            self.raw_graph.remove_node(name)
        else:
            self.raw_graph.remove_edges_from(in_edges)
        # remove linked nodes if they are only serving the removed node
        for edge in in_edges:
            if not set(self.raw_graph.in_edges(edge[0])) and not set(self.raw_graph.out_edges(edge[0]))\
             and edge[0] not in self.raw_graph.graph[d_key]:
                self.raw_graph.remove_node(edge[0])

        # update i_graph and p_graph
        self.update_graphs()
        return name

    def update_graphs(self):
        """
        Original raw_graph keeps the nodes in more ground level with more information.
        We generate privacy graph and inferential graph using the raw graph.
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
                node_0_pd = i_graph.nodes[e[0]][attr_pd_node]
                node_1_pd = i_graph.nodes[e[1]][attr_pd_node]
                pd_node = node_0_pd if node_0_pd else node_1_pd
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
                i_graph.nodes[e[0]][attr_pd_node] = pd_node

                edges_to_remove = edge_permutations.intersection(set(i_graph.edges))

        self.i_graph = i_graph

        # Generating modified privacy graph
        p_graph = copy.deepcopy(self.i_graph)

        # have to split the probabilistic nodes
        for node_id, node in self.i_graph.nodes(data=True):
            if node[attr_is_prob]:
                contains = [p for p in node[attr_contains] if (not p.startswith(pd_key) or p != node_id)]
                in_nodes = set(self.i_graph.predecessors(node_id))
                out_nodes = set(self.i_graph.successors(node_id))
                for out_node in out_nodes:
                    p_graph.remove_edge(node_id, out_node)
                for name in contains:
                    if name not in p_graph.nodes:
                        p_graph.add_node(name)
                    p_graph.nodes[name][attr_label] = name
                    p_graph.nodes[name][attr_contains] = [name]
                    p_graph.nodes[name][attr_is_prob] = True
                    p_graph.nodes[name][attr_id] = name
                    p_graph.nodes[name][attr_last_ts] = 0
                    p_graph.nodes[name][attr_color] = 'red'
                    for dep in in_nodes:
                        p_graph.add_edge(dep, name)
                    ori_out_nodes = set(self.raw_graph.successors(name)) & out_nodes
                    for out_node in ori_out_nodes:
                        p_graph.add_edge(name, out_node)
                p_graph.nodes[node_id][attr_contains] = [node_id]

        self.p_graph = p_graph

    def is_node_computable(self, user, node):
        """
        Given the node check if the node is computable based on the inferential graph
        :param user: String
        :param node: node (as in graph)
        :return: Boolean
        """
        is_computable = True
        n_id = node[attr_id]
        if node[attr_is_prob] and not node[attr_pd_node]:
            is_computable = False
        for u in self.i_graph.predecessors(n_id):
            user_edited = user_all if u in self.public else user
            if (u not in self.builtins) and (u not in self.uptodate[user_edited]):
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
                       pd_key + var_name == self.i_graph.nodes[n][attr_pd_node]):
                return self.i_graph.nodes[n]
        return None

    def get_dep_predecessors(self, node_id):
        """
        get dependant predecessors of a given node
        :param node_id: i_graph node
        :return: dependants
        """
        dep_predecessors = set()
        predecessors = set(self.i_graph.predecessors(node_id))
        dep_predecessors = dep_predecessors.union(predecessors)
        for predecessor in predecessors:
            if predecessor in self.functions:
                dep_predecessors = dep_predecessors.union(self.get_dep_predecessors(predecessor))

        return dep_predecessors

    def draw_raw_graph(self, graph_name='raw_graph'):
        """
        Draws the raw graph
        :return: graph as a base 64 string
        """
        return self.draw_graph(self.raw_graph, graph_name)

    def draw_inferential_graph(self, graph_name='inferential_graph'):
        """
        Draws the modified inferential graph
        :return: graph as a base 64 string
        """
        return self.draw_graph(self.i_graph, graph_name)

    def draw_privacy_graph(self, graph_name='privacy_graph'):
        """
        Draws the modified privacy graph
        :return: graph as a base 64 string
        """
        return self.draw_graph(self.p_graph, graph_name)

    def draw_generative_graph(self, graph_name='generative_graph'):
        """
        Draws the modified generative graph
        :return: graph as a base 64 string
        """
        g_graph = copy.deepcopy(self.raw_graph)
        for node_id, node in g_graph.nodes(data=True):
            if node_id.startswith(pd_key):
                ori_id = node_id.replace(pd_key, '')
                in_nodes = set(g_graph.predecessors(node_id))
                for in_node in in_nodes:
                    if in_node == ori_id:
                        g_graph = nx.contracted_edge(g_graph, (in_node, node_id), self_loops=False)

        return self.draw_graph(g_graph, graph_name)

    @staticmethod
    def draw_graph(graph, graph_name):
        """
        Draws the given graph under given name
        :return: graph as a base 64 string
        """
        file_path = graph_folder + '/' + graph_name
        nx.drawing.nx_pydot.write_dot(graph, file_path)
        gv.render('dot', 'png', file_path)
        os.remove(file_path)
        result = "data:image/png;base64, " + base64.b64encode(open(f"{file_path}.png", "rb").read()).decode()
        return result

    # Private commands

    def show_globals(self):
        result = ""
        result += "All: " + str(self.globals["All"].get("r", "Not here")) + "\n"
        for user in self.user_ids:
            result += user + ": " + str(self.globals[user].get("r", "Not here")) + "\n"
        return result


    def show_jobs(self, as_dict=False):
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
        if as_dict:
            result = json.dumps({
                'total_jobs': (compute_jobs + sampler_jobs + manifold_jobs),
                'compute_jobs': compute_jobs,
                'sampler_jobs': sampler_jobs,
                'manifold_jobs': manifold_jobs
            })

        else:
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
            if code in self.sampler_exception[user]:
                result += self.sampler_exception[user][code]
            else:
                result += code + " is not uptodate  "
        elif code not in (self.public | self.unknown_privacy):
            result += code + " is private  "
        elif code not in self.public:
            result += code + " is of unknown privacy  "
        elif type(self.globals[user][code]) == Reference:
            result += code + " is too big to print  "
        else:
            val = self.globals[user][code]
            if type(val) == io.BytesIO:
                result = "data:image/png;base64, " + base64.b64encode(val.getvalue()).decode()
            elif type(val) == numpy.ndarray:
                result = list(val)                
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

    def add_comment(self, name, the_comment):
        self.comment[name] = the_comment

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
                 'All'].get(name) == st_not_retained:
                    res += st_not_retained
                else:
                    res += "Privacy Unknown"
            elif name in self.uptodate["All"]:
                if type(self.globals["All"][name]) == io.BytesIO:  # write image to file
                    res += "[PNG Image]"
                elif type(self.globals["All"][name]) == Reference:
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
                raise PrivateGraphException(f"Exception: {name} is not stale, computing, exception or uptodate.")
        elif name in self.builtins:
            if name in self.public:
                if long_format:
                    res += str(self.globals["All"][name])
                else:
                    res += reprlib.repr(self.globals["All"][name])
            else:
                res += "Private"
        else:
            raise PrivateGraphException("Exception: Unknown variable in getValue " + name)
        return res

    def show_values(self):
        value_width = 120
        value_bits = []
        for name in self.code.keys():
            value_bits.append(name + " = " + self.get_value(name)[0:value_width])
        for name in self.prob_code.keys():
            if name in self.sampler_exception:
                value_bits.append(name + " ~ " + self.sampler_exception[name])
            else:
                value_bits.append(name + " ~ " + self.get_value(name)[0:value_width])
        return "\n".join(value_bits)

    def show_code(self):
        code_bits = []
        for name in self.code.keys():
            if name in self.functions:
                code_bits.append(self.eval_code[name].replace("\t", "    "))
            else:
                code_bits.append(name + " = " + str(self.code[name]))
        for name in self.prob_code.keys():
            if name in self.hierarchical:
                code_bits.append(name + "[" + self.hierarchical[name] + "] ~ " + str(self.prob_code[name]))
            else:
                code_bits.append(name + " ~ " + str(self.prob_code[name]))
        if len(code_bits) > 0:
            comment_bits = []
            for name in self.code.keys():
                comment_bits.append(self.comment.get(name, ""))
            for name in self.prob_code.keys():
                comment_bits.append(self.comment.get(name, ""))
            return "\n".join(
                "  ".join([code_bit, comment_bit]) for code_bit, comment_bit in zip(code_bits, comment_bits))
        else:
            return ""

    def show_eval_code(self):
        code_bits = []
        for name in self.code.keys():
            code_bits.append(name + " = " + str(self.eval_code[name]))
        for name in self.prob_code.keys():
            code_bits.append(name + " ~ " + str(self.py_mc3_code[name]))
        if len(code_bits) > 0:
            comment_bits = []
            for name in self.code.keys():
                comment_bits.append(self.comment.get(name, ""))
            for name in self.prob_code.keys():
                comment_bits.append(self.comment.get(name, ""))
            return "\n".join(
                "  ".join([code_bit, comment_bit]) for code_bit, comment_bit in zip(code_bits, comment_bits))
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
            if name in self.dependson and self.dependson[name] != set([]):
                res += "    " + repr(list(self.dependson[name]))
            res += "\n"
        for name in self.prob_code.keys():
            if name in self.hierarchical:
                res += name + "[" + self.hierarchical[name] + "] ~ "
            else:
                res += name + " ~ "
            if name not in self.private:
                res += self.prob_code[name][0:60]
            else:
                res += "Private"
            if name in self.probdependson and self.probdependson[name] != set([]):
                res += "    " + repr(list(self.probdependson[name]))
            res += "\n"
        return res[0:-1]

    def show_pymc3_code(self):
        pymc3_code = ''
        for node_id, node in self.i_graph.nodes(data=True):
            if node[attr_is_prob]:
                pymc3_code = pymc3_code + self.construct_pymc3_code(node, user_all)[1]
        return pymc3_code

    def show_variables(self, pattern):
        code_bits = []
        code_width = 50
        value_width = 80
        for name in [c for c in self.code.keys() if pattern.lower() in c.lower()]:
            code_bits.append(name + " = " + str(self.code[name]))
        for name in [pc for pc in self.prob_code.keys() if pattern.lower() in pc.lower()]:
            if name in self.hierarchical:
                code_bits.append(name + "[" + self.hierarchical[name] + "] ~ " + str(self.prob_code[name]))
            else:
                code_bits.append(name + " ~ " + str(self.prob_code[name]))
        if len(code_bits) > 0:
            m = max(len(line) for line in code_bits)
            m = min(m, code_width)
            newcodebits = [line[0:code_width].ljust(m, " ") for line in code_bits]
            value_bits = []
            for name in self.code.keys():
                value_bits.append(self.get_value(name)[0:value_width])
            for name in self.prob_code.keys():
                if name in self.sampler_exception:
                    value_bits.append(self.sampler_exception[name])
                else:
                    value_bits.append(self.get_value(name)[0:value_width])
            comment_bits = []
            for name in self.code.keys():
                comment_bits.append(self.comment.get(name, ""))
            for name in self.prob_code.keys():
                comment_bits.append(self.comment.get(name, ""))
            unsatisfied_depends = []
            for name in self.code.keys():
                unsatisfied_depends.append(
                    ", ".join(self.dependson[name] - (self.deterministic | self.probabilistic | self.builtins)))
            for name in self.prob_code.keys():
                unsatisfied_depends.append(
                    ", ".join(self.probdependson[name] - (self.deterministic | self.probabilistic | self.builtins)))
            return "\n".join("  ".join([codebit, valuebit, commentbit, unsatisfied_depend]) for
                             codebit, valuebit, commentbit, unsatisfied_depend in
                             zip(newcodebits, value_bits, comment_bits, unsatisfied_depends))
        else:
            return ""

    def show_variables_dict(self):
        value_width = 80

        defaults = ['Events', 'DemoEvents']
        names = defaults + list((self.probabilistic | self.deterministic) - self.builtins)
        sv = {}
        for name in names:
            sv[name] = {'name': name}
            if name in self.sampler_exception:
                sv[name]['value'] = self.sampler_exception[name]
            else:
                sv[name]['value'] = self.get_value(name)[0:value_width]

            sv[name]['comment'] = self.comment.get(name, "")
            if name in self.code:
                sv[name]['unsatisfied'] = ", ".join(
                    self.dependson[name] - (self.deterministic | self.probabilistic | self.builtins))
            elif name in self.prob_code:
                sv[name]['unsatisfied'] = ", ".join(
                    self.probdependson[name] - (self.deterministic | self.probabilistic | self.builtins))
            else:
                sv[name]['unsatisfied'] = ""

        return json.dumps(sv)

    def test_variables_dict(self):

        untested_variables = {'NumberOfSamples', 'NumberOfTuningSamples', 'NumberOfChains', 'rhat', 'ess', 'loo',
                              'waic'}
        names = list((set(self.globals[user_all].keys()) - self.builtins) - untested_variables)
        sv = OrderedDict()
        for name in sorted(names):
            if name in self.sampler_exception:
                sv[name] = self.sampler_exception[name]
            else:
                sv[name] = self.get_value(name, long_format=True)

        return json.dumps(sv)


def job(job_name, node, user, code, globals, locals, user_func, project_id, shell_id):
    name = node[attr_id]
    redis_key = redis_helper.get_redis_key(user, name, project_id, shell_id)
    name_long = int("".join(map(str, [ord(c) for c in name])))
    # 4294967291 seems to be the largest prime under 2**32 (int limit)
    seed = name_long % 4294967291
    numpy.random.seed(seed)
    s3_var_globals = retrieve_redis_vars(globals)
    for func in user_func:
        try:
            exec(func, s3_var_globals)
        except Exception as e:
            e = PrivateGraphException("Error in User Function: " + func[4:10] + "...")
            return job_name, name, user, e
    try:
        if code.startswith("def"):
            value = "User Function"
        else:
            value = eval(code, s3_var_globals, locals)
        if get_size(value) > 1e6:
            value = Reference(redis_key, value)

        return job_name, node, user, value
    except Exception as e:
        return job_name, node, user, e


def sampler_job(job_name, user, node, code, globals, locals):
    numpy.random.seed(Private.config.numpy_seed)
    try:
        s3vars = retrieve_redis_vars(globals)
        s3_var_locals = retrieve_redis_vars(locals)
        exec(code, s3vars, s3_var_locals)
        value, exception_variable, model = s3_var_locals["__private_result__"]
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


def mp_job(job_name, node, name, user, user_array, all_array):
    """
    Calculates the manifold privacy

    :param job_name: job identifier
    :param node: i_graph node
    :param name: name of the variable
    :param user: user
    :param user_array: user removed data
    :param all_array: all data
    :return: d
    """
    from Private.manifoldprivacy import dist_manifold
    d = dist_manifold(user_array, all_array) * 100.
    return job_name, node, name, user, d


def get_size(obj, seen=None):
    """
    Returns the size of the give object recursively(used to decide on caching)

    :param obj: object which require the size calculation
    :param seen: already visited nodes
    :return: size of the object in bytes
    """
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


def retrieve_redis_vars(var_dict):
    """
    Replace all the redis references in a variable dictionary with actual value

    :param var_dict: dictionary of variables
    :return: dictionary of variables with values replaced
    """
    ret_dict = {}
    for key in var_dict.keys():
        if type(var_dict[key]) == Reference:
            ret_dict[key] = var_dict[key].value()
        else:
            ret_dict[key] = var_dict[key]

    return ret_dict
