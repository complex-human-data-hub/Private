import multiprocessing
import pp
import reprlib
import numpy
import numpy.random
from collections import OrderedDict, deque
import logging
from Private.builtins import builtins, prob_builtins, setBuiltinPrivacy, setGlobals, setUserIds
import copy
from Private.manifoldprivacy import distManifold
import shutil
import io
import re
import traceback
import pprint
import dill as pickle
import os
import base64
import time

from config import ppservers

logging.basicConfig(filename='private.log',level=logging.WARNING)

numpy.set_printoptions(precision=3)

PrivacyCriterion = 5.0   # percent

def ppset(s):
    """
    Pretty print a set.
    """
    s = list(s)
    s.sort()
    return " ".join(s)

class graph:

    def __init__(self):

        # variable types

        self.deterministic = set()
        self.probabilistic = set()
        self.builtins = set(builtins.keys()) | prob_builtins

        # dependencies

        self.dependson = {} # deterministic dependencies
        self.probdependson = {} # probabilistic dependencies

        # variables related to values

        self.globals = setGlobals()
        self.userids = setUserIds()
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
        #self.sampler_chains = {}
        self.privacySamplerResults = {} # this holds results from privacy samplers so we know the difference between when
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

        if not ppservers:
            # Running locally, let ncpus default to the number of system processors
            self.server = pp.Server(ppservers=ppservers, restart=True, socket_timeout = 400000)
        else:
            # Set ncpus to 0 so that we only process on remote machines
            self.server = pp.Server(ncpus=0, ppservers=ppservers, restart=True, socket_timeout = 400000)

        print "Starting pp with", self.server.get_ncpus(), "workers"
        self.log = logging.getLogger("Private")
        #self.nxgraph = nx.DiGraph()
        self.SamplerParameterUpdated = False
        setBuiltinPrivacy(self) # set privacy of builtins

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
        result += "uptodate: "+ ppset(self.uptodate) + "\n"
        result += "computing: "+ ppset(self.computing) + "\n"
        result += "exception: "+ ppset(self.exception) + "\n"
        result += "stale: "+ ppset(self.stale) + "\n"
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

    def eval_command_line_expression(self, code, dependson, user = "All"):
        # determine status of all dependencies to see whether to evaluate

        result = ""

        # look for undefined

        undefined = set(dependson) - self.deterministic - self.probabilistic - self.builtins
        if len(undefined) == 1:
            result += list(undefined)[0] + " is undefined  "
        elif len(undefined) > 1:
            result += ", ".join(list(undefined)) + " are undefined  "

        # look for not uptodate

        notuptodate = set(dependson) - undefined - self.uptodate[user]
        if len(notuptodate) == 1:
            result += list(notuptodate)[0] + " is not uptodate  "
        elif len(notuptodate) > 1:
            result += ", ".join(list(notuptodate)) + " are not uptodate  "

        # look for private

        private = set(dependson) - undefined - notuptodate - self.public - self.unknown_privacy
        if len(private) == 1:
            result += list(private)[0] + " is private  "
        elif len(private) > 1:
            result += ", ".join(list(private)) + " are private  "

        # look for privacy unknown

        unknown_privacy = set(dependson) - undefined - notuptodate - private - self.public
        if len(unknown_privacy) == 1:
            result += list(unknown_privacy)[0] + " is of unknown privacy"
        elif len(unknown_privacy) > 1:
            result += ", ".join(list(unknown_privacy)) + " are of unknown privacy"

        # if they are all empty then evaluate the expression

        if undefined == set() and notuptodate == set() and private == set() and unknown_privacy == set():
            val = eval(code, self.globals[user], self.locals)
            if type(val) == io.BytesIO:
                #res += reprlib.repr(val)
                result = "data:image/png;base64, " + base64.b64encode(val.getvalue())
            else:
                result = str(val)

        return result

    def checkPickling(self):
        for key, value in self.globals["All"].items():
            try:
                f = open(os.devnull, "w")
                pickle.dump(value, f)
            except:
                print "Pickle error with: ", key
                traceback.print_exc()

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

    def computePrivacy(self):

        self.acquire("computePrivacy")

        # set all variables except builtins to unknown_privacy
        self.setAllUnknown()

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
                    #self.log.debug( "check above and below " + name)
                    if self.checkPrivacyUp(name) and self.checkPrivacyDown(name):
                        #self.log.debug( name + " is public")
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
                #print name, " det ", self.deterministicParents(name)
                if parent not in self.stale[user]:
                    self.changeState(user, parent, "stale")
            for child in self.probabilisticChildren(name): # children via probabilistic links
                #print name, " prob ", self.deterministicParents(name)
                if child not in self.stale[user] and child not in self.builtins:
                    self.changeState(user, child, "stale")
        else:
            raise Exception("Unknown state %s in changeState" % newstate)

    def setAllPublic(self):
        self.log.debug("All variables except builtins become public")

        # set all variables except builtins to public

        for name in self.deterministic | self.probabilistic:
            self.private.discard(name)
            self.public.discard(name)
            self.unknown_privacy.discard(name)
            self.public.add(name)

    def setAllUnknown(self):

        # set all variables except builtins to unknown privacy

        for name in self.deterministic | self.probabilistic:
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

    def define(self, name, code, evalcode=None, dependson=None, prob = False, hier = None, pyMC3code = None):
        self.log.debug("Define {name}, {code}, {dependson}, {prob}, {pyMC3code}".format(**locals()))
        self.acquire("define " + name)
        if not dependson:
            dependson = []
        if prob:
            self.probabilistic.add(name)
            self.probcode[name] = code
            self.pyMC3code[name] = pyMC3code
            if dependson != []:
                self.probdependson[name] = set(dependson)
            for n in self.probabilistic - self.deterministic:
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
        self.compute()
        self.computePrivacy() # every definition could change the privacy assignments

    def delete(self, name):
        self.acquire("delete "+name)
        if name in self.probabilistic | self.deterministic:

            for user in self.userids:
                self.changeState(user, name, "stale")
                self.globals[user].pop(name, None)

            self.deterministic.discard(name)
            self.probabilistic.discard(name)
            self.stale.discard(name)
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
        self.computePrivacy() # every delete could change the privacy assignments
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
                    res += base64.b64encode(self.globals["All"][name].getvalue())
                elif type(self.globals["All"][name]) == numpy.ndarray:
                    if longFormat:
                        res += str(self.globals["All"][name])
                    else:
                        s = self.globals["All"][name].shape
                        res += "[" * len(s) + "%f" % self.globals["All"][name].ravel()[0] + " ... " + "%f" % self.globals["All"][name].ravel()[-1] + "]" * len(s)
                elif type(self.globals["All"][name]) == float: # always display floats in full
                    res += str(self.globals["All"][name])
                else:
                    if longFormat:
                        res += json.dumps(self.globals["All"][name], indent=4)
                    else:
                        res += reprlib.repr(self.globals["All"][name])
            else:
                raise Exception(name + " is not stale, computing, exception or uptodate.")
        elif name in self.builtins:
            if name in self.public:
                if longFormat:
                    res += str(self.globals["All"][name])
                else:
                    res += reprlib.repr(self.globals["All"][name])
            else:
                res += "Private"
        else:
            raise Exception("Unknown variable in getValue" + name)
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
            return "\n".join("  ".join([codebit, valuebit, commentbit]) for codebit, valuebit, commentbit in zip(newcodebits, valuebits, commentbits))
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
            codebits.append(name + " = " + str(self.code[name]))
        for name in self.probcode.keys():
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
        nonuptodateparents = self.getParents(name) & (self.probabilistic - self.uptodate[user])
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



    def topological_sort(self):
        order, enter, state = deque(), self.probabilistic | self.deterministic, {}
        GRAY, BLACK = 0, 1

        def dfs(node):
            state[node] = GRAY
            for k in self.dependson.get(node, ()):
                sk = state.get(k, None)
                if sk == GRAY: raise ValueError("cycle")
                if sk == BLACK: continue
                enter.discard(k)
                dfs(k)
            order.appendleft(node)
            state[node] = BLACK

        while enter: dfs(enter.pop())
        return [name for name in order if name in self.probabilistic - self.deterministic]

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

    def constructPyMC3code(self, user=None):
        try:
            locals = {}
            loggingcode = """
try:
    logging = __import__("logging")
    _log = logging.getLogger("Private")
    logging.disable(100)
      """

            code = loggingcode

            # extract index variables

            for indexvariable in list(set(self.hierarchical.values())):
                code += "    __%s_Dict = dict((key, val) for val, key in enumerate(set(%s))) \n" % (indexvariable, indexvariable)
                code += "    __%s_Indices = [__%s_Dict[__private_index__] for __private_index__ in %s]\n" % (indexvariable, indexvariable, indexvariable)
                if user:
                    locals[indexvariable] = self.globals[user][indexvariable]

            code += """
    exception_variable = "No Exception Variable"
    pymc3 = __import__("pymc3")


    basic_model = pymc3.Model()

    with basic_model:

"""
            # Examples
            # mu = alpha + beta[0]*X1 + beta[1]*X2
            # sigma = pm.HalfNormal('sigma', sd=1)
            # Y_obs = pm.Normal('Y_obs', mu=mu, sd=sigma, observed=Y)

            probabilistic_only_names = self.topological_sort() # pyMC3 requires that these are ordered so that things that are dependent come later

            for name in probabilistic_only_names:
                code += '        exception_variable = "%s"\n' % name
                if name in self.hierarchical:
                    shapecode = ", shape = len(__%s_Dict)" % self.hierarchical[name]
                    code += "        " + self.pyMC3code[name] % shapecode + "\n"
                else:
                    code += "        " + self.pyMC3code[name] % ""+ "\n"

            observed_names = list(self.probabilistic & self.deterministic)
            for name in observed_names:
                code += '        exception_variable = "%s"\n' % name
                obsname = "__private_%s_observed" % name
                code += "        " + self.pyMC3code[name] % (", observed=%s" % obsname) + "\n"
                if user:
                    locals[obsname] = self.globals[user][name]
                else:
                    locals = None

            code += """
        __private_result__ = (pymc3.sample({NumberOfSamples}, tune={NumberOfTuningSamples}, chains={NumberOfChains}, random_seed=987654321, progressbar = False), "No Exception Variable")

except Exception as e:
    # remove stuff after the : as that sometimes reveals private information
    ind = e.args[0].find(":")
    if ind != -1:
        estring = e.args[0][0:ind]
    else:
        estring = e.args[0]

    newErrorString = estring   # do we need to do this?
    e.args = (newErrorString,)
    __private_result__ = (e, exception_variable)

""".format(NumberOfSamples=self.globals["All"]["NumberOfSamples"], NumberOfChains=self.globals["All"]["NumberOfChains"], NumberOfTuningSamples=self.globals["All"]["NumberOfTuningSamples"])

            return locals, code

        except Exception as e:
            self.log.debug("In constructMCcode user = " + user + " " + str(e))
            self.log.debug("In constructMCcode user = " + user + " " + str(self.globals[user]))


    def canRunSampler(self, user, verbose=False):
        if len(self.probabilistic) == 0:
            return False
        result = True
        if verbose:
            output = ""
        for name in self.probabilistic:
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


    def compute(self):

        self.acquire("compute")

        for user in self.userids:
            for name in self.variablesToBeCalculated(user):
                jobname = name + " " + user
                if jobname not in self.jobs:
                    self.changeState(user, name, "computing")
                    self.log.debug("Calculate: " + user + " " + name + " " + self.code[name])
                    self.jobs[name + " " + user] = self.server.submit(job, (name, user, self.evalcode[name], self.globals[user], self.locals), callback=self.callback)
                    #time.sleep(1)


        #self.log.debug("self.jobs: " + str(self.jobs.keys()))
        if len(self.jobs) == 0: # don't start a sampler until all other jobs have finished
            sampler_names = self.variablesToBeSampled()
            self.log.debug("sampler names: " + str(sampler_names))
            for user in self.userids:
                self.log.debug("stale names for user %s: " % user + str(self.stale[user]))
                if self.SamplerParameterUpdated or (sampler_names & self.stale[user] != set([])):
                    self.privacySamplerResults = {} # remove all privacy sampler results as they are now stale
                    if self.canRunSampler(user): # all necessary dependencies for all probabilistic variables have been defined or computed
                        for name in sampler_names:
                            self.changeState(user, name, "computing")
                        self.samplerexception[user] = {}

                        myname = "__private_sampler__" + user
                        locals, sampler_code =  self.constructPyMC3code(user)
                        self.jobs[myname] = self.server.submit(samplerjob, (myname, user, sampler_names, sampler_code, self.globals[user], locals), callback=self.samplercallback)
                        time.sleep(1)
                self.SamplerParameterUpdated = False
        self.release()

    def callback(self, returnvalue):
        self.acquire("callback")
        name, user, value = returnvalue
        if isinstance(value, Exception):
            if user == "All":
                self.globals[user][name] = str(value)
                self.changeState(user, name, "exception")
        else:
            self.globals[user][name] = value
            self.changeState(user, name, "uptodate")
            if user == "All":
                if name in ["NumberOfSamples", "NumberOfChains", "NumberOfTuningSamples"]:
                    self.SamplerParameterUpdated = True
                if type(value) == io.BytesIO:   # write image to file
                    value.seek(0)
                    with open(name+'.png', 'wb') as f:
                        shutil.copyfileobj(value, f)
        try:
            jobname = name + " " + user
            if jobname in self.jobs:
                del self.jobs[name + " " + user]
            else:
                self.log.debug("Trying to delete job %s that is not in self.jobs" % jobname)
                self.log.debug(self.jobs)
        except Exception as e:
            self.log.debug(str(e))

        self.release()
        self.compute()
        self.computePrivacy()

    def samplercallback(self, returnvalue):
        self.acquire("samplercallback")
        myname, user, names, value, exception_variable = returnvalue
        if isinstance(value, Exception):
            self.log.debug("Exception in sampler callback %s %s" % (user, str(value)))
            for name in names:
                self.globals[user][name] = ""
                self.changeState(user, name, "exception")
            if exception_variable != "No Exception Variable":
                m = re.match("__init__\(\) takes at least (\d+) arguments \(\d+ given\)", str(value))
                if m:
                    value = str(int(m.group(1))-1) + " arguments required."
                self.samplerexception[user][exception_variable] = str(value)
            else:
                for name in names:
                    self.samplerexception[user][name] = str(value)
        else: # successful sampler return
            try:
                for name in names:
                    if name in value.varnames:
                        self.globals[user][name] = numpy.random.permutation(value[name]) # permute to break the joint information across variables
                    else:                                                              # manifold privacy is applied to individual variables
                        self.globals[user][name] = "Not retained."                       # so there could be more information in the joint information
                                                                                         # that could be exploited
                for name in names:
                    self.changeState(user, name, "uptodate")

                # if all variables in all globals have been computed then calculate manifold privacy
                aname = list(names)[0]
                whichsamplersarecomplete = [isinstance(self.globals[u].get(aname, None), numpy.ndarray) for u in self.userids]
                if all(whichsamplersarecomplete):
                    #self.log.debug("sampling all done")
                    # calculate manifold privacy
                    # results are stored in self.privacySamplerResults (privacy of variables is not set directly)
                    self.log.debug("Have samples and calculating manifold privacy")

                    for name in names:
                        if name in value.varnames:

                            if self.globals[user][name].shape != self.globals["All"][name].shape: # if shape is affected by dropping a user then this variable is private
                                self.privacySamplerResults[name] = "private"
                            else:
                                allPublic = True
                                for usr in [u for u in self.userids if u != "All"]:
                                    try:
                                        d = distManifold(self.globals[usr][name], self.globals["All"][name]) * 100.
                                    except Exception as e:
                                        self.log.debug(str(e))
                                    self.log.debug(usr + ": " + name + ": " + str(d) + " " + str(d < PrivacyCriterion))
                                    allPublic = allPublic and d < PrivacyCriterion
                                if allPublic:
                                    self.privacySamplerResults[name] = "public"
                                else:
                                    self.privacySamplerResults[name] = "private"
                else:
                    self.log.debug("still more samples to compute " + str(whichsamplersarecomplete))
            except Exception as e:
                self.log.debug("in samplercallback when assigning values " + str(e))


        try:
            del self.jobs[myname]
        except Exception as e:
            self.log.debug("trying ot del job " + str(e))
        self.release()

        self.compute()

        self.computePrivacy()

    def showSamplerResults(self):
        res = str(len(self.privacySamplerResults)) + " results\n"
        for k,v in self.privacySamplerResults.items():
            res += k + ": " + v + "\n"
        return res

def job(name, user, code, globals, locals):
    try:
        value = eval(code, globals, locals)
        return((name, user, value))
    except Exception as e:
        return((name, user, e))

def samplerjob(myname, user, names, code, globals, locals):
    try:
        exec(code, globals, locals)
        value, exception_variable = locals["__private_result__"]
        return (myname, user, names, value, exception_variable)
    except Exception as e:
        return (myname, user, names, e, "No Exception Variable")

depGraph = graph()