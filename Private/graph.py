from __future__ import print_function
from __future__ import absolute_import

import copy
import hashlib
import multiprocessing
import reprlib
import sys

import numpy
import numpy.random
from collections import OrderedDict, deque
import logging
import matplotlib.pyplot as plt
import networkx as nx
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

PrivacyCriterion = 10.0   # percent
display_precision = 3


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
            self.userids = set(user_ids)
            self.globals = setGlobals2(user_ids)
        else:
            self.globals = setGlobals(events=events, proj_id=self.project_id, shell_id=self.shell_id, load_demo_events=self.load_demo_events)
            self.userids = setUserIds(events=events)
            debug_logger(["user_ids", self.userids])

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
        self.privacySamplerResults = {} # this holds results from privacy samplers so we know the difference between when
                                        # the privacy samplers haven't been run since last compute and when they have been run
        self.numberOfManifoldPrivacyProcessesComplete = {}

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
        self.check_ppserver_connection()

        #if not ppservers:
        #    # Running locally, let ncpus default to the number of system processors
        #    self.server = pp.Server(ppservers=ppservers, restart=True, socket_timeout = local_socket_timeout)
        #else:
        #    # Set ncpus to 0 so that we only process on remote machines
        #    self.server = pp.Server(ncpus=0, ppservers=ppservers, restart=True, socket_timeout = remote_socket_timeout)

        #print "Starting pp with", self.server.get_ncpus(), "workers"
        #self.nxgraph = nx.DiGraph()
        self.SamplerParameterUpdated = False

        setBuiltinPrivacy(self) # set privacy of builtins

        if user_ids:
            self.define("Events", "", evalcode="getEvents(project_id, user_id)", dependson=["getEvents"])
            if self.load_demo_events:
                self.define("DemoEvents", "", evalcode="getDemoEvents(project_id, user_id)", dependson=["getDemoEvents"])


    def check_ppserver_connection(self):

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
        result = "%d jobs\n" % len(self.jobs)
        for k,v in self.jobs.items():
            result += k + "\n"
        return result

    def checkprivacyup(self, name):
        if name in self.public:
            return True
        elif name in self.private:
            return False
        else:
            parents = self.getParents(name)
            if parents == set():
                return True
            else:
                return all(self.checkprivacyup(parent) for parent in parents)

    def checkprivacydown(self, name):
        if name in self.public:
            return True
        elif name in self.private:
            return False
        else:
            children = self.getChildren(name)
            if children == set():
                return True
            else:
                return all(self.checkprivacydown(child) for child in children)

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

    def compute_privacy(self, sub_graphs):

        self.acquire("computePrivacy")

        # set all variables except builtins to unknown_privacy
        self.set_all_unknown(sub_graphs)

        self.computeGraphPrivacy()
        self.computeProbabilisticPrivacy()
        self.computeGraphPrivacy()
        self.release()

    def computeGraphPrivacy(self):

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

    def computeProbabilisticPrivacy(self):

        # check the privacySamplerResults to see if we can fill in variables
        # only do this if we don't know the privacy already as we don't want to overwrite the values calculated directly from the graph

        for name in self.deterministic | self.probabilistic:
            if name in self.unknown_privacy:
                #self.log.debug( "looking at privacySamplerResults: " + name)
                #self.log.debug( "unknown: " + str(self.unknown_privacy))
                if name in self.privacySamplerResults.keys():
                    self.setPrivacy(name, self.privacySamplerResults[name])


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

    def set_all_unknown(self, sub_graphs):

        # set all variables except builtins to unknown privacy
        for sub_graph in sub_graphs.values():
            for name in (sub_graph & (self.deterministic | self.probabilistic)):
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

    def define(self, name, code, evalcode=None, dependson=None, prob = False, hier = None, pyMC3code = None):
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
            if dependson != []:
                self.probdependson[name] = set(dependson)
            for n in (self.probabilistic - self.deterministic) & self.get_sub_graph(name):
                for user in self.userids:
                    self.changeState(user, n, "stale")
            if hier:
                self.hierarchical[name] = hier
        else:
            self.deterministic.add(name)
            self.code[name] = code
            self.evalcode[name] = evalcode
            self.dependson[name] = set(dependson)
            for user in self.userids:
                self.changeState(user, name, "stale")
        self.release()
        self.compute_privacy(self.get_sub_graphs(name)) # need computePrivacy before compute so we don't compute public variables for each participant
        self.compute(self.get_sub_graphs(name))
        self.compute_privacy(self.get_sub_graphs(name)) # every definition could change the privacy assignments

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
        self.compute_privacy(self.get_sub_graphs(name))  # need computePrivacy before compute so we don't compute public variables for each participant
        self.compute(self.get_sub_graphs(name))
        self.compute_privacy(self.get_sub_graphs(name))

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
            res = ""
        else:
            res = name + " not found."

        self.release()
        self.compute_privacy(self.get_sub_graphs(name)) # every delete could change the privacy assignments
        return res

