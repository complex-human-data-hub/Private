import numpy.random
import numpy
from event import Event
from demo_events import Events, DemoEvents
import seaborn
import matplotlib.pyplot as plt
import io

def Normal(mu, sigma, length):
  return(numpy.random.normal(mu, sigma, length))

def distplot(x):
  seaborn.distplot(x)
  buf = io.BytesIO()
  plt.savefig(buf, format="png")
  return buf

builtins = {"distplot": distplot, "NumberOfTuningSamples": 200, "NumberOfChains": 2, "NumberOfSamples": 200, "DemoEvents": DemoEvents, "Events": Events, "Event": Event, "mean": numpy.mean, "std":numpy.std, "Normal": Normal, "Event": Event, "abs": abs, "all": all, "any":any, "bin":bin, "bool":bool, "chr":chr, "cmp":cmp, "complex":complex, "dict":dict, "dir":dir, "divmod":divmod, "enumerate":enumerate, "filter":filter, "float":float, "format":format, "frozenset":frozenset, "getattr":getattr, "hasattr":hasattr, "hex":hex, "int":int, "isinstance":isinstance, "issubclass":issubclass, "iter":iter, "len":len, "list":tuple, "long":long, "map":map, "min":min, "max":max, "object":object, "oct":oct, "ord":ord, "pow":pow, "property":property, "range":range, "reduce":reduce, "repr":repr, "reversed":reversed, "round":round, "set": frozenset, "slice":slice, "sorted":sorted, "str":str, "sum":sum, "tuple":tuple, "type":type, "unichr":unichr, "unicode":unicode, "vars":vars, "xrange":xrange, "zip":zip}

prob_builtins = set(["Normal", "HalfNormal", "Uniform", "SkewNormal", "Beta", "Kumaraswamy", "Exponential", "Laplace", "StudentT", "halfStudentT", "Cauchy", "HalfCauchy", "Gamma", "Weibull", "Lognormal", "ChiSquared", "Wald", "Pareto", "InverseGamma", "Exgaussian", "VonMises", "Triangular", "Gumbel", "Logistic", "LogitNormal"]) # continuous distributions
prob_builtins = prob_builtins | set(["Binomial", "ZeroInflatedBinomial", "Bernoulli", "Poisson", "ZeroInflatedPoisson", "NegativeBinomial", "ZeroInflatedNegativeBinomial", "DiscreteUniform", "Geometric", "Categorical", "DiscreteWeibull", "Constant", "OrderedLogistic"]) # discrete distributions

def setPrivacy(graph):
  for name in builtins:
    graph.changePrivacy(name, "public")
  for name in prob_builtins:
    graph.changePrivacy(name, "public")
 
  graph.changePrivacy("Events", "private")

def showNames(names, width=120):
  res = ""
  names.sort()
  columnWidth = max(len(s) for s in names)+2
  numColumns = width / columnWidth
  
  numRows = len(names) / numColumns
  rows = [""] * numRows
  for i, name in enumerate(names):
    rows[i%numRows] += name.ljust(columnWidth)
  return "\n".join(rows)

def showBuiltins():
  print "Builtins\n"
  print showNames(builtins.keys())
  print

def showProbBuiltins():
  print "Probabilistic Builtins\n"
  print showNames(list(prob_builtins))
  print

