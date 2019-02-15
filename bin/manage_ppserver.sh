#!/bin/bash
CMD=$1
if [ -z "$CMD" ];
then
	CMD="status";
fi

while read p;
do
	s=$(echo $p | cut -f1 -d":") # Remove the port
	echo $s
	ssh -oStrictHostKeyChecking=no $s /bin/bash <<EOF
sudo systemctl $CMD ppserver.service
EOF
done < ppserver.conf
