#!/bin/bash
for i in {60000..60026}
do
        echo "dask-worker-$i"
        sudo systemctl restart dask-worker-$i
        sleep 1
done

