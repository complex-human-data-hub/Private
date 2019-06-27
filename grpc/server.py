DEBUG = False

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
import re
import os

import signal
from concurrent import futures

import grpc

import service_pb2
import service_pb2_grpc
import json
from datetime import datetime

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, default=51135)
args = parser.parse_args()


#Setup logging 
logfile = "/tmp/private-{}.log".format(args.port)
logging.basicConfig(filename=logfile,level=logging.DEBUG)

#Import DataSource
#from Private.unforgettable_data import Source
from Private.private_data import Source
from Private.graph import graph

import os 

# Regexes
re_cmd = re.compile(r'\r')


def _debug(msg):
    with open('/tmp/private-debug.log', 'a') as fp:
        if not isinstance(msg, basestring):
            msg = json.dumps(msg)
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        fp.write("[{}][{}] {}\n".format(timestamp, os.getpid(), msg ))


class Private:
    project_uid = None
    parser = PrivateParser()
    data_source = None
    def __init__(self, project_uid):
        self.project_uid = project_uid
        self.graph = None 
        if args.port > 51150:
            self.data_source = Source(args, project_uid=project_uid)
            events = self.data_source.get_events()
            self.graph = graph(events=events)
        _debug("Loading Private")

    def execute(self, line):
        if line != "":
            try:
                parse_tree = self.parser.parse(line)
                _debug({'parse_tree': str(parse_tree)})
            except Exception as e:  # didn't parse
                _debug({'error': str(e)})
                raise Exception("Syntax Error: " + line[:e.position] + "*" + line[e.position:]) 
            else:
                try:
                    result = PrivateSemanticAnalyser(parse_tree, update_graph=self.graph)
                    _debug({'result': result})
                    return(result)
                except Exception as e:
                    _debug({'error': str(e)})
                    traceback.print_exc(file=sys.stdout)
                    return ( str(e) )
    


class ServerServicer(service_pb2_grpc.ServerServicer):
    def __init__(self):
        self.private = None
        self.initializing = False
        self.skipped = False #Skip the first return after initializing so we can set our first value
    def Foo(self, request, context):
        return service_pb2.Empty()

    def Private(self, request, context):
        try:
            _debug("received request")

            if not self.private:
                if not self.initializing:
                    self.initializing = True
                    newpid = os.fork()
                    if newpid == 0:
                        # Not sure if this is okay returning from the child, 
                        # But seems to work
                        ret = {'status': 'success', 'response': 'Initializing dataset [1]'}
                        return service_pb2.PrivateParcel(json=json.dumps(ret), project_uid=request.project_uid)    
                    else:
                        self.private = Private(request.project_uid)
                if self.skipped:
                    #Keep this so that user who keep clicking keep getting an intialising message
                    ret = {'status': 'success', 'response': 'Initializing dataset [2]'}
                    return service_pb2.PrivateParcel(json=json.dumps(ret), project_uid=request.project_uid)    
                else:
                    #Want to skip the parent of the fork coming through
                    #So that after the data is loaded we will issue the 
                    #first incoming command
                    self.skipped = True

            #if str(request.project_uid) != str(self.project_uid):
            #    raise Exception("Incorrect project ID")
            req = json.loads(request.json)
            _debug({'req':req})

            cmd = str(req.get('cmd'))
            res = None
            # Split on the carriage return
            # separate cmds 
            for c in re_cmd.split(cmd):
                res = self.private.execute(c)

            ret = {'status': 'success', 'response': res}
            _debug(ret)
            return service_pb2.PrivateParcel(json=json.dumps(ret), project_uid=request.project_uid)    
        except Exception as err:
            _debug({'error': str(err)})
            ret = {'status': 'failed', 'response': str(err)}
            return service_pb2.PrivateParcel(json=json.dumps(ret), project_uid=request.project_uid)

def main():
    port = str( args.port )

    with open('server.key', 'rb') as f:
        private_key = f.read()
    with open('server.crt', 'rb') as f:
        certificate_chain = f.read()

    server_credentials = grpc.ssl_server_credentials(
      ((private_key, certificate_chain,),))

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    service_pb2_grpc.add_ServerServicer_to_server(ServerServicer(), server)

    #server.add_secure_port('localhost:'+port, server_credentials)
    server.add_secure_port('[::]:'+port, server_credentials)

    server.start()
    try:
        while True:
            signal.pause()
    except KeyboardInterrupt:
        pass
    server.stop(0)

if __name__ == '__main__':
    main()