#  def has_descendants(self, name):
#      # Checks if a node given by 'name' has any descendants
#      for var in self.dependson.keys():
#          if name in self.dependson[var]:
#              return True
#      return False

#  def check_cycles(self, name, dependson):
#      # Checks to see if a new 'define' command will create a cycle in the graph
#      existing_vars = self.dependson.keys()
#      if name in dependson:
#          return True
#      elif name not in existing_vars:
#          return False
#      else:
#          deps = [dep for dep in dependson if dep in existing_vars]
#          if (len(deps) == 0):
#              return False
#          else:
#              # Incomplete
#              return True

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


    def isAncestor(self, name1, name2):
        parents = self.getParents(name2)
        if parents == set():
            return False
        elif name1 in parents:
            return True
        else:
            return any(self.isAncestor(name1, parent) for parent in parents)

    def draw_dependency_graph(self):
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
        plt.axis('off')
        plt.savefig(buf, format="png")
        plt.show()
        result = "data:image/png;base64, " + base64.b64encode(buf.getvalue())
        plt.close()
        return result

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
                    _log.debug(self.node)
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

    def generate_graph(self):
        """
        Generates a directed graph from the available variables

        :return: Returns a networkX graph
        """
        g = nx.DiGraph()
        visited, stack = set(), list(self.probabilistic | self.deterministic)
        while stack:
            vertex = stack.pop()
            g.add_node(vertex)
            if vertex not in visited:
                visited.add(vertex)
                for k in self.dependson.get(vertex, set()) | self.probdependson.get(vertex, set()):
                    g.add_edge(vertex, k)
                    stack.append(k)
        return g

    def get_all_sub_graphs(self, nodes_subset=None):
        """
        Identified disconnected probabilistic sub graphs.

        :return: Dictionary of sub graphs sub_graph_id: list of node names
        """
        var_graph = self.generate_graph()
        nodes = nodes_subset if nodes_subset else var_graph.nodes
        sub_graph_id = 0
        node_state = {}
        sub_graphs = {}
        not_visited, visited = 0, 1

        for node in nodes:
            node_state[node] = not_visited

        def get_connected(n, graph_id):
            if node_state[n] == not_visited:
                sub_graphs[graph_id].add(n)
                node_state[n] = visited
                descendants = nx.algorithms.descendants(var_graph, n)
                ancestors = nx.algorithms.ancestors(var_graph, n)

                for c in set(descendants) | set(ancestors):
                    if c not in self.builtins:
                        sub_graphs[graph_id].add(c)
                    if c in self.probabilistic:
                        if c not in node_state:
                            node_state[c] = not_visited
                        get_connected(c, graph_id)

        for node in nodes:
            if node_state[node] != visited and node in (self.probabilistic - self.deterministic):
                sub_graphs[sub_graph_id] = set()
                get_connected(node, sub_graph_id)
                sub_graph_id += 1

        return_sub_graphs = {}
        for key, value in sub_graphs.items():
            return_sub_graphs[self.get_graph_id(value)] = value

        return return_sub_graphs

    def get_sub_graphs(self, node):
        """
        Return all the sub graphs where the variable is present

        :param node: name of the variable, string
        :return: dictionary of sub graphs
        """
        sub_graphs = self.get_all_sub_graphs()
        result_dict = {}
        for sub_graph_id, sub_graph in sub_graphs.items():
            if node in sub_graph:
                result_dict[sub_graph_id] = sub_graph
        return result_dict

    def get_sub_graph(self, node):
        """
        Returns the first sub graph for the given node (name), can be sued for probabilistic variables

        :param node: node (name of a variable)
        :return: set of nodes (strings)
        """
        sub_graphs = self.get_sub_graphs(node)
        for sub_graph_id, sub_graph in sub_graphs.items():
            if node in sub_graph:
                return sub_graph
        return set()

    def is_sub_graph_complete(self, user, sub_graph):
        """
        Check if all required dependencies of the sub graph is up-to-date

        :param user: user name
        :param sub_graph: list of variables
        :return: boolean
        """
        result = True
        for name in sub_graph & self.probabilistic:
            if name not in self.uptodate[user]:
                result = result and self.checkdown(user, name)
                result = result and self.checkup(user, name)
            elif name in self.deterministic & self.probabilistic:
                result = result and self.checkdown(user, name)
        return result

    @staticmethod
    def get_graph_id(nodes):
        """
        Get a ID for the custer based on the nodes
        :param nodes: set of variables in the cluster
        :return: string
        """
        hash_object = hashlib.sha384(str(nodes).encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        return hex_dig

    def sub_graph_job_count(self, sub_graph_id, sub_graph):
        """
        Counts the number of active jobs for a given sub graph. This is tightly coupled to the job name (which is not
        good) and job names should not be changed without changing this function
        :param sub_graph_id: generated ID
        :param sub_graph: set() of variable names
        :return: count (int)
        """
        job_count = 0
        for job_names in self.jobs.keys():
            if job_names.endswith(str(sub_graph_id)):
                job_count += 1
            else:
                for node in sub_graph:
                    if job_names.endswith(node):
                        job_count += 1

        return job_count

    def constructPyMC3code(self, user=None, sub_graph=set()):
        #try:
            locals = {}
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

    
    basic_model = pymc3.Model()

    
    with basic_model:

"""
            # Examples
            # mu = alpha + beta[0]*X1 + beta[1]*X2
            # sigma = pm.HalfNormal('sigma', sd=1)
            # Y_obs = pm.Normal('Y_obs', mu=mu, sd=sigma, observed=Y)

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

        #except Exception as e:
        #    self.log.debug("In constructMCcode user = " + str(user) + " " + str(e.args))
        #    if user:
        #      self.log.debug("In constructMCcode user = " + str(user) + " " + str(self.globals[user]))


    def canRunSampler(self, user, verbose=False):
        if len(self.probabilistic) == 0:
            return False
        result = True
        if verbose:
            output = ""
        for name in self.probabilistic:
            if name in self.uptodate[user]:
                if verbose: output += name + " is up to date\n"
            else:
                if verbose: output += name + " checkdown " + str(self.checkdown(user, name)) + "\n"
                result = result and self.checkdown(user, name)
                if verbose: output += name + " checkup " + str(self.checkup(user, name)) + "\n"
                result = result and self.checkup(user, name)
        if verbose:
            return output
        else:
            return result

    def variablesToBeSampled(self):

        names = self.probabilistic - self.deterministic
        return names

    def variablesToBeCalculated(self, user):
        names = set([])
        for name in self.deterministic & self.stale[user]:
            if self.dependson.get(name, set([])) - self.uptodate[user] - self.builtins == set([]):
                names.add(name)
        return(names)

    def compute(self, sub_graphs):
        # Need to reconnect if we are close to the tcp_keep_alive timout
        # otherwise OS will dropout connection
        self.check_ppserver_connection()

        self.log.debug("In compute") 
        self.acquire("compute")
        debug_logger("in compute")
        try:
            for user in self.userids:
                for name in self.variablesToBeCalculated(user):
                    if name not in self.public or user == "All":
                        jobname = "Compute:  " + user + " " + name
                        if jobname not in self.jobs:
                            self.changeState(user, name, "computing")
                            self.log.debug("Calculate: " + user + " " + name + " " + self.code[name])
                            debug_logger("Calculate: " + user + " " + name + " " + self.code[name])
                            
                            user_func = [self.evalcode[func_name] for func_name in self.functions]
                            self.jobs[jobname] = self.server.submit(job, jobname, name, user, self.evalcode[name], self.get_globals(set([name]), user), self.locals, user_func, self.project_id, self.shell_id)
                            self.jobs[jobname].add_done_callback(self.callback)

            for sub_graph_id, sub_graph in sub_graphs.items():
                if self.sub_graph_job_count(sub_graph_id, sub_graph) == 0: # don't start a sampler until all other jobs have finished
                    sampler_names = self.variablesToBeSampled()
                    self.log.debug("sampler names: " + str(sampler_names))
                    for user in self.userids:
                        if user == "All" or sampler_names - self.public != set():
                            if self.SamplerParameterUpdated or (sampler_names & self.stale[user] != set([])):
                                self.privacySamplerResults = {} # remove all privacy sampler results as they are now stale
                                self.numberOfManifoldPrivacyProcessesComplete = {} # remove all counts too
                                if self.is_sub_graph_complete(user, sub_graph):
                                    sampler_names = sub_graph - self.deterministic
                                    if sampler_names & self.uptodate[user] == sampler_names:
                                        continue
                                    for name in sampler_names:
                                        self.changeState(user, name, "computing")
                                        if name in self.globals[user]:
                                            self.globals[user][name] = None  # remove any previous samples that have been calculated
                                    self.samplerexception[user] = {}

                                    jobname = "Sampler:  " + user + ", " + str(sub_graph_id)
                                    locals, sampler_code = self.constructPyMC3code(user, sub_graph)
                                    self.jobs[jobname] = self.server.submit(samplerjob, jobname, user, sampler_names, sampler_code, self.get_globals(sampler_names, user), locals, self.project_id, resources={'process': 1})
                                    self.jobs[jobname].add_done_callback(self.samplercallback)
                        self.SamplerParameterUpdated = False
        except Exception as e:
            print("in compute " + str(e))
            traceback.print_exc()
        self.release()

    def callback(self, returnvalue):
        returnvalue = returnvalue.result()
        self.acquire("callback")
        debug_logger("In callback")
        jobname, name, user, value = returnvalue
        try:
            if isinstance(value, Exception):
                if user == "All":
                    debug_logger(["callback Exception", user, name, value])
                    self.globals[user][name] = str(value)
                    self.changeState(user, name, "exception")
            else:
                self.globals[user][name] = value
                self.changeState(user, name, "uptodate")
                if user == "All":
                    if name in config_builtins:
                        builtins.get(name)(value)
                    if name in ["NumberOfSamples", "NumberOfChains", "NumberOfTuningSamples"]:
                        self.SamplerParameterUpdated = True
                    if type(value) == io.BytesIO:   # write image to file
                        value.seek(0)
                        with open(name+'.png', 'wb') as f:
                            shutil.copyfileobj(value, f)
            if jobname in self.jobs:
                del self.jobs[jobname]
            else:
                self.log.debug("Trying to delete job %s that is not in self.jobs" % jobname)
                self.log.debug(self.jobs)
        except Exception as e:
            self.log.debug(str(e))

        self.release()
        self.compute_privacy(self.get_sub_graphs(name))
        self.compute(self.get_sub_graphs(name))
        self.compute_privacy(self.get_sub_graphs(name))

    def haveSamples(self, user):
        # have to allow for possibility that some probabilistic variables are not retained and therefore won't have samples
        # so see if any of the probabilistic variables have samples
        return any(isinstance(self.globals[user].get(aname, None), numpy.ndarray) for aname in self.probabilistic)

    def samplercallback(self, returnvalue):
        returnvalue = returnvalue.result()
        numpy.random.seed(numpy_seed)
        self.acquire("samplercallback")

        myname, user, names, value, exception_variable, stats = Private.s3_helper.read_results_s3(
            returnvalue) if Private.config.s3_integration else returnvalue
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
                    value = str(int(m.group(1))-1) + " arguments required."
                self.samplerexception[user][exception_variable] = str(value)
            else:
                for name in names:
                    self.samplerexception[user][name] = str(value)
            self.log.debug("Exception in sampler callback %s %s ...done" % (user, str(value)))
        else: # successful sampler return
            try:
                self.log.debug("samplercallback: name in names ")
                for name in names:
                    if name in value.varnames:
                        self.globals[user][name] = numpy.random.permutation(value[name]) # permute to break the joint information across variables
                    else:                                                                # manifold privacy is applied to individual variables
                        self.globals[user][name] = "Not retained."                       # so there could be more information in the joint information
                    self.changeState(user, name, "uptodate")

                self.log.debug("samplercallback: name in names ...done ")

                whichsamplersarecomplete = [u for u in self.userids if u != "All" and self.haveSamples(u)]
                if user == "All" and stats is not None: # if this is All then initiate comparisons with all of the users that have already returned
                    for stat_key in stats["rhat"]:
                        self.globals[user]['rhat'][stat_key] = stats["rhat"][stat_key]
                        self.globals[user]['ess'][stat_key] = stats["ess"][stat_key]
                        self.globals[user]['waic'][stat_key] = stats["waic"]
                        self.globals[user]['loo'][stat_key] = stats["loo"]
                    for u in whichsamplersarecomplete:
                        # go through variables if we already know they are private do nothing else initiate manifold privacy calculation
                        for name in value.varnames:
                            if self.privacySamplerResults.get(name, None) != "private":
                                if name in self.globals[u].keys() and name in self.globals["All"].keys():
                                     if self.globals[u][name].shape != self.globals["All"][name].shape: # if shape is affected by dropping a user then this variable is private
                                          self.privacySamplerResults[name] = "private"
                                     else:
                                          jobname = "Manifold: " + u + " " + name
                                          self.jobs[jobname] = self.server.submit(manifoldprivacyjob, jobname, name, u, self.globals[u][name], self.globals["All"][name])
                                          self.jobs[jobname].add_done_callback(self.manifoldprivacycallback)

                else: # else compare All to this users samples using manifold privacy calculation
                    self.log.debug("samplercallback: whichsamplersarecomplete - Users ")
                    if self.haveSamples("All"):
                        # go through variables if we already know they are private do nothing else initiate manifold privacy calculation
                        for name in value.varnames:
                            if self.privacySamplerResults.get(name, None) != "private":
                                if name in self.globals[user].keys() and name in self.globals["All"].keys():
                                    if self.globals[user][name].shape != self.globals["All"][name].shape: # if shape is affected by dropping a user then this variable is private
                                        self.privacySamplerResults[name] = "private"
                                    else:
                                        jobname = "Manifold: " + user + " " + name
                                        self.jobs[jobname] = self.server.submit(manifoldprivacyjob, jobname, name, user, self.globals[user][name], self.globals["All"][name])
                                        self.jobs[jobname].add_done_callback(self.manifoldprivacycallback)
                                else:
                                    # Some variables (e.g., logs of SDs) are returned from the sampler, but are not variables in our code.
                                    pass
            except Exception as e:
                self.log.debug("in samplercallback when assigning values " + str(e))

        self.log.debug("samplercallback: delete jobs ")

        try:
            del self.jobs[myname]
        except Exception as e:
            self.log.debug("trying to del job " + str(e))

        self.log.debug("samplercallback: delete jobs ...done")

        self.release()
        self.compute_privacy(self.get_all_sub_graphs(names))
        self.compute(self.get_all_sub_graphs(names))
        self.compute_privacy(self.get_all_sub_graphs(names))

    def manifoldprivacycallback(self, returnvalue):
        returnvalue = returnvalue.result()
        sample_size = self.globals['All']['NumberOfSamples'] * self.globals['All']['NumberOfChains']
        step_size = max(int(sample_size / Private.config.max_sample_size), 1)
        self.acquire("manifoldprivacycallback")
        jobname, name, user, d = returnvalue
        try:
            self.log.debug(user + ": " + name + ": " + str(d) + " " + str(d < PrivacyCriterion))
            self.numberOfManifoldPrivacyProcessesComplete[name] = self.numberOfManifoldPrivacyProcessesComplete.get(name, 0) + 1
            if self.privacySamplerResults.get(name, None) != "private":
                if d > PrivacyCriterion:
                    self.privacySamplerResults[name] = "private"
                    self.globals['All'][name] = self.globals['All'][name][::step_size][:Private.config.max_sample_size] ## 
                    self.log.debug(user + ": " + name + ": " + str(d) + " " + str(d < PrivacyCriterion) + ": PRIVATE")
                else: 
                    self.log.debug(user + ": " + name + ": " + str(d) + " " + str(d < PrivacyCriterion) + ": UNKNOWN_PRIVACY")
                    self.privacySamplerResults[name] = "unknown_privacy"
        
            # if we have all manifold processes back and there are variables that have not been set to private they are public
            #for variable in self.numberOfManifoldPrivacyProcessesComplete.keys():
            #    if self.numberOfManifoldPrivacyProcessesComplete[variable] == len(self.userids) -1: # -1 because we don't have results for All
            #        if self.privacySamplerResults[variable] != "private":
            #            self.privacySamplerResults[variable] = "public"
            #            if len(self.globals['All'][variable]) > Private.config.max_sample_size:
            #                self.globals['All'][variable] = self.globals['All'][variable][::step_size][
            #                                                :Private.config.max_sample_size]

            if self.numberOfManifoldPrivacyProcessesComplete[name] == len(self.userids) -1: # -1 because we don't have results for All
                if self.privacySamplerResults[name] != "private":
                    self.privacySamplerResults[name] = "public"
                    self.globals['All'][name] = self.globals['All'][name][::step_size][:Private.config.max_sample_size]
                    self.log.debug(user + ": " + name + ": PUBLIC")

        except Exception as e:
            self.log.debug("manifold privacy " + str(e))
            print("manifold privacy " + str(e))
        
        try:
            del self.jobs[jobname]
        except Exception as e:
            self.log.debug("trying to del job " + str(e))
        self.release()
        self.compute_privacy(self.get_sub_graphs(name))

    def showSamplerResults(self):
        res = str(len(self.privacySamplerResults)) + " results\n"
        for k,v in self.privacySamplerResults.items():
            if k in self.numberOfManifoldPrivacyProcessesComplete:
                res += k + ": " + v + " " + str(self.numberOfManifoldPrivacyProcessesComplete[k]) + "\n"
            else:
                res += k + ": " + v + "\n"
        return res

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


def job(jobname, name, user, code, globals, locals, user_func, proj_id, shell_id):
    redis_key = redis_helper.get_redis_key(user, name, proj_id, shell_id)
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
            return ((jobname, name, user, e))
    try:
        if code.startswith("def"):
            value = "User Function"
        else:
            debug_logger(["job eval", code])
            value = eval(code, s3_var_globals, locals)
        if get_size(value) > 1e6:
        #if True:
            value = RedisReference(redis_key, value)

        return (jobname, name, user, value)
    except Exception as e:
        return((jobname, name, user, e))


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


def samplerjob(jobname, user, names, code, globals, locals, proj_id):
    numpy.random.seed(Private.config.numpy_seed)
    try:
        exec (code, retrieve_s3_vars(globals), locals)
        value, exception_variable, model = locals["__private_result__"]
        stats = None
        if user == "All":  # if this is All then initiate comparisons with all of the users that have already returned
            stats = {
                "rhat": pm.stats.rhat(value),
                "ess": pm.stats.ess(value),
                "waic": pm.stats.waic(value, model),
                "loo": pm.stats.loo(value, model)
            }
        data = (jobname, user, names, value, exception_variable, stats)
        return data
    except Exception as e:
        # This doesn't seem to be the right size, should be 6 items
        return (jobname, user, names, e, "No Exception Variable", None)

def manifoldprivacyjob(jobname, name, user, firstarray, secondarray):
    from Private.manifoldprivacy import distManifold
    d = distManifold(firstarray, secondarray) * 100.
    return jobname, name, user, d


def getJobId(jobname, user, names, code, globals, locals):
    # todo generate a unique id for the job
    folder_name = "results"
    return folder_name + "/" + str(uuid.uuid4())


def retrieve_s3_vars(var_dict):
    ret_dict = {}
    for key in var_dict.keys():
        if type(var_dict[key]) == RedisReference:
            ret_dict[key] = var_dict[key].value()
        else:
            ret_dict[key] = var_dict[key]

    return ret_dict


