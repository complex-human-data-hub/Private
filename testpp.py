import thread
import pp
import logging as l
import networkx as nx
import reprlib 
import numpy
import logging
_log = logging.getLogger("Private")
logging.basicConfig(filename='private.log',level=logging.WARNING)


__private_builtins__ = {"abs": abs, "all": all, "any":any, "bin":bin, "bool":bool, "chr":chr, "cmp":cmp, "complex":complex, "dict":dict, "dir":dir, "divmod":divmod, "enumerate":enumerate, "filter":filter, "float":float, "format":format, "frozenset":frozenset, "getattr":getattr, "hasattr":hasattr, "hex":hex, "int":int, "isinstance":isinstance, "issubclass":issubclass, "iter":iter, "len":len, "list":tuple, "long":long, "map":map, "mean": numpy.mean, "min":min, "max":max, "object":object, "oct":oct, "ord":ord, "pow":pow, "property":property, "range":range, "reduce":reduce, "repr":repr, "reversed":reversed, "round":round, "set": frozenset, "slice":slice, "sorted":sorted, "str":str, "sum":sum, "tuple":tuple, "type":type, "unichr":unichr, "unicode":unicode, "vars":vars, "xrange":xrange, "zip":zip}

__private_prob_builtins__ = set(["normal", "halfnormal"])

numpy.set_printoptions(precision=3)

