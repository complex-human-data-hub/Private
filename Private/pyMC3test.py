from __future__ import print_function
import numpy as np
#import matplotlib.pyplot as plt
#plt.style.use('seaborn-darkgrid')

import warnings
#warnings.filterwarnings("ignore")

#import logging
#logger = logging.getLogger("pymc3")
#logging.disable(100)

# Initialize random number generator
np.random.seed(123)

# True parameter values
alpha, sigma = 1, 1
beta = [1, 2.5]

# Size of dataset
size = 100

# Predictor variable
X1 = np.random.randn(size)
X2 = np.random.randn(size) * 0.2

# Simulate outcome variable
Y = alpha + beta[0]*X1 + beta[1]*X2 + np.random.randn(size)*sigma

import pymc3 as pm

print('Running on PyMC3 v{}'.format(pm.__version__))

basic_model = pm.Model()
with basic_model:

    # Priors for unknown model parameters
    alpha = pm.Normal('alpha', mu=0, sd=10)
    beta = pm.Normal('beta', mu=0, sd=10, shape=2)
    sigma = pm.HalfNormal('sigma', sd=1)

    # Expected value of outcome
    mu = alpha + beta[0]*X1 + beta[1]*X2

    meana = np.mean(alpha)

    # Likelihood (sampling distribution) of observations
    #Y_obs = pm.Normal('Y_obs', mu=mu, sd=sigma, observed=Y)

    print("here")
    trace = pm.sample(500, progressbar=False, verbose=False)
    print("here2")

    #pm.traceplot(trace)

#plt.show()

print(trace["alpha"])
