import logging
FORMAT = '[%(asctime)s] %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

from flask import Flask, render_template, jsonify, request, make_response
import grpc
import json
import service_pb2
import service_pb2_grpc
import sys
import re
import private_config as config
import uuid
import time
from datetime import datetime
import traceback

_log = logging.getLogger("Private Server")

app = Flask("Testing_Server")

re_terminal_graph = re.compile(r'^data:image')

###################
# Setup gRPC client
###################

#rpc_host = 'private-dev.mall-lab.com'
#rpc_port = 51135
#rpc_port = 51141

with open(config.certfile, 'rb') as f:
    trusted_certs = f.read()

#credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
#channel = grpc.secure_channel('{}:{}'.format(rpc_host, rpc_port), credentials)

#rpc_stub = service_pb2_grpc.ServerStub(channel)

def get_rpc_stub(host, port):
    _log.info( "get_rpc_stub: " + '{}:{}'.format(host, port) )
    credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
    channel = grpc.secure_channel('{}:{}'.format(host, port), credentials)
    rpc_stub = service_pb2_grpc.ServerStub(channel)
    return rpc_stub



###############
# Server Routes
###############

@app.route('/', methods=['GET'])
def index():
    analyze_url = "/analyze"
    return render_template(
            'index.html', 
            title="Private", 
            analyze_url=analyze_url,
            delay_sv_update=1000, # delay time to sv update as it goes too quickly on localhost
            )
    

@app.route('/analyze', methods=['POST'])
def run_analyze():
    req = {
        'ace-cmd': request.form.get('cmd')
    }
    _log.info(req)
    res = {}

    rpc_stub = get_rpc_stub(config.private_host, config.private_port)

    if rpc_stub:

        response = rpc_stub.Private(service_pb2.PrivateParcel(json=json.dumps(req), project_uid=config.private_project_id), timeout=60)

        res = json.loads(response.json)
        dest = classify_terminal_response(res)
        res['type'] = dest
    else:
        res = {
            'response': 'No private connection is available, please try again later.',
            'type': 'terminal'
       }

    return jsonify(res)



def run_webserver():
    ''' Run web server '''
    host = "0.0.0.0"
    port = 5000
    _log.info( "Serving on http://" +  host + ":" + str(port) )
    app.run(debug=True, host=host, port=port)



def classify_terminal_response(res):
    dest = "terminal"
    if not res:
        return dest
    if res.get('status') == 'success':
        response = res.get('response')
        if response and re_terminal_graph.search( response ):
            dest = "graph"
    return dest



if __name__ == '__main__':
    run_webserver()
