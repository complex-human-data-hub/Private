#!/bin/bash
dask-worker localhost:8786 --no-nanny --nthreads 2 --resources "process=1" --worker-port 60001
