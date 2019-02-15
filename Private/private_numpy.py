import numpy

def zeros(n):
    return(numpy.zeros(n))

def ones(n):
    return(numpy.ones(n))

def array(n):
    return(numpy.array(n))

def mean(m):
    return(numpy.mean(m))

def std(m):
    return(numpy.std(m))

def median(m):
    return(numpy.median(m))

def var(m):
    return(numpy.var(m))

__private_globals__ = {"zeros": zeros, "ones": ones, "array": array, "mean": mean, "median": median, "std": std, "var": var}
