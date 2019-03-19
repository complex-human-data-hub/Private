import logging
import os

mypid = os.getpid()

print "PID = ", mypid
logfile = "/tmp/private-%d.log" % mypid

# socket timeout in seconds which is also the maximum time a remote job could be executed. Increase this value if you
# have long running jobs or decrease if connectivity to remote ppservers is often lost. - {official documentation}

# In our setting it's necessary to have a minimum possible timeout when working in the cluster with the network
# failures. It's convenient to have a larger value for local setup as we don't expect any failure
remote_socket_timeout = 60
local_socket_timeout = 400000

# s3 config
s3_bucket_name = 'chdhprivate'
s3_log_level = logging.CRITICAL


ppservers = ()
ppservers_list = []
with open('ppserver.conf', 'r') as f:
    for line in f.readlines():
        s = line.strip()
        if s:
            ppservers_list.append(s)

ppservers = tuple(ppservers_list)
