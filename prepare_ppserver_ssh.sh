#!/bin/bash
while read p;
do
	s=$(echo $p | cut -f1 -d":") # Remove the port
	echo $s
	ssh -oStrictHostKeyChecking=no $s /bin/bash <<EOF
hostname;
EOF
done < ppserver.conf
