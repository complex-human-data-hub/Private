from __future__ import print_function
import logging
import os


def config_logger():
    log_format = '[%(asctime)s] %(levelname)s - %(message)s'
    if logging.getLogger().hasHandlers():
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.basicConfig(level=logging.INFO, format=log_format)

mypid = os.getpid()

print("PID = ", mypid)

# socket timeout in seconds which is also the maximum time a remote job could be executed. Increase this value if you
# have long running jobs or decrease if connectivity to remote ppservers is often lost. - {official documentation}

# In our setting it's necessary to have a minimum possible timeout when working in the cluster with the network
# failures. It's convenient to have a larger value for local setup as we don't expect any failure
remote_socket_timeout = 1209600 # 14 days
local_socket_timeout = 400000

#System tcp_keepalive_time
tcp_keepalive_time = 7200 #2 hours


# S3 configs
s3_integration = False
s3_bucket_name = 'chdhprivate'
s3_log_level = logging.CRITICAL

#dask config
dask_scheduler_ip = "dask_scheduler" # localhost, dask_scheduler (docker), FQDN
dask_scheduler_port = 8786

#redis config 
redis_server_ip = "redis_server" # localhost, redis_server (docker), FQDN

# data location
data_location = "/data/cache"

# numpy seed
numpy_seed = 8623574

# Return sample size
max_sample_size = 1000

number_of_tuning_samples = 200
number_of_chains = 2
number_of_samples = 1000

ppservers = ()
ppservers_list = []

exists = os.path.isfile('ppserver.conf')
if exists:
    with open('ppserver.conf', 'r') as f:
        for line in f.readlines():
            s = line.strip()
            if s and not s.startswith("#"):
                ppservers_list.append(s)

ppservers = tuple(ppservers_list)
