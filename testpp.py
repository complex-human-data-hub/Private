import thread
import pp
import logging as l
import networkx as nx
import repr as reprmodule

__private_builtins__ = {"abs": abs, "all": all, "any":any, "bin":bin, "bool":bool, "chr":chr, "cmp":cmp, "complex":complex, "dict":dict, "dir":dir, "divmod":divmod, "enumerate":enumerate, "filter":filter, "float":float, "format":format, "frozenset":frozenset, "getattr":getattr, "globals":globals, "hasattr":hasattr, "hex":hex, "int":int, "isinstance":isinstance, "issubclass":issubclass, "iter":iter, "len":len, "list":tuple, "locals":locals, "long":long, "map":map, "min":min, "max":max, "object":object, "oct":oct, "ord":ord, "pow":pow, "property":property, "range":range, "reduce":reduce, "repr":repr, "reversed":reversed, "round":round, "set": frozenset, "slice":slice, "sorted":sorted, "str":str, "sum":sum, "super":super, "tuple":tuple, "type":type, "unichr":unichr, "unicode":unicode, "vars":vars, "xrange":xrange, "zip":zip}

__private_dependson__ = dict(zip(__private_builtins__.keys(), [set([])]*len(__private_builtins__)))

reprmodule.aRepr.maxstring= 50

class graph:

  def __init__(self):
     self.lock = thread.allocate_lock()
     self.globals = __private_builtins__
     self.locals = {}
     self.stale = set() # either stale, computing, exception or uptodate   - maybe colour red, orange, and green
     self.computing = set()
     self.exception = set()
     self.uptodate = set()
     self.code = {}
     self.dependson = {}
     self.jobs = {}
     self.server = pp.Server()
     self.graph = nx.DiGraph()

  def updateState(self):
    '''
    anything that is currently uptodate but depends on a stale value or a computing value should be stale
    '''

    self.lock.acquire()
    changed = True
    while changed:
      changed = False
      variablestocheck = list(self.uptodate-set(self.globals.keys())) # note globals are always uptodate
      for name in variablestocheck:
        if (self.dependson[name] & (self.stale | self.computing)):
          self.stale.add(name)
          self.uptodate.remove(name)
          changed = True

    # add code here to stop jobs that are computing but that are no longer needed

    self.lock.release()

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

  def define(self, name, code, dependson=None):
    self.lock.acquire()
    self.code[name] = code
    if not dependson:
      dependson = []
    self.dependson[name] = set(dependson)
    self.stale.add(name)
    if name in self.uptodate:
      self.uptodate.remove(name)
    # add code here to stop processes that depend on values that this define makes stale
    self.lock.release()
    self.updateState()   # this has to be outside lock

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

  def hasVariable(self, variable):
    return variable in self.code.keys()

  def getValue(self, name):
    res = ""
    if self.hasVariable(name):
      if name in self.stale:
        res += "Stale"
      elif name in self.computing:
        res += "Computing"
      elif name in self.exception:
        #res += reprmodule.repr(self.locals[name])
        res += str(self.locals[name])
      else:
        #res += reprmodule.repr(self.locals[name])
        res += str(self.locals[name])
    else:
      raise Exception("Unknown variable " + name)
    return res
      
  def __repr__(self):
    res = ""
    for name in self.code.keys():
      res += name + " = "
      res += self.getValue(name)
      #res += "    " + reprmodule.repr(self.code[name])
      res += "    " + str(self.code[name])
      if self.dependson[name] != set([]):
        res += "    " + str(list(self.dependson[name]))
      res += "\n"
    return(res[0:-1])

  def compute(self):
    self.lock.acquire()
    stales = list(self.stale)
    for name in stales:
      if all([(d in self.uptodate or d in self.globals) for d in self.dependson[name]]):
        self.stale.remove(name)
        self.computing.add(name)
        self.jobs[name] = self.server.submit(job, (name, self.code[name], self.globals, self.locals), callback=self.callback)
    self.lock.release()

  def callback(self, returnvalue):
    self.lock.acquire()
    name, value = returnvalue
    if type(value) == Exception:
      self.locals[name] = str(value)
      self.computing.remove(name)
      self.exception.add(name)
    else:
      self.locals[name] = value
      del self.jobs[name]
      self.computing.remove(name)
      self.uptodate.add(name)

    self.lock.release()
    self.compute()

def job(name, code, globals, locals):
  try:
    value = eval(code, globals, locals)
    return((name, value))
  except Exception as e:
    return((name, e))

def setup():
  g = graph()
  g.define("a", "b * c", dependson = ["b", "c"])
  g.define("b", "2")
  g.define("c", "4")
  return(g)
