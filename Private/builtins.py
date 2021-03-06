from __future__ import print_function
from __future__ import absolute_import

import logging
import numpy.random
import numpy
from scipy import stats
from .event import Event
from Private.reference import Reference
import Private.redis_helper as redis_helper
import pymc3 as pm
import theano.tensor
import math
from .config import numpy_seed, number_of_tuning_samples, number_of_chains, number_of_samples, config_logger

from . import preprocessing as pre
from . import plotting as plot
from .demo_experiment_events import DemoProjects
from dateutil import parser as dateutil_parser
from datetime import timedelta
import dill as pickle


# Import our source data 
# defaults to DemoEvents, but this class
# can be replace by a custom Source class to suit 
# the researchers purposes

from .private_data import Source
from functools import reduce

config_logger()
logger = logging.getLogger("Builtins")
data_source = Source()
Events = data_source.get_events()
DemoEvents = data_source.get_demo_events()

# Deterministic Continuous Distribution Definitions
numpy.random.seed(numpy_seed)




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


# Deterministic implementation of dot and softmax
def dot(x, y, *args, **kwargs):
    return numpy.dot(x, y)


def softmax(x):
    e_x = numpy.exp(x - numpy.max(x))
    return e_x / e_x.sum(axis=0)


# Probabilistic Functions
def Sigmoid(x):
    return 1 / (1 + theano.tensor.exp(-x))



def private_array(x):
    return numpy.array(x, numpy.float)


def private_mean(x, **kwargs):
    return numpy.mean(x, **kwargs)


def private_median(x, **kwargs):
    return numpy.median(x, **kwargs)


def private_percentile(x, percent):
    return numpy.percentile(x, percent, interpolation='lower')


def private_std(x, **kwargs):
    return numpy.std(x, **kwargs)


def private_abs(x):
    return abs(x)


def private_pearsonr(*args, **kwargs):
    return stats.pearsonr(*args, **kwargs)




def private_flatten(arr):
    return [y for x in arr for y in x]



def private_all(iterable):
    return all(iterable)


def private_any(iterable):
    return any(iterable)


def private_bin(number):
    return bin(number)


def private_bool(x):
    return bool(x)


def private_chr(x):
    return chr(x)


def private_cmp(x, y):
    return ((x > y) - (x < y))


def private_complex(real, *imag):
    return complex(real, *imag)


def private_dict(x):
    return dict(x)


def private_divmod(x, y):
    return divmod(x, y)


def private_enumerate(iterable, start=0):
    return list(enumerate(iterable, start))


def private_exp(x):
    return numpy.exp(x)


def private_filter(function, iterable):  # cannot use as we can't take functions in Private
    return filter(function, iterable)


def private_float(x):
    return float(x)


def private_format(value, format_spec=None):
    return format(value, format_spec)


def private_frozenset(x):
    return frozenset(x)


def private_getattr(object, name, default=None):
    return getattr(object, name, default)


def private_hasattr(p_object, name):
    return hasattr(p_object, name)


def private_hex(x):
    return hex(x)


def private_int(x):
    return int(x)


def private_isinstance(obj, type):
    return isinstance(obj, type)


def private_issubclass(x, y):
    return issubclass(x, y)


def private_iter(source, sentinel=None):
    return iter(source, sentinel)


def private_len(x):
    return len(x)


def private_list(x):
    return list(x)


def private_long(x):
    return int(x)


def private_map(function, iterable):  # cannot use as we can't take functions in Private
    return map(function, iterable)


def private_min(*args, **kwargs):
    return min(*args, **kwargs)


def private_max(*args, **kwargs):
    return max(*args, **kwargs)


def private_object(x):
    return object(x)


def private_oct(x):
    return oct(x)


def private_ord(ch):
    return ord(ch)


def private_pow(x, y, z=None):
    return pow(x, y, z)


def private_open(name, per):  ####### WARNING Do not ship with this line in ###########
    return open(name, per)


def private_property(x):
    return property(x)


def private_range(*args):
    return range(*args)


def private_reduce(function, iterable):
    return reduce(function, iterable)


