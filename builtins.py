import numpy.random
import numpy
from event import Event
from demo_events import Events, DemoEvents
import seaborn
import matplotlib.pyplot as plt
import io
import pymc3 as pm

# Deterministic Continuous Distribution Definitions

def Uniform(argnames, lower, upper, size):
  y = pm.Uniform.dist(lower, upper)
  return y.random(size=size)

def Normal(argnames, mu, sd, size):
  y = pm.Normal.dist(mu, sd)
  return y.random(size=size)

def HalfNormal(argnames, sd, size):
  y = pm.HalfNormal.dist(sd)
  return y.random(size=size)

def SkewNormal(argnames, mu, sd, alpha, size):
  y = pm.SkewNormal.dist(mu=mu, sd=sd, alpha=alpha)
  return y.random(size=size)

def Beta(argnames, mu, sd, size):
  y = pm.Beta.dist(mu=mu, sd=sd)
  return y.random(size=size)

def Kumaraswamy(argnames, a, b, size):
  y = pm.Kumaraswamy.dist(a, b)
  return y.random(size=size)

def Exponential(argnames, lam, size):
  y = pm.Exponential.dist(lam)
  return y.random(size=size)

def Laplace(argnames, mu, b, size):
  y = pm.Laplace.dist(mu, b)
  return y.random(size=size)

def StudentT(argnames, nu, size):
  y = pm.StudentT.dist(nu)
  return y.random(size=size)

def HalfStudentT(argnames, nu, size):
  y = pm.HalfStudentT.dist(nu)
  return y.random(size=size)

def Cauchy(argnames, alpha, beta, size):
  y = pm.Cauchy.dist(alpha, beta)
  return y.random(size=size)

def HalfCauchy(argnames, beta, size):
  y = pm.HalfCauchy.dist(beta)
  return y.random(size=size)

def Gamma(argnames, mu, sd, size):
  y = pm.Gamma.dist(mu, sd)
  return y.random(size=size)

def Weibull(argnames, alpha, beta, size):
  y = pm.Weibull.dist(alpha, beta)
  return y.random(size=size)

def LogNormal(argnames, mu, sd, size):
  y = pm.Lognormal.dist(mu=mu, sd=sd)
  return y.random(size=size)

def ChiSquared(argnames, nu, size):
  y = pm.ChiSquared.dist(nu)
  return y.random(size=size)

def Wald(argnames, mu, lam, size):
  y = pm.Wald.dist(mu, lam)
  return y.random(size=size)

def Pareto(argnames, alpha, m, size):
  y = pm.Pareto.dist(alpha, m)
  return y.random(size=size)

def InverseGamma(argnames, mu, sd, size):
  y = pm.InverseGamma.dist(mu, sd)
  return y.random(size=size)

def ExGaussian(argnames, mu, sd, nu, size):
  y = pm.ExGaussian.dist(mu, sd, nu)
  return y.random(size=size)

def Triangular(argnames, lower, upper, c, size):
  y = pm.Triangular.dist(lower, upper, c)
  return y.random(size=size)

def Gumbel(argnames, mu, beta, size):
  y = pm.Gumbel.dist(mu, beta)
  return y.random(size=size)

def Logistic(argnames, mu, s, size):
  y = pm.Logistic.dist(mu, s)
  return y.random(size=size)

def LogitNormal(argnames, mu, sd, size):
  y = pm.LogitNormal.dist(mu, sd)
  return y.random(size=size)

# Deterministic Discrete  Distribution Definitions

def Binomial(argnames, n, p, size):
  y = pm.Binomial.dist(n, p)
  return y.random(size=size)

def ZeroInflatedBinomial(argnames, psi, n, p, size):
  y = pm.ZeroInflatedBinomial.dist(psi, n, p)
  return y.random(size=size)

def BetaBinomial(argnames, alpha, beta, n, size):
  y = pm.BetaBinomial.dist(alpha, beta, n)
  return y.random(size=size)

def Bernoulli(argnames, p, size):
  y = pm.Bernoulli.dist(p)
  return y.random(size=size)

def Poisson(argnames, mu, size):
  y = pm.Poisson.dist(mu)
  return y.random(size=size)

def ZeroInflatedPoisson(argnames, psi, mu, size):
  y = pm.ZeroInflatedPoisson.dist(psi, mu)
  return y.random(size=size)

def NegativeBinomial(argnames, mu, alpha, size):
  y = pm.NegativeBinomial.dist(mu, alpha)
  return y.random(size=size)

def ZeroInflatedNegativeBinomial(argnames, psi, mu, alpha, size):
  y = pm.ZeroInflatedNegativeBinomial.dist(psi, mu, alpha)
  return y.random(size=size)

def DiscreteUniform(argnames, upper, lower, size):
  y = pm.DiscreteUniform.dist(upper, lower)
  return y.random(size=size)

