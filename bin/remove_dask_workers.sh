#!/bin/bash
for i in {60000..60026}
do
	newservice=dask-worker-$i.service
        echo $newservice
        sudo systemctl stop $newservice
        sudo systemctl disable $newservice
	outfile=/etc/systemd/system/$newservice
	sudo rm $outfile	
done

sudo systemctl daemon-reload

