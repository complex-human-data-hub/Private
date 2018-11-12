import thread
import pp
import logging as l
import networkx as nx
import reprlib 
import numpy
from collections import OrderedDict
import logging
_log = logging.getLogger("Private")
logging.basicConfig(filename='private.log',level=logging.WARNING)


__private_builtins__ = {"abs": abs, "all": all, "any":any, "bin":bin, "bool":bool, "chr":chr, "cmp":cmp, "complex":complex, "dict":dict, "dir":dir, "divmod":divmod, "enumerate":enumerate, "filter":filter, "float":float, "format":format, "frozenset":frozenset, "getattr":getattr, "hasattr":hasattr, "hex":hex, "int":int, "isinstance":isinstance, "issubclass":issubclass, "iter":iter, "len":len, "list":tuple, "long":long, "map":map, "mean": numpy.mean, "min":min, "max":max, "object":object, "oct":oct, "ord":ord, "pow":pow, "property":property, "range":range, "reduce":reduce, "repr":repr, "reversed":reversed, "round":round, "set": frozenset, "slice":slice, "sorted":sorted, "str":str, "sum":sum, "tuple":tuple, "type":type, "unichr":unichr, "unicode":unicode, "vars":vars, "xrange":xrange, "zip":zip}

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
    self.lock = thread.allocate_lock()
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


    # self.allvars = set()

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
    self.nxgraph = nx.DiGraph()

  def show_sets(self):
    print "deterministic: ", ppset(self.deterministic)
    print "probabilistic: ", ppset(self.probabilistic)
    print "builtin: ", ppset(self.builtin)
    print "imports: ", ppset(self.imports)
    print
    print "uptodate: ", ppset(self.uptodate)
    print "computing: ", ppset(self.computing)
    print "exception: ", ppset(self.exception)
    print "stale: ", ppset(self.stale)
    print
    print "private: ", ppset(self.private)
    print "releasable: ", ppset(self.releasable)
    print "privacy_unknown: ", ppset(self.privacy_unknown)
    print
    print "locals: ", ppset(self.locals.keys())
    print "globals: ", ppset(self.globals.keys())

  def changeState(self, name, newstate):
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
    else:
      raise Exception("Unknown state %s in changeState" % newstate)

  def updateState(self):
    '''
    anything that is currently uptodate but depends deterministically on a stale value or a computing value should be stale
    '''
    #_log.debug("Entering updateState")
    self.lock.acquire()
    changed = True
    while changed:
      changed = False
      variablestocheck = list(self.uptodate & self.deterministic) 
      for name in variablestocheck:
        if name in self.dependson:
          if (self.dependson[name] & (self.stale | self.computing)):
            self.changeState(name, "stale")
            changed = True

    # add code here to stop jobs that are computing but that are no longer needed

    self.lock.release()
    #_log.debug("Leaving updateState")

  def makeProbabilisticOnlyVariablesStale(self):
    #self.lock.acquire()
    for name in self.probabilistic - self.deterministic:
      self.changeState(name, "stale")
    #self.lock.release()
        