def private_repr(x):
    return repr(x)


def private_reversed(x):
    return reversed(x)


def private_round(number, ndigits=None):
    return round(number, ndigits=ndigits)


def private_set(iterable):
    return frozenset(iterable)


def private_slice(*args):
    return slice(*args)


def private_sorted(iterable, cmp=None, key=None, reverse=False):
    return sorted(iterable, cmp=cmp, key=key, reverse=reverse)


def private_sqrt(x):
    return math.sqrt(x)


def private_str(x):
    return str(x)


def private_sum(iterable, start=0):
    return sum(iterable, start)


def private_tuple(x):
    return tuple(x)


def private_type(x):
    return type(x)


def private_unichr(x):
    return chr(x)


def private_unicode(obj):
    return str(obj)


def private_vars(p_object=None):
    return vars(p_object)


def private_xrange(start, stop, *step):
    return range(start, stop, *step)


def private_zip(*iterables):
    return zip(*iterables)


def private_fft(x, seg_size=-1):
    return pre.fft(x, seg_size)


def private_mfcc(x):
    return pre.mfcc(x)


def zip_date(lists, keys='StartDateTime', maxdist=('minutes', 30), unmatched=False):
    return pre.zip_date(lists, keys, maxdist, keep_unmatched=unmatched)


def bucket_date(lists, keys, interval, start=None, empty=False):
    return pre.bucket_date(lists, keys, interval, bucket_start_str=start, keep_empty_buckets=empty)


def euclidean_distance(v1, v2):
    return pre.euclidean_distance(v1, v2)


def all_pair_euclidean_distance(vector_list1, vector_list2):
    return pre.all_pair_euclidean_distance(vector_list1, vector_list2)


def location_distance(lat1, lon1, lat2, lon2):
    return pre.get_distance_km(lat1, lon1, lat2, lon2)


def all_pair_location_distance(loc_list1, loc_list2):
    return  pre.get_all_pair_loc_distance(loc_list1, loc_list2)


def array_output_threshold(x):
    numpy.set_printoptions(threshold=int(x))


def private_isclose(a, b, rtol=1e-05, atol=1e-08, equal_nan=False):
    return numpy.isclose(a, b, rtol, atol, equal_nan)



# how do we stop the user guessing the at a project_id and user_id
# from a different project??
def private_get_events(project_id, user_id):
    rk_events = redis_helper.get_redis_key(user_id, "Events", project_id, "shared")
    return Reference(rk_events, [], keep_existing=True) # Empty list is so we can set a display value of that type


def private_get_demo_events(project_id,user_id):
    rk_events = redis_helper.get_redis_key(user_id, "DemoEvents", project_id, "shared")
    display_data = DemoProjects.get(project_id, []) 
    return Reference(rk_events, display_data, keep_existing=True) # Empty list is so we can set a display value of that type

def private_get_number_of_tuning_samples():
    return number_of_tuning_samples

def private_get_number_of_chains():
    return number_of_chains

def private_get_number_of_samples():
    return number_of_samples


# Datetime functions

def private_dateutil_parse(datestr):
    return dateutil_parser.parse(datestr)



def private_datetime_timedelta(*args, **kwargs):
    return timedelta(*args, **kwargs)

