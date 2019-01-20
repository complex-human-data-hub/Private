import numpy.random
import numpy
from event import Event
from demo_events import Events, DemoEvents
import seaborn
import matplotlib.pyplot as plt
import io
import pymc3 as pm

# Deterministic Continuous Distribution Definitions

def Uniform(lower, upper, size):
  y = pm.Uniform.dist(lower, upper)
  return y.random(size=size)

def Normal(mu, sd, size):
  y = pm.Normal.dist(mu, sd)
  return y.random(size=size)

def HalfNormal(sd, size):
  y = pm.HalfNormal.dist(sd)
  return y.random(size=size)

def SkewNormal(mu, sd, alpha, size):
  y = pm.SkewNormal.dist(mu=mu, sd=sd, alpha=alpha)
  return y.random(size=size)

def Beta(mu, sd, size):
  y = pm.Beta.dist(mu=mu, sd=sd)
  return y.random(size=size)

def Kumaraswamy(a, b, size):
  y = pm.Kumaraswamy.dist(a, b)
  return y.random(size=size)

def Exponential(lam, size):
  y = pm.Exponential.dist(lam)
  return y.random(size=size)

def Laplace(mu, b, size):
  y = pm.Laplace.dist(mu, b)
  return y.random(size=size)

def StudentT(nu, size):
  y = pm.StudentT.dist(nu)
  return y.random(size=size)

def HalfStudentT(nu, size):
  y = pm.HalfStudentT.dist(nu)
  return y.random(size=size)

def Cauchy(alpha, beta, size):
  y = pm.Cauchy.dist(alpha, beta)
  return y.random(size=size)

def HalfCauchy(beta, size):
  y = pm.HalfCauchy.dist(beta)
  return y.random(size=size)

def Gamma(mu, sd, size):
  y = pm.Gamma.dist(mu, sd)
  return y.random(size=size)

def Weibull(alpha, beta, size):
  y = pm.Weibull.dist(alpha, beta)
  return y.random(size=size)

def LogNormal(mu, sd, size):
  y = pm.Lognormal.dist(mu=mu, sd=sd)
  return y.random(size=size)

def ChiSquared(nu, size):
  y = pm.ChiSquared.dist(nu)
  return y.random(size=size)

def Wald(mu, lam, size):
  y = pm.Wald.dist(mu, lam)
  return y.random(size=size)

def Pareto(alpha, m, size):
  y = pm.Pareto.dist(alpha, m)
  return y.random(size=size)

def InverseGamma(mu, sd, size):
  y = pm.InverseGamma.dist(mu, sd)
  return y.random(size=size)

def ExGaussian(mu, sd, nu, size):
  y = pm.ExGaussian.dist(mu, sd, nu)
  return y.random(size=size)

def Triangular(lower, upper, c, size):
  y = pm.Triangular.dist(lower, upper, c)
  return y.random(size=size)

def Gumbel(mu, beta, size):
  y = pm.Gumbel.dist(mu, beta)
  return y.random(size=size)

def Logistic(mu, s, size):
  y = pm.Logistic.dist(mu, s)
  return y.random(size=size)

def LogitNormal(mu, sd, size):
  y = pm.LogitNormal.dist(mu, sd)
  return y.random(size=size)

# Deterministic Discrete  Distribution Definitions

def Binomial(n, p, size):
  y = pm.Binomial.dist(n, p)
  return y.random(size=size)

def ZeroInflatedBinomial(psi, n, p, size):
  y = pm.ZeroInflatedBinomial.dist(psi, n, p)
  return y.random(size=size)

def BetaBinomial(alpha, beta, n, size):
  y = pm.BetaBinomial.dist(alpha, beta, n)
  return y.random(size=size)

def Bernoulli(p, size):
  y = pm.Bernoulli.dist(p)
  return y.random(size=size)

def Poisson(mu, size):
  y = pm.Poisson.dist(mu)
  return y.random(size=size)

def ZeroInflatedPoisson(psi, mu, size):
  y = pm.ZeroInflatedPoisson.dist(psi, mu)
  return y.random(size=size)

def NegativeBinomial(mu, alpha, size):
  y = pm.NegativeBinomial.dist(mu, alpha)
  return y.random(size=size)

