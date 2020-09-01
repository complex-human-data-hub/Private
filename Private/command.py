from __future__ import print_function
from __future__ import absolute_import
import sys
import re
import traceback
import logging
import argparse
from Private.config import logfile
from arpeggio import NoMatch

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
    current_probabilistic = set()
    current_deterministic = set()
    syntax_errors = []
    for i in range(len(code_lines)):
        if not code_lines[i].isspace():
            if code_lines[i].startswith("def "):
                function_start = i
                function_code = ""
                function_lines = []
                try:
                    function_code += code_lines[i] + '\n'
                    function_lines.append(code_lines[i])
                    function_complete = False
                    while not function_complete:
                        i += 1
                        if code_lines[i].startswith("    "):
                            function_code += code_lines[i] + ';'
                            function_lines.append(code_lines[i] + ';')
                            if code_lines[i].strip().startswith("return"):
                                function_complete = True
                                function_name = parser.parse(function_code).value.split('|')[1].strip()
                                current_deterministic.add(function_name)
                        else:
                            function_complete = True
                            parser.parse(function_code).value.split('|')[1].strip()

                except NoMatch as e:
                    position = e.position
                    for j, function_line in enumerate(function_lines):
                        if position - len(function_line) > 0:
                            position = position - len(function_line)
                        else:
                            syntax_errors.append((function_start + j +1, position))
                            break

            elif not code_lines[i].startswith("    "):
                try:
                    if '=' in code_lines[i]:
                        variable = parser.parse(code_lines[i]).value.split('|')[0].strip()
                        current_deterministic.add(variable)
                    elif '~' in code_lines[i]:
                        variable = parser.parse(code_lines[i]).value.split('|')[0].strip()
                        current_probabilistic.add(variable)
                except NoMatch as e:
                    syntax_errors.append((i+1, e.position))

    if syntax_errors:
        raise Exception({'status': 'failed', 'type': 'syntax_error', 'value': syntax_errors})


    delete_probabilistic = graph.probabilistic.difference(current_probabilistic)
    delete_deterministic = graph.deterministic.difference(current_deterministic).difference(graph.builtins)

    for v in delete_probabilistic:
        graph.delete(v, is_prob=True)

    for v in delete_deterministic:
        graph.delete(v, is_prob=False)

    function_code = ""
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