builtins = {\

            # make __bultins__ None
            # this is crucial to stop __builtins__ being available in eval code

            "__builtins__": None,
            "__import__": __import__,
            "Exception": Exception,

            "True": True,
            "False": False,

            # Deterministic Continuous Distributions

            "Uniform": Uniform,
            "Normal": Normal,
            "HalfNormal": HalfNormal,
            "SkewNormal": SkewNormal,
            "Beta": Beta,
            "Kumaraswamy": Kumaraswamy,
            "Exponential": Exponential,
            "Laplace": Laplace,
            "StudentT": StudentT,
            "HalfStudentT": HalfStudentT,
            "Cauchy": Cauchy,
            "HalfCauchy": HalfCauchy,
            "Gamma": Gamma,
            "Weibull": Weibull,
            "LogNormal": LogNormal,
            "ChiSquared": ChiSquared,
            "Wald": Wald,
            "Pareto": Pareto,
            "InverseGamma": InverseGamma,
            "ExGaussian": ExGaussian,
            "Triangular": Triangular,
            "Gumbel": Gumbel,
            "Logistic": Logistic,
            "LogitNormal": LogitNormal,

            # Deterministic Discrete Distributions

            "Binomial": Binomial,
            "ZeroInflatedBinomial": ZeroInflatedBinomial,
            "BetaBinomial": BetaBinomial,
            "Bernoulli": Bernoulli,
            "Poisson": Poisson,
            "ZeroInflatedPoisson": ZeroInflatedPoisson,
            "NegativeBinomial": NegativeBinomial,
            "ZeroInflatedNegativeBinomial": ZeroInflatedNegativeBinomial,
            "DiscreteUniform": DiscreteUniform,
            "Geometric": Geometric,
            "Categorical": Categorical,
            "DiscreteWeibull": DiscreteWeibull,
            "Constant": Constant,

            # Theano Functions
            "dot": dot, 
            "softmax": softmax,

            # Probilistic Function 
            "Sigmoid": Sigmoid,

            # Plotting Functions
            #   Distribution plots
            "jointplot": plot.jointplot,
            "pairplot": plot.pairplot,
            "distplot": plot.distplot,
            "kdeplot": plot.kdeplot,
            "rugplot": plot.rugplot,

            #   Relational and Categorical plots
            "relplot": plot.relplot,
            "catplot": plot.catplot,

            #   Regression plots
            "lmplot": plot.lmplot,
            "regplot": plot.regplot,
            "residplot": plot.residplot,

            # Matrix plots
            "heatmap": plot.heatmap,
            "clustermap": plot.clustermap,

            # Other plots
            "pointplot": plot.pointplot,

            # Control of Sampler

            #"NumberOfTuningSamples": 200,
            #"NumberOfChains": 2,
            #"NumberOfSamples": 1000,

            # Data

            "DemoEvents": DemoEvents,
            "Events": Events,
            "Event": Event,
            #"ExpEvents": ExpEvents,

            # Summary Statistics

            "array": private_array,
            "mean": private_mean,
            "median": private_median,
            "percentile": private_percentile,
            "std": private_std,


            # Scipy Statistics
            "pearsonr": private_pearsonr,

            # Convenience functions
            "flatten": private_flatten,

            # Standard python builtins that don't generate privacy problems

            "abs": private_abs,
            "all": private_all,
            "any":private_any,
            "bin":private_bin,
            "bool":private_bool,
            "chr":private_chr,
            "cmp":private_cmp,
            "complex":private_complex,
            "dict":private_dict,
            "divmod":private_divmod,
            "enumerate":private_enumerate,
            "exp":private_exp,
            "filter":private_filter,
            "float":private_float,
            "format":private_format,
            "frozenset":private_frozenset,
            "getattr":private_getattr,
            "hasattr":private_hasattr,
            "hex":private_hex,
            "int":private_int,
            "isinstance":private_isinstance,
            "issubclass":private_issubclass,
            "iter":private_iter,
            "len":private_len,
            "list":private_tuple,
            "long":private_long,
            "map":private_map,
            "min":private_min,
            "max":private_max,
            "object":private_object,
            "oct":private_oct,
            "open":private_open,       ####### WARNING Do not ship with this line in ###########
            "ord":private_ord,
            "pow":private_pow,
            "property":private_property,
            "range":private_range,
            "reduce":private_reduce,
            "repr":private_repr,
            "reversed":private_reversed,
            "round":private_round,
            "set": private_frozenset,
            "slice":private_slice,
            "sorted":private_sorted,
            "sqrt":private_sqrt,
            "str":private_str,
            "sum":private_sum,
            "tuple":private_tuple,
            "type":private_type,
            "unichr":private_unichr,
            "unicode":private_unicode,
            "vars":private_vars,
            "xrange":private_xrange,
            "zip":private_zip,

            # Pre-processing builtins

            "fft": private_fft,
            "mfcc": private_mfcc,
            "zipDate": zip_date,
            "bucketDate": bucket_date,
            "eucDist": euclidean_distance,
            "eucDistAll": all_pair_euclidean_distance,
            "locDist": location_distance,
            "locDistAll": all_pair_location_distance,

            #testing
            "isclose": private_isclose,

            # config builtins
            "ArrayOutputThreshold": array_output_threshold,

            # stat and diagnostic built-ins
            #"rhat": {},
            #"ess": {},
            #"waic": {},
            #"loo": {},

            "getEvents": private_get_events,
            "getDemoEvents": private_get_demo_events,


            "getNumberOfTuningSamples": private_get_number_of_tuning_samples,
            "getNumberOfChains": private_get_number_of_chains,
            "getNumberOfSamples": private_get_number_of_samples,
            

            #datetime functions
            "dateutilparse": private_dateutil_parse,
            "datetimetimedelta": private_datetime_timedelta,
    }

