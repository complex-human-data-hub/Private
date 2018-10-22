import _thread
import pp
import logging as l
import networkx as nx

class graph:

  def __init__(self):
     self.lock = _thread.allocate_lock()
     self.value = {}
     self.stale = set() # either stale, computing or uptodate   - maybe colour red, orange, and green
     self.computing = set()
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
      uptodates = list(self.uptodate)
      for name in uptodates:
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

  def define(self, name, code, dependson=[]):
    self.lock.acquire()
    self.code[name] = code
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





  def __str__(self):
    res = ""
    for name in self.code.keys():
      if name in self.stale:
        res += name + " [Stale] "
      elif name in self.computing:
        res += name + " [Computing] "
      else:
        res += name + " = " + str(self.value[name])
      res += "    " + self.code[name]
      if self.dependson[name] != set([]):
        res += "    " + str(self.dependson[name])
      res += "\n"
    return(res)

  def compute(self):
    self.lock.acquire()
    stales = list(self.stale)
    for name in stales:
      if all([d in self.uptodate for d in self.dependson[name]]):
        self.stale.remove(name)
        self.computing.add(name)
        self.jobs[name] = self.server.submit(job, (name, self.code[name], self.value), callback=self.callback)
    self.lock.release()

  def callback(self, returnvalue):
    self.lock.acquire()
    name, value = returnvalue
    self.value[name] = value
    del self.jobs[name]
    self.computing.remove(name)
    self.uptodate.add(name)
    self.lock.release()
    self.compute()

def job(name, code, value):
  value = eval(code, None, value)
  return((name, value))

def setup():
  g = graph()
  g.define("a", "b * c", dependson = ["b", "c"])
  g.define("b", "2")
  g.define("c", "4")
  return(g)
