import thread
import multiprocessing
import pp
#import logging as l
import networkx as nx
import reprlib 
import numpy
from collections import OrderedDict
import logging
logging.basicConfig(filename='private.log',level=logging.WARNING)


__private_builtins__ = {"abs": abs, "all": all, "any":any, "bin":bin, "bool":bool, "chr":chr, "cmp":cmp, "complex":complex, "dict":dict, "dir":dir, "divmod":divmod, "enumerate":enumerate, "filter":filter, "float":float, "format":format, "frozenset":frozenset, "getattr":getattr, "hasattr":hasattr, "hex":hex, "int":int, "isinstance":isinstance, "issubclass":issubclass, "iter":iter, "len":len, "list":tuple, "long":long, "map":map, "min":min, "max":max, "object":object, "oct":oct, "ord":ord, "pow":pow, "property":property, "range":range, "reduce":reduce, "repr":repr, "reversed":reversed, "round":round, "set": frozenset, "slice":slice, "sorted":sorted, "str":str, "sum":sum, "tuple":tuple, "type":type, "unichr":unichr, "unicode":unicode, "vars":vars, "xrange":xrange, "zip":zip}

__private_prob_builtins__ = set(["normal", "halfnormal"])

numpy.set_printoptions(precision=3)

def ppset(s):
  """
  Pretty print a set.
  """
  s = list(s)
  return " ".join(s)

