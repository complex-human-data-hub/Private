from Private.parser import get_private_parser
from Private.semantics import private_semantic_analyser

import json
from datetime import datetime
import sys
import io
import logging
import re
import os
import traceback
import argparse

import signal
from concurrent import futures

import grpc
import service_pb2
import service_pb2_grpc


from arpeggio import NoMatch



parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, default=51135)
parser_args = parser.parse_args()

FORMAT = '[%(asctime)s] %(levelname)s - %(message)s'
if logging.getLogger().hasHandlers():
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO, format=FORMAT)

_log = logging.getLogger("gRPC server")

#Import DataSource
from Private.private_data import Source
from Private.graph import Graph

# Regexes
re_oneword = re.compile(r'^[A-Za-z0-9]+$')

def _debug(msg):
    _log.info(msg)


class Private:
    project_uid = None
    parser = get_private_parser()
    data_source = None
    def __init__(self, project_uid, events=None, load_demo_events=True, shell_id=None, user_ids=None):
        self.project_uid = project_uid
        self.graph = None 
        self.load_demo_events = load_demo_events
        self.shell_id = shell_id
        self.user_ids = user_ids
        if events or user_ids:
            self.graph = Graph(events=events, project_id=self.project_uid, load_demo_events=self.load_demo_events, shell_id=shell_id, user_ids=user_ids)


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
                    result = private_semantic_analyser(parse_tree, update_graph=self.graph)
                    _debug({'result': result})
                    return(result)
                except Exception as e:
                    _debug({'error': str(e)})
                    traceback.print_exc(file=sys.stdout)
                    return ( str(e) )


    def remove_comments(self, s):
        if "#" in s:
            return s[0:s.index("#")]
        return s


    def execute_lines(self, code_lines):
        result = None
        current_probabilistic = set()
        current_deterministic = set()
        syntax_errors = []
        for i in range(len(code_lines)):
            code_line = self.remove_comments(code_lines[i])
            if code_line and not code_line.isspace():
                if code_line.startswith("def "):
                    function_start = i
                    function_code = ""
                    function_lines = []
                    try:
                        function_code += code_line + '\n'
                        function_lines.append(code_line)
                        function_complete = False
                        while not function_complete:
                            i += 1
                            code_line = self.remove_comments(code_lines[i])
                            if code_line.startswith("    "):
                                function_code += code_line + ';'
                                function_lines.append(code_line + ';')
                                if code_line.strip().startswith("return"):
                                    function_complete = True
                                    function_name = self.parser.parse(function_code).value.split('|')[1].strip()
                                    current_deterministic.add(function_name)
                            else:
                                function_complete = True
                                self.parser.parse(function_code).value.split('|')[1].strip()

                    except NoMatch as e:
                        position = e.position
                        for j, function_line in enumerate(function_lines):
                            if position - len(function_line) > 0:
                                position = position - len(function_line)
                            else:
                                syntax_errors.append((function_start + j +1, position))
                                break

                elif not code_line.startswith("    "):
                    try:
                        if '=' in code_line:
                            variable = self.parser.parse(code_line).value.split('|')[0].strip()
                            current_deterministic.add(variable)
                        elif '~' in code_lines[i]:
                            variable = self.parser.parse(code_line).value.split('|')[0].strip()
                            current_probabilistic.add(variable)
                        elif code_line.strip():
                            # We have some code that will throw syntax error (i.e., no = or ~)
                            variable = self.parser.parse(code_line).value.split('|')[0].strip()

                    except NoMatch as e:
                        syntax_errors.append((i+1, e.position))

        if syntax_errors:
            raise Exception({'status': 'failed', 'type': 'syntax_error', 'value': syntax_errors})


        keep_private_variables = {'NumberOfSamples', 'NumberOfTuningSamples', 'NumberOfChains', 'rhat', 'ess', 'loo',
                              'waic'}

        delete_probabilistic = self.graph.probabilistic.difference(current_probabilistic)
        delete_deterministic = self.graph.deterministic.difference(current_deterministic).difference(self.graph.builtins).difference(keep_private_variables)

        for v in delete_probabilistic:
            self.graph.delete(v, is_prob=True)

        for v in delete_deterministic:
            self.graph.delete(v, is_prob=False)

        function_code = ""
        for line in code_lines:
            input_line = self.remove_comments(line)
            if input_line.startswith("def"):
                function_code += input_line + '\n'
                continue

            if input_line.startswith("    "):
                function_code += input_line + ';'
                if input_line.strip().startswith("return"):
                    result = self.execute(function_code)
                    function_code = ""
                continue

            elif input_line.strip() != "":
                result = self.execute(input_line)

        return(result) # This should really be an array of results



class ServerServicer(service_pb2_grpc.ServerServicer):
    def __init__(self):
        self.private = None
        self.initializing = False
        self.skipped = False #Skip the first return after initializing so we can set our first value
        self.events_cache = "/tmp/uevents-{}.json"
        self.data_source = None

    def Foo(self, request, context):
        return service_pb2.Empty()

    def Private(self, request, context):
        try:
            _debug("received request")

            req = json.loads(request.json)
            cmd = str(req.get('cmd', ''))
            ace_cmd = str(req.get('ace-cmd', ''))

            # Check if we need to reset the Private Server
            if cmd == 'reset' or ace_cmd == 'reset':
                self.private = None
                self.initializing = False
                self.data_source = None
                ret = {'status': 'success', 'response': 'Private Reset'}
                return service_pb2.PrivateParcel(json=json.dumps(ret), project_uid=request.project_uid)

            if not self.private:
                _debug("not private")
                self.data_source = Source(project_id=request.project_uid)
                _debug("load Source")
                user_ids = self.data_source.get_user_ids() 
                _debug("got user_ids")
                self.private = Private(request.project_uid, load_demo_events=True, shell_id=parser_args.port, user_ids=user_ids)
                _debug("private loaded")


            req = json.loads(request.json)
            _debug({'req':req})

            ace_cmd = str(req.get('ace-cmd', ''))
            res = None
            if ace_cmd:
                if (re_oneword.match(ace_cmd)):
                    res = self.private.execute(ace_cmd)
                else:
                    res = self.private.execute_lines(ace_cmd.splitlines())

            ret = {'status': 'success', 'response': res}
            _debug(ret)
            return service_pb2.PrivateParcel(json=json.dumps(ret), project_uid=request.project_uid)
        except Exception as err:
            _debug({'error': str(err), 'traceback': traceback.format_exc()})
            ret = {'status': 'failed', 'response': str(err)}
            return service_pb2.PrivateParcel(json=json.dumps(err.args[0]), project_uid=request.project_uid)


def main():
    port = str( parser_args.port )

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


