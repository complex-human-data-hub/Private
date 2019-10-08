import logging
FORMAT = '[%(asctime)s] %(levelname)s - %(message)s'
logging.basicConfig(filename='/tmp/private-terminal.log',level=logging.DEBUG, format=FORMAT)

from flask import Flask, render_template, jsonify, request, make_response
import grpc
import json
import service_pb2
import service_pb2_grpc
import sys
import re
import shelvelock
import private_config as config
import uuid
import time
from datetime import datetime
from flask_compress import Compress
import traceback

#formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s", "%Y-%m-%d %H:%M:%S")
#logging.setFormatter(formatter)


_log = logging.getLogger("Private Server")

app = Flask("Testing_Server")
Compress(app)

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
    credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
    channel = grpc.secure_channel('{}:{}'.format(host, port), credentials)
    rpc_stub = service_pb2_grpc.ServerStub(channel)
    return rpc_stub

def get_private_server(uid, uip, uua):
    _log.debug("[{}] get_private_server".format(uid))
    rpc_stub = None
    server_shelf = None
    try:
        uid_str = str(uid)
        _log.debug("[{}] opening shelf".format(uid))
        server_shelf = shelvelock.open(config.privateserver_shelf)
        #Check for current session


        if uid_str in server_shelf:

            _log.debug("[{}]   uid IN shelf".format(uid))
            server = json.loads( server_shelf[uid_str] )
            server['access_time'] = time.time()
            server['ip'] = uip
            server['ua'] = uua
            server_shelf[uid_str] = json.dumps( server )
            _log.debug("[{}]   uid IN shelf get rpc_stub".format(uid))
            rpc_stub = get_rpc_stub(config.private_host, server.get('port')) 
            _log.debug("[{}]   uid IN shelf get rpc_stub ...done".format(uid))
        #Lets try and assign a server
        else:
            _log.debug("[{}]   uid NOT IN shelf".format(uid))
            for port in config.port_range:
                inuse = False
                for key in server_shelf.keys():
                    server = json.loads( server_shelf[key] )
                    if server.get('port') == port:
                        inuse = True
                if not inuse:
                    server_shelf[uid_str] = json.dumps({
                            'uid': uid_str,
                            'port': port,
                            'ip': uip,
                            'ua': uua,
                            'access_time': time.time()
                        })
                    rpc_stub = get_rpc_stub(config.private_host, port)

                    _log.debug("[{}]     found available RPC connection".format(uid))
            _log.debug("[{}]   uid NOT IN shelf...done".format(uid))
 

    except Exception as e:
        _log.debug(json.dumps({
            'error': 'get_private_server',
            'message': str(e)
            }))
    finally:
        if server_shelf:
            server_shelf.close()
        _log.debug("[{}] closing shelf".format(uid))

    if rpc_stub:    
        _log.debug("[{}] HAVE rpc_stub".format(uid))
    else:
        _log.debug("[{}] DON'T HAVE rpc_stub".format(uid))

    return rpc_stub
    



###############
# Server Routes
###############

@app.route('/', methods=['GET'])
def index():
    analyze_url = "/analyze"
    user_uid = request.cookies.get('uid')
    if not user_uid:
        user_uid = str( uuid.uuid4() )

    if 'debug' in request.cookies:
        resp = make_response( render_template('index-dev.html', uid=user_uid, title="Dev", analyze_url=analyze_url))
    else:
        resp = make_response( render_template('index.html', uid=user_uid, title="Private", analyze_url=analyze_url))
    resp.set_cookie('uid', value=user_uid)
    
    _log.debug("[{}] /".format(user_uid))
    return resp
    

@app.route('/analyze', methods=['POST'])
def run_analyze():
    try:
        #user_uid = request.form.get('uid')
        user_uid = request.cookies.get('uid')
        user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        user_ua = request.environ.get('HTTP_USER_AGENT', "") # Having troubles getting the IP, so using UA as a reference

        _log.debug('[{}] /analyze'.format(user_uid))
        req = {
            'cmd': request.form.get('cmd')
        }
        _log.debug("[{}] ...CMD: {}".format(user_uid, req['cmd']))
        res = {}

        #project is going to remain static 
        #project_uid = '91b4e84e078c38b22a51fcc1c2c1ae62'
        # The user's permissions to access
        # expt_uid would now be tested
        if 'debug' in request.cookies:
            _log.debug("[{}] ...cookie.debug".format(user_uid))
            rpc_stub = get_rpc_stub(config.private_host, config.debug_port)
        else:
            _log.debug("[{}] ...NO cookie.debug".format(user_uid))
            rpc_stub = get_private_server(user_uid, user_ip, user_ua)

        if rpc_stub:
            _log.debug("[{}] ...rpc_stub".format(user_uid))
            _log.debug( "[{}] ...Making RPC request: {}".format(user_uid, req) )

            response = rpc_stub.Private(service_pb2.PrivateParcel(json=json.dumps(req), project_uid=config.project_uid), timeout=10)

            _log.debug("[{}] ...Request RETURNED".format(user_uid))
            res = json.loads(response.json)
            dest = classify_terminal_response(res)
            res['type'] = dest
        else:
            _log.debug("[{}] NO rpc_stub".format(user_uid))
            res = {
                'response': 'No private connection is available, please try again later.',
                'type': 'terminal'
            }

    except Exception as err:
        _log.debug("[{}] /analyse error: {}".format(user_uid, str(err)))
        _log.debug(traceback.format_exc())
    return jsonify(res)



def run_webserver():
    ''' Run web server '''
    host = "0.0.0.0"
    port = 5000
    _log.info( "Serving on ", "http://" +  host + ":" + str(port) )
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


def _debug(msg):
    with open('/tmp/bens.log', 'a') as fp:
        if isinstance(msg, basestring):
            fp.write("{}\n".format(msg))
        else:
            fp.write(str(msg) + "\n")


if __name__ == '__main__':
    run_webserver()