class graph:

  def __init__(self):

    #self.lock = thread.allocate_lock()
    self.lock = multiprocessing.Lock()
    self.globals = __private_builtins__
    self.locals = {}


    # each current program variable should be either deterministic or probablistic or both

    self.deterministic = set()
    self.probabilistic = set()
    self.builtin = set(__private_builtins__.keys()) or __private_prob_builtins__
    self.imports = set()

    # each variable should be in one of stale, computing, exception or uptodate

    self.stale = set() 
    self.computing = set()
    self.exception = set()
    self.uptodate = set(__private_builtins__.keys()) or __private_prob_builtins__

    # each variable should be in private, releasable, privacy_unknown

    self.private = set()
    self.releasable = set()
    self.privacy_unknown = set()


    # code associated with variables

    self.code = OrderedDict()   # private code for deterministic variables
    self.probcode = OrderedDict() # private code of probabilistic variables
    self.pyMC3code = OrderedDict() # pyMC3 code for probabilistic variables

    # dependencies

    self.dependson = {} # deterministic dependencies
    self.probdependson = {} # probabilistic dependencies

    # comments

    self.comment = {}

    # auxiliary variables

    self.jobs = {}
    self.server = pp.Server()
    self.log = logging.getLogger("Private")
    #self.nxgraph = nx.DiGraph()

  def show_sets(self):
    result = ""
    result += "deterministic: "+ ppset(self.deterministic) + "\n"
    result += "probabilistic: "+ ppset(self.probabilistic) + "\n"
    result += "builtin: "+ ppset(self.builtin) + "\n"
    result += "imports: "+ ppset(self.imports) + "\n"
    result += "\n"
    result += "uptodate: "+ ppset(self.uptodate) + "\n"
    result += "computing: "+ ppset(self.computing) + "\n"
    result += "exception: "+ ppset(self.exception) + "\n"
    result += "stale: "+ ppset(self.stale) + "\n"
    result += "\n"
    result += "private: "+ ppset(self.private) + "\n"
    result += "releasable: "+ ppset(self.releasable) + "\n"
    result += "privacy_unknown: "+ ppset(self.privacy_unknown) + "\n"
    result += "\n"
    result += "locals: "+ ppset(self.locals.keys()) + "\n"
    result += "globals: "+ ppset(self.globals.keys()) + "\n"
    return result

  def changeState(self, name, newstate):
    self.log.debug("Change state of %s to %s." % (name, newstate))
    if name in self.uptodate:
      self.uptodate.remove(name)
    if name in self.computing:
      self.computing.remove(name)
    if name in self.exception:
      self.exception.remove(name)
    if name in self.stale:
      self.stale.remove(name)
    if newstate == "uptodate":
      self.uptodate.add(name)
    elif newstate == "computing":
      self.computing.add(name)
    elif newstate == "exception":
      self.exception.add(name)
    elif newstate == "stale":
      self.stale.add(name)
      # check dependencies to see if other variables need to be made stale
      for parent in self.deterministicParents(name): # parents via deterministic links
        if parent not in self.stale:
          self.changeState(parent, "stale")
      for child in self.probabilisticChildren(name): # children via probabilistic links
        if child not in self.stale and child not in self.builtin and child not in self.imports:
          self.changeState(child, "stale")
 
        
        
    else:
      raise Exception("Unknown state %s in changeState" % newstate)

  def add_comment(self, name, the_comment):
    self.comment[name] = the_comment

  def define(self, name, code, dependson=None, prob = False, pyMC3code = None, private=False):
    self.log.debug("Define {name}, {code}, {dependson}, {prob}, {pyMC3code}".format(**locals()))
    self.lock.acquire()
    if not dependson:
      dependson = []
    if prob:
      self.probabilistic.add(name)
      self.probcode[name] = code
      self.pyMC3code[name] = pyMC3code
      if dependson != []:
        self.probdependson[name] = set(dependson)
      for name in self.probabilistic - self.deterministic:
        self.changeState(name, "stale")
    else:
      self.deterministic.add(name)
      self.code[name] = code
      if private:
        self.private.add(name)
      if dependson != []:
        self.dependson[name] = set(dependson)
      self.changeState(name, "stale")
      if set(dependson) & self.private != set():
        self.private.add(name)
    self.lock.release()

  def delete(self, name):
    self.lock.acquire()
    self.changeState(name, "stale")

    self.globals.pop(name, None)
    self.deterministic.discard(name)
    self.probabilistic.discard(name)
    self.stale.discard(name)
    self.private.discard(name)
    self.releasable.discard(name)
    self.privacy_unknown.discard(name)

    self.code.pop(name, None)
    self.probcode.pop(name, None)
    self.pyMC3code.pop(name, None)

    self.dependson.pop(name, None)
    self.probdependson.pop(name, None)
    self.comment.pop(name, None)
    self.lock.release()
  
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
#      self.lock.release()
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

  def getValue(self, name):
    res = ""
    if name in self.deterministic | self.probabilistic:
      if name in self.private:
        res += "Private"
      elif name in self.stale:
        res += "Stale"
      elif name in self.computing:
        res += "Computing"
      elif name in self.exception:
        res += "Exception: " + str(self.globals[name])
      elif name in self.uptodate:
        if type(self.globals[name]) == numpy.ndarray:
          s = self.globals[name].shape
          res += "[" * len(s) + "%f" % self.globals[name].ravel()[0] + " ... " + "%f" % self.globals[name].ravel()[-1] + "]" * len(s)
        else:
          res += reprlib.repr(self.globals[name])
      else:
        raise Exception(name + " is not stale, computing, exception or uptodate.")
    else:
      raise Exception("Unknown variable " + name)
    return res
      
  def __repr__(self):
    codebits = []
    for name in self.code.keys():
      codebits.append(name + " = " + str(self.code[name]))
    for name in self.probcode.keys():
      codebits.append(name + " ~ " + str(self.probcode[name]))
    if len(codebits) > 0:
      m = max(len(line) for line in codebits)
      newcodebits = [line.ljust(m, " ") for line in codebits]
      valuebits = []
      for name in self.code.keys():
        valuebits.append(self.getValue(name))
      for name in self.probcode.keys():
        valuebits.append(self.getValue(name))
      commentbits = []
      for name in self.code.keys():
        commentbits.append(self.comment.get(name, ""))
      for name in self.probcode.keys():
        commentbits.append(self.comment.get(name, ""))
      return "\n".join("  ".join([codebit, valuebit, commentbit]) for codebit, valuebit, commentbit in zip(newcodebits, valuebits, commentbits))
    else:
      return ""

  def show_dependencies(self):
    res = ""
    for name in self.code.keys():
      res += name + " = "
      res += str(self.code[name])
      if name in self.dependson:
        if self.dependson[name] != set([]):
          res += "    " + str(list(self.dependson[name]))
      res += "\n"
    for name in self.probcode.keys():
      res += name + " ~ "
      res += str(self.probcode[name])
      if name in self.probdependson:
        if self.probdependson[name] != set([]):
          res += "    " + str(list(self.probdependson[name]))
      res += "\n"
    print res[0:-1]

  def checkup(self, name):
    nonuptodateparents = self.getParents(name) & self.probabilistic - self.uptodate
    if nonuptodateparents == set([]):
      return True
    else:
      return all(self.checkup(p) for p in nonuptodateparents)
    '''
    parents = self.getParents(name)
    if parents == []:
      return False
    for d in parents:
      if d not in self.uptodate:
        if not self.checkup(d):
          return False
    return True
'''

  def checkdown(self, name):
    if name not in self.dependson and name not in self.probdependson:
      return False

    nonuptodatechildren = self.getChildren(name) - self.uptodate - __private_prob_builtins__
    if nonuptodatechildren == set([]):
      return True
    else:
      return all(self.checkdown(p) for p in nonuptodatechildren)
    '''
    if name not in self.probdependson and name not in self.dependson:
      return False

    # check dependencies

    result = True
    if name in self.probdependson:
      for d in self.probdependson[name]:
        if d not in self.uptodate and d not in __private_prob_builtins__:
          result = result and self.checkdown(d)
    if name in self.dependson:
      for d in self.dependson[name]:
        if d not in self.uptodate and d not in __private_prob_builtins__:
          result = result and self.checkdown(d)
    return result
'''

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

    code = """
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
      code += "    " + self.pyMC3code[name] % ""+ "\n"

    observed_names = list(self.probabilistic & self.deterministic)
    for name in observed_names:
      obsname = "__private_%s_observed" % name
      code += "    " + self.pyMC3code[name] % (", observed=%s" % obsname) + "\n"
      locals[obsname] = self.globals[name]

    code += """
    __private_result__ = pm.sample(500, progressbar = False)

