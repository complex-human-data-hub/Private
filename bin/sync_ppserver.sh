#!/bin/bash
while read p;
do
	s=$(echo $p | cut -f1 -d":") # Remove the port
	echo $s
	rsync -avuzpor --exclude .git --exclude .gitignore . ubuntu@$s:/home/ubuntu/venv/lib/python2.7/site-packages/Private
	ssh -oStrictHostKeyChecking=no $s /bin/bash <<EOF
cd Private
git pull
sudo systemctl restart ppserver.service
EOF
done < ppserver.conf
