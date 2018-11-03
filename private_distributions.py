import numpy.random

def normal(mu, sigma, length):
  return(numpy.random.normal(mu, sigma, length))

__private_globals__ = {"normal": normal}
