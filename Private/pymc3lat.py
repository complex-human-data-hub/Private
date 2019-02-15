import numpy as np
import numpy.random as r
import pandas as pd
#import matplotlib.pyplot as plt
#plt.style.use('seaborn-darkgrid')

import warnings
#warnings.filterwarnings("ignore")

#import logging
#logger = logging.getLogger("pymc3")
#logging.disable(100)

# Initialize random number generator
np.random.seed(123)


latitudes = [ \
{"Name": "Simon", "ParticipantNumber": 0, "Latitude": -32.8777964}, \
{"Name": "Simon", "ParticipantNumber": 0, "Latitude": -31.13299626},  \
{"Name": "Simon", "ParticipantNumber": 0, "Latitude": -29.30672514},  \
{"Name": "Simon", "Latitude": -31.44427978}, \
{"Name": "Simon", "Latitude": -30.6007072},  \
{"Name": "Simon", "Latitude": -30.26990065},  \
{"Name": "Simon", "Latitude": -31.14992687},  \
{"Name": "Simon", "Latitude": -32.01555767}, \
{"Name": "Simon", "Latitude": -31.98173715},  \
{"Name": "Simon", "Latitude": -30.26162892}, \
{"Name": "James", "Latitude": -31.79765827},  \
{"Name": "James", "Latitude": -32.18883745},  \
{"Name": "James", "Latitude": -31.89547302},  \
{"Name": "James", "Latitude": -33.27869788}, \
{"Name": "James", "Latitude": -32.17336627},  \
{"Name": "James", "Latitude": -31.86958377},  \
{"Name": "James", "Latitude": -32.76938723},  \
{"Name": "James", "Latitude": -31.98001131}, \
{"Name": "James", "Latitude": -32.52816492},  \
{"Name": "James", "Latitude": -29.61288676}, \
{"Name": "James", "Latitude": -29.82344246},  \
{"Name": "James", "Latitude": -31.69931953},  \
{"Name": "James", "Latitude": -32.70747199}, \
{"Name": "James", "Latitude": -30.41835425},  \
{"Name": "James", "Latitude": -32.44337631}, \
{"Name": "Mary", "Latitude": -31.06767744},  \
{"Name": "Mary", "Latitude": -32.06719055},  \
{"Name": "Mary", "Latitude": -31.77793909},  \
{"Name": "Mary", "Latitude": -31.12540107}, \
{"Name": "Mary", "Latitude": -32.23763943},  \
{"Name": "Mary", "Latitude": -30.42938149},  \
{"Name": "Mary", "Latitude": -31.11839393},  \
{"Name": "Mary", "Latitude": -31.5200227}, \
{"Name": "Mary", "Latitude": -31.23391723},  \
{"Name": "Mary", "Latitude": -30.27704399},  \
{"Name": "Mary", "Latitude": -30.59014408},  \
{"Name": "Mary", "Latitude": -31.75727519}, \
{"Name": "Mary", "Latitude": -30.90310857},  \
{"Name": "Mary", "Latitude": -31.86057581},  \
{"Name": "Mary", "Latitude": -30.6213658},  \
{"Name": "Mary", "Latitude": -29.54493083}, \
{"Name": "Mary", "Latitude": -32.94843911},  \
{"Name": "Mary", "Latitude": -29.76572936},  \
{"Name": "Mary", "Latitude": -32.08862493},  \
{"Name": "Mary", "Latitude": -31.11800896}]

Latitudes = pd.DataFrame(latitudes)
print Latitudes


lats = np.normal(-31, 1, 10)

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

    meana = mean(alpha)

    # Likelihood (sampling distribution) of observations
    #Y_obs = pm.Normal('Y_obs', mu=mu, sd=sigma, observed=Y)

    print "here"
    trace = pm.sample(500, progressbar=False, verbose=False)
    print "here2"

    #pm.traceplot(trace)

#plt.show()

print trace["alpha"]
