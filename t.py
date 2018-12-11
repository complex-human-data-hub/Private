
import logging
_log = logging.getLogger("Private")
logging.disable(100)

import pymc3 as pm
from numpy import exp


try:

  basic_model = pm.Model()

  with basic_model:

    exception_variable = None
    exception_variable = "ua"
    ua = pm.Normal('ua', 0, 1)
    exception_variable = "ub"
    ub = pm.Normal('ub', 1, 1)
    exception_variable = "l"
    p = exp(ua) / (exp(ua) + exp(ub))
    l = pm.Bernoulli('l', p, observed=[1,1,1,0])

    __private_result__ = (pm.sample(200, tune=200, chains=2, random_seed=987654321, progressbar = False), "No Exception Variable")

except Exception as e:
  # remove stuff after the : as that sometimes reveals private information
  ind = e.args[0].find(":")
  if ind != -1:
    estring = e.args[0][0:ind]
  else:
    estring = e.args[0]
    
  #newErrorString = "Problem with %s: %s" % (exception_variable, estring)
  newErrorString = estring
  e.args = (newErrorString,)
  __private_result__ = (e, exception_variable)


print __private_result__[0]["ua"]
