from __future__ import print_function
from __future__ import absolute_import
import sys
import traceback
import logging
import argparse
from Private.config import logfile

parser = argparse.ArgumentParser()
parser.add_argument("filename", nargs="?", default = None)
args = parser.parse_args()

_log = logging.getLogger("Private")
logging.basicConfig(filename=logfile,level=logging.DEBUG)
_log.debug("============================= Starting new interpreter =============================")

from Private.parser import PrivateParser
from Private.semantics import PrivateSemanticAnalyser

#from private_data import Source
from Private import graph

#data_source = Source()
#events = data_source.get_events()
#current_graph = graph(events=events)

current_graph = None

def execute(line):
    if line != "":
        try:
            parse_tree = parser.parse(line)
        except Exception as e:  # didn't parse
            print("Syntax Error: " + line[:e.position] + "*" + line[e.position:])
        else:
            try:
                #if not current_graph:
                #    global current_graph 
                #    current_graph = graph(events=events)
                result = PrivateSemanticAnalyser(parse_tree, update_graph=current_graph)
                if result:
                    print(result)
            except Exception as e:
                print("Error: " + str(e))
                traceback.print_exc(file=sys.stdout)

def load_code(filename):
    f = open(filename, "r").readlines()
    function = ""
    for line in f:
        input_line = line[0:-1]
        print(input_line)
        if input_line.startswith("def"):
            function += input_line + '\n'
            continue 

        if input_line.startswith("    "):
            function += input_line + ';'
            if input_line.strip().startswith("return"):
                execute(function)
                function = ""
            continue

        elif input_line != "":
            execute(input_line)

parser = PrivateParser()
if args.filename:
    load_code(args.filename)

input_line = input("> ")
while input_line != 'exit':
    function = ""
    if input_line.startswith("def"):
        function += input_line + '\n'
        input_line = input("> ")
        while input_line.startswith("    "):
            function += input_line + ';'
            if input_line.strip().startswith("return"):
                break
            input_line = input("> ")
        execute(function)
    elif input_line != "":
        execute(input_line)

    input_line = input("> ")


exit()
