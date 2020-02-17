from __future__ import print_function
import shelvelock
from . import private_config as config
import json
import time
now = time.time() 

def format_output(item):
    inactive_mins = int((now - item.get('access_time')) / 60.)
    #return "{}\t{}\t{}\t{}\t{}".format(inactive_mins, item.get('port'), item.get('uid'), item.get('ip', ''), item.get('ua', ''))
    return "{}\t{}\t{}\t{}".format(inactive_mins, item.get('port'), item.get('uid'), item.get('ua', ''))


server_shelf = shelvelock.open(config.privateserver_shelf)


print("Inactive\tPort\tUID\tIP\tUA")
for key in server_shelf.keys():
    print(format_output( json.loads(server_shelf.get(key)) ))

server_shelf.close()
