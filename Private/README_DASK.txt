#Start the scheduler in the master machine
dask-scheduler

#Start the dask workers in the other machines
dask-worker <scheduler ip>:<schduler port> --no-nanny --nthreads 2 --resources "process=1"