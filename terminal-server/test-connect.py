import grpc
import json
import service_pb2
import service_pb2_grpc
import sys


###################
# Setup gRPC client
###################

rpc_host = 'private_server' # localhost, private_server (docker), FQDN
rpc_port = 51135

with open('server.crt', 'rb') as f:
    trusted_certs = f.read()

credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
channel = grpc.secure_channel('{}:{}'.format(rpc_host, rpc_port), credentials)

rpc_stub = service_pb2_grpc.ServerStub(channel)



###############
# Server Routes
###############

def run_analyze(cmd):
    req = {
        'ace-cmd': cmd
    }

    project_uid = '999-999-999'
    # The user's permissions to access
    # expt_uid would now be tested
    print ("Making RPC request: {}".format(req))
    response = rpc_stub.Private(service_pb2.PrivateParcel(json=json.dumps(req), project_uid=project_uid))
    return json.loads(response.json)


res = run_analyze(sys.argv[1])
print (json.dumps(res, indent=4, default=str))


