import numpy 

def zeros(n):
  return(numpy.zeros(n))

def ones(n):
  return(numpy.ones(n))

__private_globals__ = {"zeros": zeros, "ones": ones}