prob_builtins = set(["Normal", "HalfNormal", "Uniform", "SkewNormal", "Beta", "Kumaraswamy", "Exponential", "Laplace", "StudentT", "HalfStudentT", "Cauchy", "HalfCauchy", "Gamma", "Weibull", "Lognormal", "ChiSquared", "Wald", "Pareto", "InverseGamma", "Exgaussian", "VonMises", "Triangular", "Gumbel", "Logistic", "LogitNormal"]) # continuous distributions
prob_builtins = prob_builtins | set(["Binomial", "ZeroInflatedBinomial", "Bernoulli", "Poisson", "ZeroInflatedPoisson", "NegativeBinomial", "ZeroInflatedNegativeBinomial", "DiscreteUniform", "Geometric", "Categorical", "DiscreteWeibull", "Constant", "OrderedLogistic"]) # discrete distributions
prob_builtins = prob_builtins | {'dot', 'softmax'} # theano
commands = set(["del", "dt", "sv", "sval", "clear", "sd", "scode", "sevalcode", "smccode", "sss", "ssr", "spp", "ss", "sg", "sj", "vc", "vs", "sb", "spb", "sncpus", "showstats", "help"])
config_builtins = ("ArrayOutputThreshold",)
plot_builtins = {"jointplot", "pairplot", "distplot", "kdeplot", "rugplot", "relplot", "catplot", "lmplot", "regplot", "residplot", "heatmap", "clustermap", "pointplot"}
illegal_variable_names = prob_builtins | set(["fft", "mfcc", "zipDate", "bucketDate" , "eucDist", "eucDistAll", "locDist", "locDistAll"]) | set(["rhat", "ess", "waic", "loo"]) | set(["Events", "DemoEvents"])
data_builtins = {'Events', 'DemoEvents', 'Event'}
keep_private_variables = ['NumberOfSamples', 'NumberOfTuningSamples', 'NumberOfChains', 'rhat', 'ess', 'loo', 'waic']

def set_builtin_privacy(graph):
    for name in builtins:
        graph.set_privacy(name, "public")
    for name in prob_builtins:
        graph.set_privacy(name, "public")

    graph.set_privacy("Events", "private")
    graph.set_privacy("getEvents", "private")


def show_names(names, width=80):
    names.sort()
    column_width = max(len(s) for s in names)+2
    num_columns = width // column_width

    num_rows = len(names) // num_columns
    rows = [""] * num_rows
    for i, name in enumerate(names):
        rows[i%num_rows] += name.ljust(column_width)
    return "\n".join(rows)


def show_builtins():
    res = "Builtins\n\n"
    res += show_names(list(builtins.keys()))
    return res


def show_prob_builtins():
    res = "Probabilistic Builtins\n\n"
    res += show_names(list(prob_builtins))
    return res


def set_globals(user_ids):
    logger.debug("set_globals")
    result = {}
    # We can pickle builtins 
    # so quicker than deepcopy
    builtins_pickle = pickle.dumps(builtins) 

    for u in user_ids:
        result[u] = pickle.loads(builtins_pickle)
    result["All"] = pickle.loads(builtins_pickle)
    logger.debug("set_globals ...done")
    return result

