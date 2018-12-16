#import thread
import multiprocessing
import pp
#import logging as l
#import networkx as nx
import reprlib 
import numpy
from collections import OrderedDict
import logging
from builtins import builtins, prob_builtins, setPrivacy
import copy
import traceback
from manifoldprivacy import distManifold
import shutil
import io
import re
import traceback
import pprint

logging.basicConfig(filename='private.log',level=logging.WARNING)

numpy.set_printoptions(precision=3)

PrivacyCriterion = 1.0

def ppset(s):
  """
  Pretty print a set.
  """
  s = list(s)
  s.sort()
  return " ".join(s)

class graph:

  def __init__(self):

    #self.lock = thread.allocate_lock()
    self.lock = multiprocessing.Lock()
    self.whohaslock = None
    self.globals = copy.copy(builtins)
    self.locals = {}
    self.prettyprinter = pprint.PrettyPrinter()


    # each current program variable should be either deterministic or probablistic or both

    self.deterministic = set()
    self.probabilistic = set()
    self.builtins = set(builtins.keys()) or prob_builtins
    #self.imports = set()

    # each variable should be in one of stale, computing, exception or uptodate

    self.stale = set() 
    self.computing = set()
    self.exception = set()
    self.uptodate = set(builtins.keys()) or prob_builtins
    self.samplerexception = {}

    # each variable should be in private, public, privacy_unknown

    self.private = set()
    self.public = set()
    self.privacy_unknown = set()


    # code associated with variables

    self.code = OrderedDict()   # private code for deterministic variables
    self.probcode = OrderedDict() # private code of probabilistic variables
    self.evalcode = OrderedDict() # python code for determinitisitc variables
    self.pyMC3code = OrderedDict() # pyMC3 code for probabilistic variables

    # dependencies

    self.dependson = {} # deterministic dependencies
    self.probdependson = {} # probabilistic dependencies

    # comments

    self.comment = {}

    # auxiliary variables

    self.jobs = {}
    self.sampler_chains = {}
    self.server = pp.Server()
    self.log = logging.getLogger("Private")
    #self.nxgraph = nx.DiGraph()

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
    #result += "imports: "+ ppset(self.imports) + "\n"
    result += "\n"
    result += "uptodate: "+ ppset(self.uptodate) + "\n"
    result += "computing: "+ ppset(self.computing) + "\n"
    result += "exception: "+ ppset(self.exception) + "\n"
    result += "stale: "+ ppset(self.stale) + "\n"
    result += "\n"
    result += "private: "+ ppset(self.private) + "\n"
    result += "public: "+ ppset(self.public) + "\n"
    result += "privacy_unknown: "+ ppset(self.privacy_unknown) + "\n"
    result += "\n"
    result += "locals: "+ ppset(self.locals.keys()) + "\n"
    result += "globals: "+ ppset(self.globals.keys()) + "\n"
    return result

  def checkprivacyup(self, name):
    if name in self.public:
      return True
    else:
      parents = self.getParents(name)
      if parents == set():
        return False
      else:
        return all(self.checkprivacyup(parent) for parent in parents)

  def checkprivacydown(self, name):
    if name in self.public:
      return True
    else:
      children = self.getChildren(name)
      if children == set():
        return False
      else:
        return all(self.checkprivacydown(child) for child in children)

  def eval_command_line_expression(self, code):
    return(eval(code, self.globals, self.locals))

  def computePrivacy(self):
    
    try:
      if self.uptodate & self.privacy_unknown == set():
        return
      for name in self.deterministic:
        if all(child in self.public for child in self.dependson[name]):
          self.setPrivacy(name, "public")
        elif any(child in self.private for child in self.dependson[name]):
          self.setPrivacy(name, "private")
        else:
          self.setPrivacy(name, "privacy_unknown")
      if len(self.jobs) == 0:
        anyPrivacyUnknown = False
        for name in self.probabilistic - self.deterministic:
          if self.checkprivacyup(name) and self.checkprivacydown(name):
            self.setPrivacy(name, "public")
          else:
            self.setPrivacy(name, "privacy_unknown")
            anyPrivacyUnknown = True

        if anyPrivacyUnknown:
          if self.canRunSampler(): # all necessary dependencies for all probabilistic variables have been defined or computed
            sampler_names = self.variablesToBeSampled()
            locals, sampler_code =  self.constructPyMC3code()
            AllEvents = self.globals["Events"]
            users = set([e.UserId for e in AllEvents])
            for user in users:
              self.globals["Events"] = [e for e in AllEvents if e.UserId != user]
              myname = "__private_sampler__" + user
              self.sampler_chains[myname] = None
              self.jobs[myname] = self.server.submit(samplerjob, (myname, sampler_names, sampler_code, self.globals, locals), callback=self.privacysamplercallback)
            self.globals["Events"] = AllEvents # make sure to set globals["Events"] back to the entire data set on completion
    except Exception as e:
      print "here: ", e

  def changeState(self, name, newstate):
    self.log.debug("Change state of %s to %s." % (name, newstate))
    self.uptodate.discard(name)
    self.computing.discard(name)
    self.exception.discard(name)
    self.stale.discard(name)
    if newstate == "uptodate":   # whenever a variable changes to be uptodate the privacy could have changed
      self.uptodate.add(name)
    elif newstate == "computing": # when a variables changes to be computing its privacy is unknown
      self.computing.add(name)
      self.setPrivacy(name, "privacy_unknown")
    elif newstate == "exception": # when a variables changes to be exception its privacy is unknown
      self.exception.add(name)
      self.setPrivacy(name, "privacy_unknown")
    elif newstate == "stale": # when a variable changes to be stale its privacy is unknown
      self.stale.add(name)
      self.setPrivacy(name, "privacy_unknown")
      # check dependencies to see if other variables need to be made stale
      #print name, self.deterministicParents(name)
      for parent in self.deterministicParents(name): # parents via deterministic links
        #print name, " det ", self.deterministicParents(name)
        if parent not in self.stale:
          self.changeState(parent, "stale")
      for child in self.probabilisticChildren(name): # children via probabilistic links
        #print name, " prob ", self.deterministicParents(name)
        if child not in self.stale and child not in self.builtins:
          self.changeState(child, "stale")
    else:
      raise Exception("Unknown state %s in changeState" % newstate)
    self.computePrivacy()

  def setPrivacy(self, name, privacy):
    self.log.debug(name + " becomes " + privacy)
    self.private.discard(name)
    self.public.discard(name)
    self.privacy_unknown.discard(name)

    if privacy == "private":
      self.private.add(name)
    elif privacy == "public":
      self.public.add(name)
    elif privacy == "privacy_unknown":
      self.privacy_unknown.add(name)

  def add_comment(self, name, the_comment):
    self.comment[name] = the_comment

  #def define(self, name, code, evalcode=None, dependson=None, prob = False, pyMC3code = None, privacy="privacy_unknown"):
  def define(self, name, code, evalcode=None, dependson=None, prob = False, pyMC3code = None):
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
          self.changeState(n, "stale")
    else:
      self.deterministic.add(name)
      self.code[name] = code
      self.evalcode[name] = evalcode
      self.dependson[name] = set(dependson)
      self.changeState(name, "stale")
    self.release()
    self.compute()

  def delete(self, name):
    self.acquire("delete "+name)
    self.changeState(name, "stale")

    self.globals.pop(name, None)
    self.deterministic.discard(name)
    self.probabilistic.discard(name)
    self.stale.discard(name)
    self.private.discard(name)
    self.public.discard(name)
    self.privacy_unknown.discard(name)

    self.code.pop(name, None)
    self.probcode.pop(name, None)
    self.pyMC3code.pop(name, None)

    self.dependson.pop(name, None)
    self.probdependson.pop(name, None)
    self.comment.pop(name, None)
    self.release()
  
