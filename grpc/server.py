PROJECT_UID = 12345
DEBUG = True

if DEBUG:
    import os,sys,inspect
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0,parentdir)
    from parser import PrivateParser
    from semantics import PrivateSemanticAnalyser
else:
    from Private.parser import PrivateParser
    from Private.semantics import PrivateSemanticAnalyser

import sys
import io
import traceback
import logging



import signal
from concurrent import futures

import grpc

import service_pb2
import service_pb2_grpc
import json



class Private:
    project_uid = None
    parser = PrivateParser()
    def __init__(self, project_uid):
        self.project_uid = project_uid
        self._log = logging.getLogger("Private {}".format(PROJECT_UID))
        logging.basicConfig(filename='/tmp/private-{}.log'.format(PROJECT_UID),level=logging.INFO)

    def execute(self, line):
        if line != "":
            try:
                parse_tree = self.parser.parse(line)
            except Exception as e:  # didn't parse
                self._log.debug(e)
            else:
                try:
                    result = PrivateSemanticAnalyser(parse_tree)
                    return(result)
                except Exception as e:
                    self._log.debug(e)
                    traceback.print_exc(file=sys.stdout)
    


class ServerServicer(service_pb2_grpc.ServerServicer):
    project_uid = PROJECT_UID
    def __init__(self):
        self.private = Private(self.project_uid)

    def Foo(self, request, context):
        return service_pb2.Empty()

    def Private(self, request, context):
        try:
            if str(request.project_uid) != str(self.project_uid):
                raise Exception("Incorrect project ID")
            req = json.loads(request.json)
            res = self.private.execute(str(req.get('cmd')))
            ret = {'status': 'success', 'response': res}
            return service_pb2.PrivateParcel(json=json.dumps(ret), project_uid=request.project_uid)    
        except Exception as err:
            ret = {'status': 'failed'}
            return service_pb2.PrivateParcel(json=json.dumps(ret), project_uid=request.project_uid)

def main():
    port = '51134'

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

