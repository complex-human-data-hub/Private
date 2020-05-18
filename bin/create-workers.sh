#!/bin/bash
port=60000
workers=3
endworker=$(($port+$workers))
for i in $(seq $port 1 $endworker)
do

daskservice=$(<dask-worker.service)
newservice=dask-worker-$i.service
outfile=/tmp/$newservice
echo $outfile
echo "${daskservice/WORKER_PORT/$i}" > $outfile
echo "sudo systemctl enable $newservice"
echo "sudo systemctl restart $newservice"
done; 
