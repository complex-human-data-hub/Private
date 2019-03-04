import shelvelock 
import private_config as config
import json
import time
now = time.time() 

def format_output(item):
    inactive_mins = int((now - item.get('access_time')) / 60.)
    return "{}\t{}\t{}".format(inactive_mins, item.get('port'), item.get('uid'))


server_shelf = shelvelock.open(config.privateserver_shelf)


print "Inactive\tPort\tUID"
for key in server_shelf.keys():
    print format_output( json.loads(server_shelf.get(key)) )

server_shelf.close()