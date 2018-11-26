import thread
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

logging.basicConfig(filename='private.log',level=logging.WARNING)

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
    self.globals = copy.copy(builtins)
    self.locals = {}


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

    # each variable should be in private, public, privacy_unknown

    self.private = set()
    self.public = set()
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
    self.sampler_chains = {}
    self.server = pp.Server()
    self.log = logging.getLogger("Private")
    #self.nxgraph = nx.DiGraph()

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

  def changeState(self, name, newstate):
    self.log.debug("Change state of %s to %s." % (name, newstate))
    self.uptodate.discard(name)
    self.computing.discard(name)
    self.exception.discard(name)
    self.stale.discard(name)
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
        #print name, " det ", self.deterministicParents(name)
        if parent not in self.stale:
          self.changeState(parent, "stale")
      for child in self.probabilisticChildren(name): # children via probabilistic links
        #print name, " prob ", self.deterministicParents(name)
        if child not in self.stale and child not in self.builtins:
          self.changeState(child, "stale")
    else:
      raise Exception("Unknown state %s in changeState" % newstate)

  def changePrivacy(self, name, privacy):
    self.private.discard(name)
    self.public.discard(name)
    self.privacy_unknown.discard(name)
      
    if privacy == "private":
      self.private.add(name)
    elif privacy == "public":
      self.public.add(name)
    else:
      if name in self.deterministic:
        # first look at deterministic children to see if you can deduce the privacy value
        if name in self.dependson:
          if all(child in self.public for child in self.dependson[name]):
            self.public.add(name)
          elif any(child in self.private for child in self.dependson[name]):
            self.private.add(name)
          else:
            self.privacy_unknown.add(name)
        else: # there are no determinsitic dependancies
          self.public.add(name)
      else: # probabilistic
        if all(parent in self.public for parent in self.getParents(name)) and all(child in self.public for child in self.getChildren(name)):
          self.public.add(name)
        else:
          self.privacy_unknown.add(name)

    # propagate privacy to parents
    for parent in self.getParents(name):
      self.changePrivacy(parent, "privacy_unknown")

  def add_comment(self, name, the_comment):
    self.comment[name] = the_comment

  def define(self, name, code, dependson=None, prob = False, pyMC3code = None, privacy="privacy_unknown"):
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
        for n in self.probabilistic - self.deterministic:
          self.changeState(n, "stale")
    else:
      self.deterministic.add(name)
      self.code[name] = code
      self.dependson[name] = set(dependson)
      self.changeState(name, "stale")
    self.changePrivacy(name, privacy)
    self.lock.release()

  def delete(self, name):
    self.lock.acquire()
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
      if name in self.stale:
        res += "Stale"
      elif name in self.computing:
        res += "Computing"
      elif name in self.exception: # note an exception might reveal information about the value so might only be able to show this if the variable is public
        res += str(self.globals[name])
      elif name in self.private:
        res += "Private"
      elif name in self.privacy_unknown:
        res += "Privacy Unknown"
      elif name in self.uptodate:
        if type(self.globals[name]) == numpy.ndarray:
          s = self.globals[name].shape
          res += "[" * len(s) + "%f" % self.globals[name].ravel()[0] + " ... " + "%f" % self.globals[name].ravel()[-1] + "]" * len(s)
        else:
          res += reprlib.repr(self.globals[name])
      else:
        raise Exception(name + " is not stale, computing, exception or uptodate.")
    elif name in self.builtins:
      if name in self.public:
        res += reprlib.repr(self.globals[name])
      else:
        res += "Private"
    else:
      raise Exception("Unknown variable " + name)
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
        valuebits.append(self.getValue(name)[0:codewidth])
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

    nonuptodatechildren = self.getChildren(name) - self.uptodate - prob_builtins
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
        if d not in self.uptodate and d not in prob_builtins:
          result = result and self.checkdown(d)
    if name in self.dependson:
      for d in self.dependson[name]:
        if d not in self.uptodate and d not in prob_builtins:
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

    code = loggingcode + """
import pymc3 as pm


try:

  basic_model = pm.Model()

  with basic_model:

    exception_variable = None
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
    __private_result__ = pm.sample({NumberOfSamples}, tune={NumberOfTuningSamples}, chains={NumberOfChains}, random_seed=987654321, progressbar = False)

except Exception as e:
  # remove stuff after the : as that sometimes reveals private information
  ind = e.args[0].find(":")
  if ind != -1:
    estring = e.args[0][0:ind]
  else:
    estring = e.args[0]
    
  newErrorString = "Problem with %s: %s" % (exception_variable, estring)
  e.args = (newErrorString,)
  __private_result__ = e

""".format(NumberOfSamples=self.globals["NumberOfSamples"], NumberOfChains=self.globals["NumberOfChains"], NumberOfTuningSamples=self.globals["NumberOfTuningSamples"])
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
      #print name, self.dependson.get(name, set([])) , self.uptodate , self.builtins
      if self.dependson.get(name, set([])) - self.uptodate - self.builtins == set([]):
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
          myname = "__private_sampler__"
          self.sampler_chains[myname] = None
          self.jobs["__private_sampler__"] = self.server.submit(samplerjob, (myname, sampler_names, sampler_code, self.globals, locals), callback=self.samplercallback)
          if len(self.privacy_unknown) != 0:
            print "privacy to be figured", self.privacy_unknown
            AllEvents = self.globals["Events"]
            users = set([e.UserId for e in AllEvents])
            for user in users:
              #print "remove " + user
              self.globals["Events"] = [e for e in AllEvents if e.UserId != user]
              myname = "__private_sampler__ " + user
              self.sampler_chains[myname] = None
              self.jobs[myname] = self.server.submit(samplerjob, (myname, sampler_names, sampler_code, self.globals, locals), callback=self.privacysamplercallback)
            self.globals["Events"] = AllEvents # make sure to set globals["Events"] back to the entire data set on completion
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

  def samplercallback(self, returnvalue):  
    self.log.debug("samplercallback")
    self.lock.acquire()
    myname, names, value = returnvalue
    #print "samplercallback: ", myname
    if isinstance(value, Exception):
      for name in names:
        self.globals[name] = str(value)
        self.changeState(name, "exception")
    else: # successful sampler return
      tochecknames = list(self.privacy_unknown & set(names))   # names to check for privacy
      self.log.debug(str(tochecknames))
      if len(tochecknames) > 0:
        samples = value[tochecknames[0]]
        self.log.debug(str(samples))
        for i in xrange(1,len(tochecknames)):
          samples.concatenate(value[tochecknames[i]])
        self.sampler_chains[myname] = samples
        #self.show_sampler_chains()

      for name in names:
        if name in value.varnames:
          self.globals[name] = value[name]
        else:
          self.globals[name] = "Not retained."
          
        self.changeState(name, "uptodate")

    del self.jobs["__private_sampler__"]
    self.lock.release()
    self.compute()

  def show_sampler_chains(self):
    print(str(len(self.sampler_chains)) + " chains")
    try:
      for k,v in self.sampler_chains.items():
        if type(v) == str:
          print( k+ " " + str(v))
        elif type(v) == numpy.ndarray:
          print( k+ " array")
        elif v == None:
          print( k+ " None")
        else:
          print "Unknown value type"
    except Exception as e:
        print "here", e
        traceback.print_exc()

  def privacysamplercallback(self, returnvalue):  
    self.lock.acquire()
    myname, names, value = returnvalue
    #print "privacysamplercallback: ", myname
    tochecknames = list(self.privacy_unknown & set(names))
    samples = value[tochecknames[0]]
    for i in xrange(1,len(tochecknames)):
      samples.concatenate(value[tochecknames[i]])
    self.sampler_chains[myname] = samples
    if type(self.sampler_chains["__private_sampler__"]) == numpy.ndarray:
      for usertest in self.sampler_chains.keys():
        #print "Check " + usertest
        if usertest != "__private_sampler__":
          if type(self.sampler_chains[usertest]) == numpy.ndarray:
            #print "Calculating distManifold " + usertest
            #print self.sampler_chains[usertest]
            #print self.sampler_chains["__private_sampler__"]
            try:
              d = distManifold(self.sampler_chains[usertest], self.sampler_chains["__private_sampler__"]) * 100.
            except Exception as e:
              print e
            #print d
            if d < 4.:
              self.sampler_chains[usertest] = "public"
              #print "public"
            else:
              self.sampler_chains[usertest] = "private"
              #print "private"
 
    if all(False if type(v) == numpy.ndarray else v == "public" for k,v in self.sampler_chains.items() if k != "__private_sampler__"):
      for name in tochecknames:
        self.changePrivacy(name, "public")
    elif any(False if type(v) == numpy.ndarray else v == "private" for k,v in self.sampler_chains.items() if k != "__private_sampler__"):
      for name in tochecknames:
        self.changePrivacy(name, "private")

    #self.show_sampler_chains()
    del self.jobs[myname]
    self.lock.release()
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
    return (myname, names, locals["__private_result__"])
  except Exception as e:
    return (myname, names, e)

depGraph = graph()
setPrivacy(depGraph) # set privacy of builtins
