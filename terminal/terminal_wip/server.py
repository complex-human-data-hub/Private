from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import grpc
import json
import service_pb2
import service_pb2_grpc
import sys

app = Flask("Testing_Server")
CORS(app)

###################
# Setup gRPC client
###################

rpc_host = 'private.unforgettable.me'
rpc_port = 51134

with open('server.crt', 'rb') as f:
    trusted_certs = f.read()

credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
channel = grpc.secure_channel('{}:{}'.format(rpc_host, rpc_port), credentials)

rpc_stub = service_pb2_grpc.ServerStub(channel)



###############
# Server Routes
###############

@app.route('/', methods=['GET'])
def index():
    return render_template('index2.html',)


@app.route('/analyze', methods=['POST'])
def run_analyze():
    req = {
        'cmd': request.form.get('cmd')
    }

    project_uid = request.form.get('uid')

    # The user's permissions to access
    # expt_uid would now be tested
    print "Making RPC request: {}".format(req)
    response = rpc_stub.Private(service_pb2.PrivateParcel(json=json.dumps(req), project_uid=project_uid))

    return jsonify(json.loads(response.json))



def run_webserver():
    ''' Run web server '''
    host = "0.0.0.0"
    port = 5000
    print "Serving on ", "http://" +  host + ":" + str(port)
    app.run(debug=True, host=host, port=port)



if __name__ == '__main__':
    run_webserver()
