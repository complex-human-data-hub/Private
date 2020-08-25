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
from Private.graph import Graph

graph = Graph()


def execute(line):
    if line != "":
        try:
            parse_tree = parser.parse(line)
        except Exception as e:  # didn't parse
            print("Syntax Error: " + line[:e.position] + "*" + line[e.position:])
        else:
            try:
                result = PrivateSemanticAnalyser(parse_tree, update_graph=graph)
                if result:
                    print(result)
            except Exception as e:
                print("Error: " + str(e))
                traceback.print_exc(file=sys.stdout)


def get_value(var):
    execute(var)


def execute_block(code_block):
    execute_lines(code_block.split('\n'))


def execute_file(file_name):
    try:
        code_lines = open("samples/" + file_name, "r").readlines()
        execute_lines(code_lines)
    except Exception as e:
        print(e)


def execute_lines(code_lines):
    function_code = ""
    current_probabilistic = set()
    current_deterministic = set()
    for line in code_lines:
        if not line.isspace():
            variable = parser.parse(line).value.split('|')[0].strip()
            if '=' in line:
                current_deterministic.add(variable)
            elif '~' in line:
                current_probabilistic.add(variable)

    delete_probabilistic = graph.probabilistic.difference(current_probabilistic)
    delete_deterministic = graph.deterministic.difference(current_deterministic)

    for v in delete_probabilistic:
        graph.delete(v, is_prob=True)

    for v in delete_deterministic:
        graph.delete(v, is_prob=False)

    for line in code_lines:
        input_line = line[0:-1]
        print(input_line)
        if input_line.startswith("def"):
            function_code += input_line + '\n'
            continue

        if input_line.startswith("    "):
            function_code += input_line + ';'
            if input_line.strip().startswith("return"):
                execute(function_code)
                function_code = ""
            continue

        elif input_line != "":
            execute(input_line)


parser = PrivateParser()
if args.filename:
    execute_file(args.filename)

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
    elif input_line.startswith("file"):
        filename = input_line.split(" ")[1]
        execute_file(filename)
    elif input_line != "":
        execute(input_line)

    input_line = input("> ")


exit()
