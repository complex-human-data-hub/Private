DEBUG = True
PROJECT_UID = '12345'

if DEBUG:
    import os,sys,inspect
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0,parentdir)

import sys
import io
import traceback
import logging

_log = logging.getLogger("Private {}".format(PROJECT_UID))
logging.basicConfig(filename='/tmp/private-{}.log'.format(PROJECT_UID),level=logging.DEBUG)


from parser import PrivateParser
from semantics import PrivateSemanticAnalyser

import signal
from concurrent import futures

import grpc

import service_pb2
import service_pb2_grpc
import json



class Private:
    expt_uid = PROJECT_UID
    parser = PrivateParser()
    def execute(self, line):
        if line != "":
            try:
                    parse_tree = self.parser.parse(line)
            except Exception as e:  # didn't parse
                print(e)
            else:
                try:
                    result = PrivateSemanticAnalyser(parse_tree)
                    print "result: {}".format(result)
                    if result:
                        return(result)
                except Exception as e:
                    print(e)
                    traceback.print_exc(file=sys.stdout)
    


class ServerServicer(service_pb2_grpc.ServerServicer):
    def __init__(self):
        self.private = Private()

    def Foo(self, request, context):
        return service_pb2.Empty()

    def Private(self, request, context):
        try:
            if request.project_uid != PROJECT_UID:
                raise Exception("Incorrect project ID")
            req = json.loads(request.json)
            print req
            res = self.private.execute(str(req.get('cmd')))
            ret = {'status': 'success', 'response': res}
            return service_pb2.PrivateParcel(json=json.dumps(ret), project_uid=request.project_uid)    
        except Exception as err:
            ret = {'status': 'failed', 'error': err}
            return service_pb2.PrivateParcel(json=json.dumps(ret), project_uid=request.project_uid)

def main():
    port = '1337'

    with open('server.key', 'rb') as f:
        private_key = f.read()
    with open('server.crt', 'rb') as f:
        certificate_chain = f.read()

    server_credentials = grpc.ssl_server_credentials(
      ((private_key, certificate_chain,),))

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    service_pb2_grpc.add_ServerServicer_to_server(ServerServicer(), server)

    server.add_secure_port('localhost:'+port, server_credentials)

    server.start()
    try:
        while True:
            signal.pause()
    except KeyboardInterrupt:
        pass
    server.stop(0)

if __name__ == '__main__':
    main()