except Exception as e:
  __private_result__ = e

"""
    return locals, code

  def canRunSampler(self, verbose=False):
    result = True
    for name in self.probabilistic:
      if verbose: print name, "checkdown", self.checkdown(name)
      result = result and self.checkdown(name)
      if verbose: print name, "checkup", self.checkup(name)
      result = result and self.checkup(name)
    return result

  def variablesToBeSampled(self):

    names = self.probabilistic - self.deterministic
    return names

  def variablesToBeCalculated(self):
    names = set([])
    for name in self.deterministic & self.stale:
      if self.dependson.get(name, set([])) - self.uptodate - self.builtin - self.imports == set([]):
        names.add(name)
    return(names)

    
  def compute(self):

    self.lock.acquire()

    for name in self.variablesToBeCalculated():
      if name not in self.jobs:
        self.changeState(name, "computing")
        self.log.debug("Calculate: " + name + " " + self.code[name])
        self.jobs[name] = self.server.submit(job, (name, self.code[name], self.globals, self.locals), callback=self.callback)
      
    
    if len(self.jobs) == 0: # don't start a sampler until all other jobs have finished
      sampler_names = self.variablesToBeSampled()
      if sampler_names & self.stale != set([]):
        if self.canRunSampler(): # all necessary dependencies for all probabilistic variables have been defined or computed
          locals, sampler_code =  self.constructPyMC3code()
          for name in sampler_names:
            self.changeState(name, "computing")
          self.jobs["__private_sampler__"] = self.server.submit(samplerjob, (sampler_names, sampler_code, self.globals, locals), callback=self.samplercallback)
        


    self.lock.release()

  def callback(self, returnvalue):
    self.lock.acquire()
    name, value = returnvalue
    if isinstance(value, Exception):
      self.globals[name] = str(value)
      self.changeState(name, "exception")
    else:
      self.globals[name] = value
      self.changeState(name, "uptodate")
    del self.jobs[name]

    self.lock.release()
    self.compute()

  def samplercallback(self, returnvalue):   # work on this
    self.lock.acquire()
    names, value = returnvalue
    if isinstance(value, Exception):
      for name in names:
        self.globals[name] = str(value)
        self.changeState(name, "exception")
    else: # successful sampler return
      for name in names:
        if name in value.varnames:
          self.globals[name] = value[name]
        else:
          self.globals[name] = "Not retained."
          
        self.changeState(name, "uptodate")

    del self.jobs["__private_sampler__"]
    self.lock.release()
    self.compute()

def job(name, code, globals, locals):
  try:
    value = eval(code, globals, locals)
    return((name, value))
  except Exception as e:
    return((name, e))

def samplerjob(names, code, globals, locals):
  try:
    exec(code, globals, locals)
    return (names, locals["__private_result__"])
  except Exception as e:
    return (names, e)

depGraph = graph()
