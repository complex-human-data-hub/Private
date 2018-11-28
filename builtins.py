import numpy.random
import numpy
from event import Event
from demo_events import Events, DemoEvents
import seaborn
import matplotlib.pyplot as plt
import io
import pymc3 as pm

# Deterministic Continuous Distribution Definitions

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

def distplot(x):
  seaborn.distplot(x)
  buf = io.BytesIO()
  plt.savefig(buf, format="png")
  return buf


builtins = {\

            # Deterministic Continuous Distributions

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

            "mean": numpy.mean, \
            "std":numpy.std, \

            # Standard python builtins that don't generate privacy problems

            "abs": abs, \
            "all": all, \
            "any":any, \
            "bin":bin, \
            "bool":bool, \
            "chr":chr, \
            "cmp":cmp, \
            "complex":complex, \
            "dict":dict, \
            "divmod":divmod, \
            "enumerate":enumerate, \
            "filter":filter, \
            "float":float, \
            "format":format, \
            "frozenset":frozenset, \
            "getattr":getattr, \
            "hasattr":hasattr, \
            "hex":hex, \
            "int":int, \
            "isinstance":isinstance, \
            "issubclass":issubclass, \
            "iter":iter, \
            "len":len, \
            "list":tuple, \
            "long":long, \
            "map":map, \
            "min":min, \
            "max":max, \
            "object":object, \
            "oct":oct, \
            "ord":ord, \
            "pow":pow, \
            "property":property, \
            "range":range, \
            "reduce":reduce, \
            "repr":repr, \
            "reversed":reversed, \
            "round":round, \
            "set": frozenset, \
            "slice":slice, \
            "sorted":sorted, \
            "str":str, \
            "sum":sum, \
            "tuple":tuple, \
            "type":type, \
            "unichr":unichr, \
            "unicode":unicode, \
            "vars":vars, \
            "xrange":xrange, \
            "zip":zip}

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

