import numpy.random
import numpy


def Normal(mu, sigma, length):
  return(numpy.random.normal(mu, sigma, length))

class Event:

  def __init__(self, mydict):
    self.__dict__ = mydict

  def __repr__(self):
    return repr(self.__dict__)

  def hasField(self, fieldname):
    return fieldname in self.__dict__.keys()


__private_builtins__ = {"Event": Event, "mean": numpy.mean, "std":numpy.std, "Normal": Normal, "Event": Event, "abs": abs, "all": all, "any":any, "bin":bin, "bool":bool, "chr":chr, "cmp":cmp, "complex":complex, "dict":dict, "dir":dir, "divmod":divmod, "enumerate":enumerate, "filter":filter, "float":float, "format":format, "frozenset":frozenset, "getattr":getattr, "hasattr":hasattr, "hex":hex, "int":int, "isinstance":isinstance, "issubclass":issubclass, "iter":iter, "len":len, "list":tuple, "long":long, "map":map, "min":min, "max":max, "object":object, "oct":oct, "ord":ord, "pow":pow, "property":property, "range":range, "reduce":reduce, "repr":repr, "reversed":reversed, "round":round, "set": frozenset, "slice":slice, "sorted":sorted, "str":str, "sum":sum, "tuple":tuple, "type":type, "unichr":unichr, "unicode":unicode, "vars":vars, "xrange":xrange, "zip":zip}

__private_prob_builtins__ = set(["Normal", "HalfNormal", "Uniform", "SkewNormal", "Beta", "Kumaraswamy", "Exponential", "Laplace", "StudentT", "halfStudentT", "Cauchy", "HalfCauchy", "Gamma", "Weibull", "Lognormal", "ChiSquared", "Wald", "Pareto", "InverseGamma", "Exgaussian", "VonMises", "Triangular", "Gumbel", "Logistic", "LogitNormal"]) # continuous distributions
__private_prob_builtins__ = __private_prob_builtins__ | set(["Binomial", "ZeroInflatedBinomial", "Bernoulli", "Poisson", "ZeroInflatedPoisson", "NegativeBinomial", "ZeroInflatedNegativeBinomial", "DiscreteUniform", "Geometric", "Categorical", "DiscreteWeibull", "Constant", "OrderedLogistic"]) # discrete distributions