#  def updateGraph(self, name, dependson=[]):
#      self.lock.acquire()
#      # save a version of the current graph before making changes
#      save = self.graph.copy()
#
#      # Add variables and edges to graph data structure
#      vars = [name] + dependson
#      for var in vars:
#          if var not in self.graph:
#              self.graph.add_node(var)
#          if var != name:
#              self.graph.add_edge(var, name)
#
#      # Remove edges to old predecessors
#      preds = self.graph.predecessors(name)
#      for pred in preds:
#          if pred not in dependson:
#              self.graph.remove_edge(pred, name)
#
#      # Check for cycles
#      try:
#          cycles = nx.find_cycle(self.graph)
#          self.graph = save
#          self.lock.release()
#          return False, cycles
#      except:
#          self.lock.release()
#          return True, None

  def add_comment(self, name, the_comment):
    self.comment[name] = the_comment

  def define(self, name, code, dependson=None, prob = False, pyMC3code = None, private=False):
    _log.debug("Entering define {name}, {code}, {dependson}, {prob}, {pyMC3code}".format(**locals()))
    self.lock.acquire()
    if not dependson:
      dependson = []
    if prob:
      self.probabilistic.add(name)
      self.probcode[name] = code
      self.pyMC3code[name] = pyMC3code
      if dependson != []:
        self.probdependson[name] = set(dependson)
      self.makeProbabilisticOnlyVariablesStale()
      #if not name in self.uptodate:
      #  self.stale.add(name)
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
    # add code here to stop processes that depend on values that this define makes stale

    
    self.lock.release()
    self.updateState() 
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
      self.lock.release()
      self.updateState()

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
        res += str(self.globals[name])
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
    for parent in self.deterministic | self.probabilistic:
      if parent in self.probdependson:
        if name in self.probdependson[parent]:
          parents.append(parent)
      if parent in self.dependson and parent not in parents:
        if name in self.dependson[parent]:
          parents.append(parent)
    if parents == []:
      return False
    for d in parents:
      if d not in self.uptodate:
        if not self.checkup(d):
          return False
    return True

  def checkdown(self, name):
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

  def probbelow(self, name):
    '''
    Is there a probabilistic link anywhere below name.
    '''

    if name in self.probabilistic:
      return True
    if name not in self.probdependson.keys() and name not in self.dependson.keys():
      return False

    # check dependencies

    result = True
    if name in self.probdependson:
      for d in self.probdependson[name]:
        if d in self.probabilistic:
          return True
        else:
          result = result and self.checkdown(d)
    if name in self.dependson:
      for d in self.dependson[name]:
        if d in self.probabilistic:
          return True
        else:
          result = result and self.checkdown(d)
    return result

  def constructPyMC3code(self):
    locals = {}
    loggingcode = """
import logging
_log = logging.getLogger("pymc3")
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

    deterministic_not_uptodate = list(self.deterministic - self.uptodate)
    for name in deterministic_not_uptodate:
      code += "    " + name + " = " + self.code[name]+ "\n"

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

#  def canRunSampler(self, verbose=False):
#    #_log.debug("Entering canRunSampler")
#    result = True
#    for name in self.probdependson.keys():
#      if verbose: print name, "checkdown", self.checkdown(name)
#      result = result and self.checkdown(name)
#      if not name in self.uptodate:
#        if verbose: print name, "checkup", self.checkup(name)
#        result = result and self.checkup(name)
#    #_log.debug("Leaving canRunSampler: "+ str(result))
#    return result

  def canRunSampler(self, verbose=False):
    #_log.debug("Entering canRunSampler")
    result = True
    for name in self.variablesToBeSampled():
      if verbose: print name, "checkdown", self.checkdown(name)
      result = result and self.checkdown(name)
      if verbose: print name, "checkup", self.checkup(name)
      result = result and self.checkup(name)
    #_log.debug("Leaving canRunSampler: "+ str(result))
    return result

  def variablesToBeSampled(self):

    names = self.probabilistic - self.deterministic
    for name in self.deterministic:
      if name in self.dependson:
        if any(self.probbelow(d) for d in self.dependson[name]):
          names = names | set([name])
    return names

  def variablesToBeCalculated(self):
    names = set([])
    for name in self.deterministic:
      if name not in self.dependson:
        names.add(name)
      else:
        for d in self.dependson[name]:
            if all(not self.probbelow(d) and (d in self.uptodate or d in self.imports or d in self.builtin) for d in self.dependson[name]):
              names.add(name)
    return(names)

    
  def compute(self):


    """
    _log.debug("Entering compute")
    self.lock.acquire()
    stales = list(self.stale)

    # do deterministic variables with no probabilsitic dependencies in their tree

    #_log.debug("compute: Do deterministic variables")
    for name in self.deterministic:
        if name in self.stale:
          if name not in self.dependson:
            self.changeState(name, "computing")
            self.jobs[name] = self.server.submit(job, (name, self.code[name], self.globals, self.locals), callback=self.callback)
          else:
            for d in self.dependson[name]:
              _log.debug("### "+ name + " " + d + " " + str(not self.probbelow(d)) + " " + str(d in self.uptodate) + " " + str(d in self.imports) + " " + str(d in self.builtin))
            if all(not self.probbelow(d) and (d in self.uptodate or d in self.imports or d in self.builtin) for d in self.dependson[name]):
              self.changeState(name, "computing")
              self.jobs[name] = self.server.submit(job, (name, self.code[name], self.globals, self.locals), callback=self.callback)


    # do variables that require the sampler
    # that is variables that are probabilistic only or have deterministic dependencies 
    # that have probabilistic dependencies in their tree

    #_log.debug("compute: Do probabilistic variables")
    sampler_names = self.probabilistic 
    for name in self.dependson.keys():
       for d in self.dependson[name]:
         
    if len(uncalculated_unobserved_names) > 0:  # there are some probabilistic variables to calculate
      if self.canRunSampler(): # all necessary dependencies for all probabilistic variables have been defined or computed
        locals, sampler_code =  self.constructPyMC3code()
        for name in unobserved_names:
          self.changeState(name, "computing")
        self.jobs["__private_sampler__"] = self.server.submit(samplerjob, (unobserved_names, sampler_code, self.globals, locals), callback=self.samplercallback)

    self.lock.release()
    self.updateState()
    _log.debug("Leaving compute")
"""
    #_log.debug("Entering compute")
    self.lock.acquire()

    for name in self.variablesToBeCalculated() & self.stale:
      _log.debug("Starting " + name)
      self.changeState(name, "computing")
      self.jobs[name] = self.server.submit(job, (name, self.code[name], self.globals, self.locals), callback=self.callback)
      
    
    sampler_names = self.variablesToBeSampled()
    if sampler_names & self.stale != set([]):
      if self.canRunSampler(): # all necessary dependencies for all probabilistic variables have been defined or computed
        locals, sampler_code =  self.constructPyMC3code()
        for name in sampler_names:
          self.changeState(name, "computing")
        self.jobs["__private_sampler__"] = self.server.submit(samplerjob, (sampler_names, sampler_code, self.globals, locals), callback=self.samplercallback)

    self.lock.release()
    self.updateState()
    #_log.debug("Leaving compute")

  def isException(self, v):
    return type(v) in [SyntaxError, ValueError, NameError, TypeError]

  def callback(self, returnvalue):
    self.lock.acquire()
    name, value = returnvalue
    if self.isException(value):
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
    if self.isException(value):
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
