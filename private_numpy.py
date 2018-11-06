import numpy 

def zeros(n):
  return(numpy.zeros(n))

def ones(n):
  return(numpy.ones(n))

def array(n):
  return(numpy.array(n))

__private_globals__ = {"zeros": zeros, "ones": ones, "array": array}