#  def delete(self, name):
#      self.lock.acquire()
#      try:
#          if not self.has_descendants(name):
#              self.graph.remove_node(name)
#              if name in self.computing:
#                  # Add code here to end job
#                  pass
#                  #self.computing.remove(name)
#                  #self.computing[name]
#              if name in self.uptodate:
#                  self.uptodate.remove(name)
#              if name in self.stale:
#                  self.stale.remove(name)
#          else:
#              l.warning("You cannot delete a variable with descendants")
#      except NetworkXError:
#          l.warning("NetworkX error?")
#          pass
#      self.release()
#      #self.updateState()

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
      if name in self.stale:
        res += "Stale"
      elif name in self.computing:
        res += "Computing"
      elif name in self.exception: 
        res += str(self.globals[name])
      elif name in self.private:
        res += "Private"
      elif name in self.privacy_unknown:
        res += "Privacy Unknown"
      elif name in self.uptodate:
        if type(self.globals[name]) == numpy.ndarray:
          if longFormat:
            res += str(self.globals[name])
          else:
            s = self.globals[name].shape
            res += "[" * len(s) + "%f" % self.globals[name].ravel()[0] + " ... " + "%f" % self.globals[name].ravel()[-1] + "]" * len(s)
        elif type(self.globals[name]) == float: # always display floats in full
          res += str(self.globals[name])
        else:
          if longFormat:
            res += self.prettyprinter.pformat(self.globals[name])
          else:
            res += reprlib.repr(self.globals[name])
      else:
        raise Exception(name + " is not stale, computing, exception or uptodate.")
    elif name in self.builtins:
      if name in self.public:
        if longFormat:
          res += str(self.globals[name])
        else:
          res += reprlib.repr(self.globals[name])
      else:
        res += "Private"
    else:
      raise Exception("Unknown variable in getValue" + name)
    return res
      
  def __repr__(self):
    codebits = []
    codewidth = 80
    valuewidth = 80
    for name in self.code.keys():
      codebits.append(name + " = " + str(self.code[name]))
    for name in self.probcode.keys():
      codebits.append(name + " ~ " + str(self.probcode[name]))
    if len(codebits) > 0:
      m = max(len(line) for line in codebits)
      m = min(m, codewidth)
      newcodebits = [line[0:codewidth].ljust(m, " ") for line in codebits]
      valuebits = []
      for name in self.code.keys():
        valuebits.append(self.getValue(name)[0:codewidth])
      for name in self.probcode.keys():
        if name in self.samplerexception:
          valuebits.append(self.samplerexception[name])
        else:
          valuebits.append(self.getValue(name)[0:codewidth])
      commentbits = []
      for name in self.code.keys():
        commentbits.append(self.comment.get(name, ""))
      for name in self.probcode.keys():
        commentbits.append(self.comment.get(name, ""))
      return "\n".join("  ".join([codebit, valuebit, commentbit]) for codebit, valuebit, commentbit in zip(newcodebits, valuebits, commentbits))
    else:
      return ""

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

  def checkup(self, name):
    nonuptodateparents = self.getParents(name) & self.probabilistic - self.uptodate
    if nonuptodateparents == set([]):
      return True
    else:
      return all(self.checkup(p) for p in nonuptodateparents)

  def checkdown(self, name):
    if name not in self.dependson and name not in self.probdependson:
      return False

    nonuptodatechildren = self.getChildren(name) - self.uptodate - prob_builtins
    if nonuptodatechildren == set([]):
      return True
    else:
      return all(self.checkdown(p) for p in nonuptodatechildren)

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

  #def getAncestors(self, name):
  #  parents = self.getParents(name)
  #  result = parents
  #  for name in parents:
  #    result = result | self.getAncestors(name)
  #  return result

  def getChildren(self, name):
    return self.dependson.get(name, set([])) | self.probdependson.get(name, set([]))

  def probabilisticChildren(self, name):
    return self.probdependson.get(name, set([]))

  #def getDescendants(self, name):
  #  children = self.getChildren(name)
  #  result = children
  #  for name in children:
  #    result = result | self.getDescendants(name)
  #  return result
      

  def constructPyMC3code(self):
    locals = {}
    loggingcode = """
import logging
_log = logging.getLogger("Private")
logging.disable(100)
"""

    code = loggingcode + """
import pymc3 as pm


try:

  basic_model = pm.Model()

  with basic_model:

"""
    # Examples
    # mu = alpha + beta[0]*X1 + beta[1]*X2
    # sigma = pm.HalfNormal('sigma', sd=1)
    # Y_obs = pm.Normal('Y_obs', mu=mu, sd=sigma, observed=Y)

    probabilsitic_only_names = list(self.probabilistic - self.deterministic)
    for name in probabilsitic_only_names:
      code += '    exception_variable = "%s"\n' % name
      code += "    " + self.pyMC3code[name] % ""+ "\n"

    observed_names = list(self.probabilistic & self.deterministic)
    for name in observed_names:
      code += '    exception_variable = "%s"\n' % name
      obsname = "__private_%s_observed" % name
      code += "    " + self.pyMC3code[name] % (", observed=%s" % obsname) + "\n"
      locals[obsname] = self.globals[name]

    code += """
    __private_result__ = (pm.sample({NumberOfSamples}, tune={NumberOfTuningSamples}, chains={NumberOfChains}, random_seed=987654321, progressbar = False), "No Exception Variable")

except Exception as e:
  # remove stuff after the : as that sometimes reveals private information
  ind = e.args[0].find(":")
  if ind != -1:
    estring = e.args[0][0:ind]
  else:
    estring = e.args[0]
    
  newErrorString = estring
  e.args = (newErrorString,)
  __private_result__ = (e, exception_variable)

""".format(NumberOfSamples=self.globals["NumberOfSamples"], NumberOfChains=self.globals["NumberOfChains"], NumberOfTuningSamples=self.globals["NumberOfTuningSamples"])
    return locals, code

  def canRunSampler(self, verbose=False):
    if len(self.probabilistic) == 0:
      return False
    result = True
    if verbose:
      output = ""
    for name in self.probabilistic:
      if verbose: output += name + " checkdown " + str(self.checkdown(name)) + "\n"
      result = result and self.checkdown(name)
      if verbose: output += name + " checkup " + str(self.checkup(name)) + "\n"
      result = result and self.checkup(name)
    if verbose:
      return output
    else:
      return result

  def variablesToBeSampled(self):

    names = self.probabilistic - self.deterministic
    return names

  def variablesToBeCalculated(self):
    names = set([])
    for name in self.deterministic & self.stale:
      self.log.debug(name + " " + str(self.dependson.get(name, set([])) - self.uptodate - self.builtins ))
      self.log.debug(name + " " + str(self.dependson.get(name, set([]))))
      self.log.debug(name + " " + str(self.uptodate))
      self.log.debug(name + " " + str(self.builtins))
      if self.dependson.get(name, set([])) - self.uptodate - self.builtins == set([]):
        names.add(name)
    return(names)

    
  def compute(self):

    self.acquire("compute")

    for name in self.variablesToBeCalculated():
      if name not in self.jobs:
        self.changeState(name, "computing")
        self.log.debug("Calculate: " + name + " " + self.code[name])
        self.jobs[name] = self.server.submit(job, (name, self.evalcode[name], self.globals, self.locals), callback=self.callback)
      
    
    if len(self.jobs) == 0: # don't start a sampler until all other jobs have finished
      sampler_names = self.variablesToBeSampled()
      if sampler_names & self.stale != set([]):
        if self.canRunSampler(): # all necessary dependencies for all probabilistic variables have been defined or computed
          locals, sampler_code =  self.constructPyMC3code()
          for name in sampler_names:
            self.changeState(name, "computing")
          myname = "__private_sampler__"
          self.sampler_chains[myname] = None
          self.samplerexception = {}
          self.jobs["__private_sampler__"] = self.server.submit(samplerjob, (myname, sampler_names, sampler_code, self.globals, locals), callback=self.samplercallback)
    self.computePrivacy()
    self.release()

  def callback(self, returnvalue):
    self.acquire("callback")
    name, value = returnvalue
    if isinstance(value, Exception):
      self.globals[name] = str(value)
      self.changeState(name, "exception")
    else:
      self.globals[name] = value
      self.changeState(name, "uptodate")
      if type(value) == io.BytesIO:   # write image to file 
        value.seek(0)
        with open(name+'.png', 'wb') as f:
          shutil.copyfileobj(value, f)
    del self.jobs[name]

    self.release()
    self.compute()

  def samplercallback(self, returnvalue):  
    self.acquire("samplercallback")
    myname, names, value, exception_variable = returnvalue
    if isinstance(value, Exception):
      for name in names:
        self.globals[name] = ""
        self.changeState(name, "exception")
      if exception_variable != "No Exception Variable":
        m = re.match("__init__\(\) takes at least (\d+) arguments \(\d+ given\)", str(value))
        if m:
          value = str(int(m.group(1))-1) + " arguments required."
        self.samplerexception[exception_variable] = str(value)
    else: # successful sampler return
      tochecknames = list(self.privacy_unknown & set(value.varnames))   # names to check for privacy
      self.log.debug("names to check " + str(tochecknames))
      if len(tochecknames) > 0:
        try:
          sampleslist = [value[name] for name in tochecknames]
          samples = numpy.concatenate(sampleslist)
        except Exception as e:
          print "in samplercallback", e
        self.sampler_chains[myname] = samples
        self.log.debug(self.show_sampler_chains())

      for name in names:
        if name in value.varnames:
          self.globals[name] = value[name]
        else:
          self.globals[name] = "Not retained."
          self.setPrivacy(name, "public") # no problem making this public as there is nothing to see
          
        self.changeState(name, "uptodate")

    del self.jobs["__private_sampler__"]
    self.release()
    self.compute()

  def show_sampler_chains(self):
    res = str(len(self.sampler_chains)) + " chains\n"
    try:
      for k,v in self.sampler_chains.items():
        if type(v) == str:
          res += k+ " " + str(v) + "\n"
        elif type(v) == numpy.ndarray:
          res += k+ " array\n"
        elif v == None:
          res += k+ " None\n"
        else:
          res += "Unknown value type\n"
    except Exception as e:
        res += "here" + str(e)
        #traceback.print_exc()
    return res

  def privacysamplercallback(self, returnvalue):  
    self.acquire("privacysamplercallback")
    try:
      myname, names, value, exception_variable = returnvalue
      tochecknames = list(self.privacy_unknown & set(value.varnames))
      if len(tochecknames) > 0:
        sampleslist = [value[name] for name in tochecknames]
        samples = numpy.concatenate(sampleslist)
        self.sampler_chains[myname] = samples
        if type(self.sampler_chains["__private_sampler__"]) == numpy.ndarray: # note this should always be the case 
          for usertest in self.sampler_chains.keys():
            if usertest != "__private_sampler__":
              if type(self.sampler_chains[usertest]) == numpy.ndarray:
                try:
                  d = distManifold(self.sampler_chains[usertest], self.sampler_chains["__private_sampler__"]) * 100.
                except Exception as e:
                  print e
                if d < PrivacyCriterion:
                  self.sampler_chains[usertest] = "public"
                else:
                  self.sampler_chains[usertest] = "private"
 
          if all(False if type(v) == numpy.ndarray else v == "public" for k,v in self.sampler_chains.items() if k != "__private_sampler__"):
            for name in tochecknames:
              self.setPrivacy(name, "public")
          elif any(False if type(v) == numpy.ndarray else v == "private" for k,v in self.sampler_chains.items() if k != "__private_sampler__"):
            for name in tochecknames:
              self.setPrivacy(name, "private")
          self.log.debug(self.show_sampler_chains())
        else:
          self.log.error("The primary sampler chains should always have been calculated prior to the privacy sampler chains")
          self.log.debug(self.show_sampler_chains())

      del self.jobs[myname]
    except Exception as e:
      print "In privacysamplercallback", e
    self.release()
    self.compute()

def job(name, code, globals, locals):
  try:
    value = eval(code, globals, locals)
    return((name, value))
  except Exception as e:
    return((name, e))

def samplerjob(myname, names, code, globals, locals):
  try:
    exec(code, globals, locals)
    value, exception_variable = locals["__private_result__"]
    return (myname, names, value, exception_variable)
  except Exception as e:
    return (myname, names, e, "No Exception Variable")

depGraph = graph()
setPrivacy(depGraph) # set privacy of builtins