def Geometric(argnames, p, size):
  y = pm.Geometric.dist(p)
  return y.random(size=size)

def Categorical(argnames, p, size):
  y = pm.Categorical.dist(p)
  return y.random(size=size)

def DiscreteWeibull(argnames, q, beta, size):
  y = pm.DiscreteWeibull.dist(q, beta)
  return y.random(size=size)

def Constant(argnames, c, size):
  y = pm.Constant.dist(c)
  return y.random(size=size)

# Plotting Function Definitions

def distplot(argnames, x):
  seaborn.distplot(x, axlabel=str(argnames[0]))
  buf = io.BytesIO()
  plt.savefig(buf, format="png")
  plt.close()
  return buf

def private_mean(argnames, x):
  return numpy.mean(x)

def private_std(argnames, x):
  return numpy.std(x)

def private_abs(argnames, x):
  return abs(x)

def private_all(argnames, x):
  return all(x)

def private_any(argnames, x):
  return any(x)

def private_bin(argnames, x):
  return bin(x)

def private_bool(argnames, x):
  return bool(x)

def private_chr(argnames, x):
  return chr(x)

def private_cmp(argnames, x):
  return cmp(x)

def private_complex(argnames, x):
  return complex(x)

def private_dict(argnames, x):
  return dict(x)

def private_divmod(argnames, x):
  return divmod(x)

def private_enumerate(argnames, x):
  return enumerate(x)

def private_exp(argnames, x):
  return numpy.exp(x)

def private_filter(argnames, x):
  return filter(x)

def private_float(argnames, x):
  return float(x)

def private_format(argnames, x):
  return format(x)

def private_frozenset(argnames, x):
  return frozenset(x)

def private_getattr(argnames, x):
  return getattr(x)

def private_hasattr(argnames, x):
  return hasattr(x)

def private_hex(argnames, x):
  return hex(x)

def private_int(argnames, x):
  return int(x)

def private_isinstance(argnames, x):
  return isinstance(x)

def private_issubclass(argnames, x):
  return issubclass(x)

def private_iter(argnames, x):
  return iter(x)

def private_len(argnames, x):
  return len(x)

def private_list(argnames, x):
  return tuple(x)

def private_long(argnames, x):
  return long(x)

def private_map(argnames, x):
  return map(x)

def private_min(argnames, x):
  return min(x)

def private_max(argnames, x):
  return max(x)

def private_object(argnames, x):
  return object(x)

def private_oct(argnames, x):
  return oct(x)

def private_ord(argnames, x):
  return ord(x)

def private_pow(argnames, x):
  return pow(x)

def private_property(argnames, x):
  return property(x)

def private_range(argnames, x):
  return range(x)

def private_reduce(argnames, x):
  return reduce(x)

def private_repr(argnames, x):
  return repr(x)

def private_reversed(argnames, x):
  return reversed(x)

def private_round(argnames, x):
  return round(x)

def private_set(argnames, x):
  return frozenset(x)

def private_slice(argnames, x):
  return slice(x)

def private_sorted(argnames, x):
  return sorted(x)

def private_str(argnames, x):
  return str(x)

def private_sum(argnames, x):
  return sum(x)

def private_tuple(argnames, x):
  return tuple(x)

def private_type(argnames, x):
  return type(x)

def private_unichr(argnames, x):
  return unichr(x)

def private_unicode(argnames, x):
  return unicode(x)

def private_vars(argnames, x):
  return vars(x)

def private_xrange(argnames, x):
  return xrange(x)

def private_zip(argnames, x):
  return zip(x)


builtins = {\

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

prob_builtins = set(["Normal", "HalfNormal", "Uniform", "SkewNormal", "Beta", "Kumaraswamy", "Exponential", "Laplace", "StudentT", "halfStudentT", "Cauchy", "HalfCauchy", "Gamma", "Weibull", "Lognormal", "ChiSquared", "Wald", "Pareto", "InverseGamma", "Exgaussian", "VonMises", "Triangular", "Gumbel", "Logistic", "LogitNormal"]) # continuous distributions
prob_builtins = prob_builtins | set(["Binomial", "ZeroInflatedBinomial", "Bernoulli", "Poisson", "ZeroInflatedPoisson", "NegativeBinomial", "ZeroInflatedNegativeBinomial", "DiscreteUniform", "Geometric", "Categorical", "DiscreteWeibull", "Constant", "OrderedLogistic"]) # discrete distributions

def setPrivacy(graph):
  for name in builtins:
    graph.setPrivacy(name, "public")
  for name in prob_builtins:
    graph.setPrivacy(name, "public")
 
  graph.setPrivacy("Events", "private")

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
  res = "Builtins\n\n"
  res += showNames(builtins.keys())
  return res

def showProbBuiltins():
  res = "Probabilistic Builtins\n\n"
  res += showNames(list(prob_builtins))
  return res

