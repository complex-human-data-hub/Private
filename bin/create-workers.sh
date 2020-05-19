#!/bin/bash
port=60004
workers=22
endworker=$(($port+$workers))
for i in $(seq $port 1 $endworker)
do

daskservice=$(<dask-worker.service)
newservice=dask-worker-$i.service
outfile=/etc/systemd/system/$newservice
tmpfile=/tmp/$newservice

echo $outfile
echo "${daskservice/WORKER_PORT/$i}" > $tmpfile
sudo mv $tmpfile $outfile
sudo systemctl enable $newservice
sudo systemctl restart $newservice
done; 