def ZeroInflatedNegativeBinomial(psi, mu, alpha, size):
  y = pm.ZeroInflatedNegativeBinomial.dist(psi, mu, alpha)
  return y.random(size=size)

def DiscreteUniform(upper, lower, size):
  y = pm.DiscreteUniform.dist(upper, lower)
  return y.random(size=size)

def Geometric(p, size):
  y = pm.Geometric.dist(p)
  return y.random(size=size)

def Categorical(p, size):
  y = pm.Categorical.dist(p)
  return y.random(size=size)

def DiscreteWeibull(q, beta, size):
  y = pm.DiscreteWeibull.dist(q, beta)
  return y.random(size=size)

def Constant(c, size):
  y = pm.Constant.dist(c)
  return y.random(size=size)

# Plotting Function Definitions

def distplot(x):  # have to stop this plotting if x is Private
  seaborn.distplot(x)
  buf = io.BytesIO()
  plt.savefig(buf, format="png")
  plt.close()
  return buf

def private_mean(x):
  return numpy.mean(x)

def private_median(x):
  return numpy.median(x)

def private_std(x):
  return numpy.std(x)

def private_abs(x):
  return abs(x)

def private_all(x):
  return all(x)

def private_any(x):
  return any(x)

def private_bin(x):
  return bin(x)

def private_bool(x):
  return bool(x)

def private_chr(x):
  return chr(x)

def private_cmp(x):
  return cmp(x)

def private_complex(x):
  return complex(x)

def private_dict(x):
  return dict(x)

def private_divmod(x):
  return divmod(x)

def private_enumerate(x):
  return list(enumerate(x))

def private_exp(x):
  return numpy.exp(x)

def private_filter(x):
  return filter(x)

def private_float(x):
  return float(x)

def private_format(x):
  return format(x)

def private_frozenset(x):
  return frozenset(x)

def private_getattr(x):
  return getattr(x)

def private_hasattr(x):
  return hasattr(x)

def private_hex(x):
  return hex(x)

def private_int(x):
  return int(x)

def private_isinstance(x):
  return isinstance(x)

def private_issubclass(x):
  return issubclass(x)

def private_iter(x):
  return iter(x)

def private_len(x):
  return len(x)

def private_list(x):
  return tuple(x)

def private_long(x):
  return long(x)

def private_map(x):
  return map(x)

def private_min(x):
  return min(x)

def private_max(x):
  return max(x)

def private_object(x):
  return object(x)

def private_oct(x):
  return oct(x)

def private_ord(x):
  return ord(x)

def private_pow(x):
  return pow(x)

def private_property(x):
  return property(x)

def private_range(x):
  return range(x)

def private_reduce(x):
  return reduce(x)

def private_repr(x):
  return repr(x)

def private_reversed(x):
  return reversed(x)

def private_round(x):
  return round(x)

def private_set(x):
  return frozenset(x)

def private_slice(x):
  return slice(x)

def private_sorted(x):
  return sorted(x)

def private_str(x):
  return str(x)

def private_sum(x):
  return sum(x)

def private_tuple(x):
  return tuple(x)

def private_type(x):
  return type(x)

def private_unichr(x):
  return unichr(x)

def private_unicode(x):
  return unicode(x)

def private_vars(x):
  return vars(x)

def private_xrange(x):
  return xrange(x)

def private_zip(x):
  return zip(x)


