from __future__ import print_function
import grpc
import json
from . import service_pb2
from . import service_pb2_grpc
import time
import config
import shelvelock
import sys

killall = False
if len(sys.argv) > 1:
    killall = True 

with open(config.certfile, 'rb') as f:
    trusted_certs = f.read()


def get_rpc_stub(host, port):
    credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
    channel = grpc.secure_channel('{}:{}'.format(host, port), credentials)
    #channel = grpc.secure_channel('{}:{}'.format(host, port), credentials, options=opts)
    rpc_stub = service_pb2_grpc.ServerStub(channel)
    return rpc_stub


server_shelf = shelvelock.open(config.privateserver_shelf)
remove = [51150, 51149, 51154]
now = time.time()
for key in server_shelf.keys():
    server = json.loads( server_shelf[key] )
    if server.get('port') in remove or killall or ((now - server.get('access_time')) >= config.server_timeout):
        req = {'cmd': 'clear'}
        print(server.get('port'))
        rpc_stub = get_rpc_stub(config.private_host, server.get('port'))
        response = rpc_stub.Private(service_pb2.PrivateParcel(json=json.dumps(req), project_uid=config.project_uid))
        del server_shelf[key]

server_shelf.close()
    