class graph:

  def __init__(self):
     self.lock = thread.allocate_lock()
     self.globals = __private_builtins__
     self.locals = {}
     self.stale = set() # either stale, computing, exception or uptodate   - maybe colour red, orange, and green
     self.computing = set()
     self.exception = set()
     self.uptodate = set()
     self.private = set()
     self.allvars = set()
     self.code = {}
     self.probcode = {}
     self.pyMC3code = {}
     self.dependson = {}
     self.probdependson = {}
     self.jobs = {}
     self.server = pp.Server()
     self.graph = nx.DiGraph()

  def updateState(self):
    '''
    anything that is currently uptodate but depends deterministically on a stale value or a computing value should be stale
    '''
    _log.debug("Entering updateState")
    #self.lock.acquire()
    changed = True
    while changed:
      changed = False
      variablestocheck = list(self.uptodate & set(self.dependson.keys())-set(self.globals.keys())) # note globals are always uptodate
      _log.debug("updateState: " + str(variablestocheck))
      _log.debug("updateState: " + str(self.locals))
      for name in variablestocheck:
        if (self.dependson[name] & (self.stale | self.computing)):
          self.stale.add(name)
          self.uptodate.remove(name)
          changed = True

    # add code here to stop jobs that are computing but that are no longer needed

    #self.lock.release()
    _log.debug("Leaving updateState")

  def makeProbabilisticOnlyVariablesStale(self):
    #self.lock.acquire()
    for name in self.probdependson:
      if name not in self.dependson:
        if name in self.uptodate:
          self.uptodate.remove(name)
        self.stale.add(name)
    #self.lock.release()
        
  def updateGraph(self, name, dependson=[]):
      self.lock.acquire()
      # save a version of the current graph before making changes
      save = self.graph.copy()

      # Add variables and edges to graph data structure
      vars = [name] + dependson
      for var in vars:
          if var not in self.graph:
              self.graph.add_node(var)
          if var != name:
              self.graph.add_edge(var, name)

      # Remove edges to old predecessors
      preds = self.graph.predecessors(name)
      for pred in preds:
          if pred not in dependson:
              self.graph.remove_edge(pred, name)

      # Check for cycles
      try:
          cycles = nx.find_cycle(self.graph)
          self.graph = save
          self.lock.release()
          return False, cycles
      except:
          self.lock.release()
          return True, None

  def define(self, name, code, dependson=None, prob = False, pyMC3code = None, private=False):
    _log.debug("Entering define {name}, {code}, {dependson}, {prob}, {pyMC3code}".format(**locals()))
    self.lock.acquire()
    if not dependson:
      dependson = []
    if prob:
      self.probcode[name] = code
      self.pyMC3code[name] = pyMC3code
      self.probdependson[name] = set(dependson)
      if not name in self.dependson:
        self.stale.add(name)
        if name in self.uptodate:
          self.uptodate.remove(name)
        
    else:
      self.code[name] = code
      if private:
        self.private.add(name)
      self.dependson[name] = set(dependson)
      self.stale.add(name)
      if name in self.uptodate:
        self.uptodate.remove(name)
    self.allvars.add(name)
    # add code here to stop processes that depend on values that this define makes stale
    if name in self.probdependson:
      self.makeProbabilisticOnlyVariablesStale()
    self.updateState()   # this has to be outside lock
    self.lock.release()
    _log.debug("define: " + str(self))
    _log.debug("Leaving define")

  def delete(self, name):
      self.lock.acquire()
      try:
          if not self.has_descendants(name):
              self.graph.remove_node(name)
              if name in self.computing:
                  # Add code here to end job
                  pass
                  #self.computing.remove(name)
                  #self.computing[name]
              if name in self.uptodate:
                  self.uptodate.remove(name)
              if name in self.stale:
                  self.stale.remove(name)
          else:
              l.warning("You cannot delete a variable with descendants")
      except NetworkXError:
          l.warning("NetworkX error?")
          pass
      self.updateState()
      self.lock.release()

  def has_descendants(self, name):
      # Checks if a node given by 'name' has any descendants
      for var in self.dependson.keys():
          if name in self.dependson[var]:
              return True
      return False

  def check_cycles(self, name, dependson):
      # Checks to see if a new 'define' command will create a cycle in the graph
      existing_vars = self.dependson.keys()
      if name in dependson:
          return True
      elif name not in existing_vars:
          return False
      else:
          deps = [dep for dep in dependson if dep in existing_vars]
          if (len(deps) == 0):
              return False
          else:
              # Incomplete
              return True

  def hasVariable(self, variable):
    return variable in self.code or variable in self.probcode

  def getValue(self, name):
    res = ""
    if self.hasVariable(name):
      if name in self.private:
        res += "Private"
      elif name in self.stale:
        res += "Stale"
      elif name in self.computing:
        res += "Computing"
      elif name in self.exception:
        res += str(self.locals[name])
      elif name in self.uptodate:
        if type(self.locals[name]) == numpy.ndarray:
          s = self.locals[name].shape
          res += "[" * len(s) + "%f" % self.locals[name].ravel()[0] + " ... " + "%f" % self.locals[name].ravel()[-1] + "]" * len(s)
        else:
          res += reprlib.repr(self.locals[name])
      else:
        raise Exception(name + " is not stale, computing, exception or uptodate.")
    else:
      raise Exception("Unknown variable " + name)
    return res
      
  def __repr__(self):
    res = ""
    codebits = []
    for name in self.code.keys():
      codebits.append(name + " = " + str(self.code[name]))
    for name in self.probcode.keys():
      codebits.append(name + " ~ " + str(self.probcode[name]))
    m = max(len(line) for line in codebits)
    newcodebits = [line.ljust(m, " ") for line in codebits]
    valuebits = []
    for name in self.code.keys():
      valuebits.append(self.getValue(name))
    for name in self.probcode.keys():
      valuebits.append(self.getValue(name))
    return "\n".join("  ".join([codebit, valuebit]) for codebit, valuebit in zip(newcodebits, valuebits))

  def show_dependencies(self):
    res = ""
    for name in self.code.keys():
      res += name + " = "
      res += str(self.code[name])
      if self.dependson[name] != set([]):
        res += "    " + str(list(self.dependson[name]))
      res += "\n"
    for name in self.probcode.keys():
      res += name + " ~ "
      res += str(self.probcode[name])
      if self.probdependson[name] != set([]):
        res += "    " + str(list(self.probdependson[name]))
      res += "\n"
    print res[0:-1]

  def checkup(self, name):
    parents = []
    for parent in list(self.allvars):
      if parent in self.probdependson:
        if name in self.probdependson[parent]:
          parents.append(parent)
      #if parent in self.dependson:
      #  if name in self.dependson[parent]:
      #    parents.append(parent)
    if parents == []:
      return False
    for d in parents:
      if d not in self.uptodate:
        if not self.checkup(d):
          return False
    return True

  def checkdown(self, name):
    if name in self.probdependson:
      for d in self.probdependson[name]:
        if d not in self.uptodate and d not in self.locals and d not in __private_prob_builtins__:
          if d not in self.allvars:
            return False
          if not self.checkdown(d):
            return False
      return True
    else:
      return True

  def constructPyMC3code(self):
    locals = {}
    code = """
import pymc3 as pm
import logging
logger = logging.getLogger("pymc3")
logging.disable(100)

basic_model = pm.Model()

with basic_model:

"""
    # Examples
    # mu = alpha + beta[0]*X1 + beta[1]*X2
    # sigma = pm.HalfNormal('sigma', sd=1)
    # Y_obs = pm.Normal('Y_obs', mu=mu, sd=sigma, observed=Y)

    unobserved_names = list(set(self.probdependson.keys()) - set(self.dependson.keys()))
    for name in unobserved_names:
        code += "    " + self.pyMC3code[name] % ""+ "\n"
    observed_names = list(set(self.probdependson.keys()) & set(self.dependson.keys()))
    for name in observed_names:
      obsname = "__private_%s_observed" % name
      code += "    " + self.pyMC3code[name] % (", observed=%s" % obsname) + "\n"
      locals[obsname] = self.locals[name]

    code += """
    __private_result__ = pm.sample(500)
"""
    return locals, code

  def canRunSampler(self, verbose=False):
    _log.debug("Entering canRunSampler")
    result = True
    for name in self.probdependson.keys():
      if verbose: print name, "checkdown", self.checkdown(name)
      result = result and self.checkdown(name)
      if not name in self.uptodate:
        if verbose: print name, "checkup", self.checkup(name)
        result = result and self.checkup(name)
    _log.debug("Leaving canRunSampler: "+ str(result))
    return result

  def compute(self):
    _log.debug("Entering compute")
    self.lock.acquire()
    stales = list(self.stale)

    # do deterministic variables

    for name in self.dependson.keys():
      if name in self.stale:
        if all([(d in self.uptodate or d in self.globals) for d in self.dependson[name]]):
          self.stale.remove(name)
          self.computing.add(name)
          self.jobs[name] = self.server.submit(job, (name, self.code[name], self.globals, self.locals), callback=self.callback)

    _log.debug("compute: Done deterministic variables")

    # do probabilistic variables

    unobserved_names = list(set(self.probdependson.keys()) - set(self.dependson.keys()))
    uncalculated_unobserved_names = set(unobserved_names) & self.stale
    if len(uncalculated_unobserved_names) > 0:  # there are some probabilistic variables to calculate
      if self.canRunSampler(): # all necessary dependencies for all probabilistic variables have been defined or computed
        locals, sampler_code =  self.constructPyMC3code()
        for name in unobserved_names:
            self.stale.remove(name)
            self.computing.add(name)
        self.jobs["__private_sampler__"] = self.server.submit(samplerjob, (unobserved_names, sampler_code, self.globals, locals), callback=self.samplercallback)

    self.lock.release()
    _log.debug("Leaving compute")

  def callback(self, returnvalue):
    self.lock.acquire()
    name, value = returnvalue
    if type(value) == Exception:
      self.locals[name] = str(value)
      self.computing.remove(name)
      self.exception.add(name)
    else:
      self.locals[name] = value
      self.computing.remove(name)
      self.uptodate.add(name)
    del self.jobs[name]

    self.lock.release()
    self.compute()

  def samplercallback(self, returnvalue):   # work on this
    self.lock.acquire()
    names, value = returnvalue
    if type(value) == Exception:
      for name in names:
        self.locals[name] = str(value)
        self.computing.remove(name)
        self.exception.add(name)
    else: # successful sampler return
      for name in names:
        self.locals[name] = value[name]
        self.computing.remove(name)
        self.uptodate.add(name)

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

def setup():
  g = graph()
  g.define("a", "b * c", dependson = ["b", "c"])
  g.define("b", "2")
  g.define("c", "4")
  return(g)

depGraph = graph()