builtins = {\

            # make __bultins__ None
            # this is crucial to stop __builtins__ being available in eval code

            "__builtins__": None,
            "__import__": __import__,
            "Exception": Exception,

            "True": True,
            "False": False,

            # Deterministic Continuous Distributions

            "Uniform": Uniform, \
            "Normal": Normal, \
            "HalfNormal": HalfNormal, \
            "SkewNormal": SkewNormal, \
            "Beta": Beta, \
            "Kumaraswamy": Kumaraswamy, \
            "Exponential": Exponential, \
            "Laplace": Laplace, \
            "StudentT": StudentT, \
            "HalfStudentT": HalfStudentT, \
            "Cauchy": Cauchy, \
            "HalfCauchy": HalfCauchy, \
            "Gamma": Gamma, \
            "Weibull": Weibull, \
            "LogNormal": LogNormal, \
            "ChiSquared": ChiSquared, \
            "Wald": Wald, \
            "Pareto": Pareto, \
            "InverseGamma": InverseGamma, \
            "ExGaussian": ExGaussian, \
            "Triangular": Triangular, \
            "Gumbel": Gumbel, \
            "Logistic": Logistic, \
            "LogitNormal": LogitNormal, \

            # Deterministic Discrete Distributions

            "Binomial": Binomial, \
            "ZeroInflatedBinomial": ZeroInflatedBinomial, \
            "BetaBinomial": BetaBinomial, \
            "Bernoulli": Bernoulli, \
            "Poisson": Poisson, \
            "ZeroInflatedPoisson": ZeroInflatedPoisson, \
            "NegativeBinomial": NegativeBinomial, \
            "ZeroInflatedNegativeBinomial": ZeroInflatedNegativeBinomial, \
            "DiscreteUniform": DiscreteUniform, \
            "Geometric": Geometric, \
            "Categorical": Categorical, \
            "DiscreteWeibull": DiscreteWeibull, \
            "Constant": Constant, \

            # Plotting Functions

            "distplot": distplot, \

            # Control of Sampler 

            "NumberOfTuningSamples": 200, \
            "NumberOfChains": 2, \
            "NumberOfSamples": 200, \

            # Data

            "DemoEvents": DemoEvents, \
            "Events": Events, \
            "Event": Event, \

            # Summary Statistics

            "mean": private_mean, \
            "median": private_median, \
            "std": private_std, \

            # Standard python builtins that don't generate privacy problems

            "abs": private_abs, \
            "all": private_all, \
            "any":private_any, \
            "bin":private_bin, \
            "bool":private_bool, \
            "chr":private_chr, \
            "cmp":private_cmp, \
            "complex":private_complex, \
            "dict":private_dict, \
            "divmod":private_divmod, \
            "enumerate":private_enumerate, \
            "exp":private_exp, \
            "filter":private_filter, \
            "float":private_float, \
            "format":private_format, \
            "frozenset":private_frozenset, \
            "getattr":private_getattr, \
            "hasattr":private_hasattr, \
            "hex":private_hex, \
            "int":private_int, \
            "isinstance":private_isinstance, \
            "issubclass":private_issubclass, \
            "iter":private_iter, \
            "len":private_len, \
            "list":private_tuple, \
            "long":private_long, \
            "map":private_map, \
            "min":private_min, \
            "max":private_max, \
            "object":private_object, \
            "oct":private_oct, \
            "ord":private_ord, \
            "pow":private_pow, \
            "property":private_property, \
            "range":private_range, \
            "reduce":private_reduce, \
            "repr":private_repr, \
            "reversed":private_reversed, \
            "round":private_round, \
            "set": private_frozenset, \
            "slice":private_slice, \
            "sorted":private_sorted, \
            "str":private_str, \
            "sum":private_sum, \
            "tuple":private_tuple, \
            "type":private_type, \
            "unichr":private_unichr, \
            "unicode":private_unicode, \
            "vars":private_vars, \
            "xrange":private_xrange, \
            "zip":private_zip}

prob_builtins = set(["Normal", "HalfNormal", "Uniform", "SkewNormal", "Beta", "Kumaraswamy", "Exponential", "Laplace", "StudentT", "HalfStudentT", "Cauchy", "HalfCauchy", "Gamma", "Weibull", "Lognormal", "ChiSquared", "Wald", "Pareto", "InverseGamma", "Exgaussian", "VonMises", "Triangular", "Gumbel", "Logistic", "LogitNormal"]) # continuous distributions
prob_builtins = prob_builtins | set(["Binomial", "ZeroInflatedBinomial", "Bernoulli", "Poisson", "ZeroInflatedPoisson", "NegativeBinomial", "ZeroInflatedNegativeBinomial", "DiscreteUniform", "Geometric", "Categorical", "DiscreteWeibull", "Constant", "OrderedLogistic"]) # discrete distributions

def setBuiltinPrivacy(graph):
  for name in builtins:
    graph.setPrivacy(name, "public")
  for name in prob_builtins:
    graph.setPrivacy(name, "public")
 
  graph.setPrivacy("Events", "private")

def showNames(names, width=80):
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
  res = "Builtins\n\n"
  res += showNames(builtins.keys())
  return res

def showProbBuiltins():
  res = "Probabilistic Builtins\n\n"
  res += showNames(list(prob_builtins))
  return res

