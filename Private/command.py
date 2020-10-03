from __future__ import print_function
from __future__ import absolute_import

import json
import sys
import re
import time
import traceback
import logging
import argparse
from Private.config import logfile
from arpeggio import NoMatch
import threading
import copy
import random
import os

parser = argparse.ArgumentParser()
parser.add_argument("filename", nargs="?", default = None)
args = parser.parse_args()

_log = logging.getLogger("Private")
logging.basicConfig(filename=logfile,level=logging.DEBUG)
_log.debug("============================= Starting new interpreter =============================")

from Private.parser import get_private_parser
from Private.semantics import PrivateSemanticAnalyser
from Private.graph import Graph
from datetime import datetime

graph = Graph()
test_folder = "tests"


def test_logger(msg):
    with open(test_folder + "/testing.log", "a") as fp:
        if not isinstance(msg, str):
            msg = json.dumps(msg, indent=4, default=str)
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        fp.write("[{}][{}] {}\n".format(timestamp, os.getpid(), msg))


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


def code_line_to_block(code_lines):
    code_blocks = []
    for code_line in code_lines:
        if code_line.startswith("    "):
            code_blocks[-1].append(code_line)
        else:
            code_blocks.append([code_line])
    return code_blocks


def code_block_to_lines(code_blocks):
    code_lines = []
    for code_block in code_blocks:
        code_lines.extend(code_block)
    return code_lines


def execute_test(test_cases, p_limit, t_limit):
    random.seed(123465)
    test_case_ext = '.test'
    expected_ext = '.expected'
    result_file = 'result.log'
    if test_cases == '*':
        test_files = [f for f in os.listdir(test_folder) if f.endswith(test_case_ext)]
    else:
        test_files = [test]
    test_logger("Starting testing for files: " + str(test_files))
    with open(test_folder + "/" + result_file, "w+") as fp:
        for test_file in test_files:
            test_logger("Starting testing: " + test_file)
            test_name = test_file.split('.')[0]
            if os.path.isfile(test_folder + "/" + test_name + expected_ext):
                result = open(test_folder + "/" + test_name + expected_ext, "r").read()
            else:
                result = None
            try:
                fp.write(f"Starting test {test_name}\n")
                start = int(round(time.time()))
                now = start
                code_lines = open(test_folder + "/" + test_name + test_case_ext, "r").readlines()
                failed = []
                permutations_tried = 0
                for i in range(p_limit):
                    permutations_tried += 1
                    execute_lines(code_lines)
                    job_count = 1
                    while job_count > 0:
                        time.sleep(10)
                        sj = json.loads(graph.show_jobs(True))
                        test_logger(sj)
                        job_count = sum(sj.values())
                    r = graph.test_variables_dict()
                    if not result:
                        with open(test_folder + "/" + test_name + expected_ext, "w+") as res_file:
                            res_file.write(r)
                            result = r
                    if r != result:
                        failed.append((copy.copy(code_lines), r))
                    execute_lines([])
                    now = int(round(time.time()))
                    if (now - start)/60 > t_limit:
                        break
                    code_blocks = code_line_to_block(code_lines)
                    random.shuffle(code_blocks)
                    code_lines = code_block_to_lines(code_blocks)
                if failed:
                    fp.write("Test Status: Failed\n")
                else:
                    fp.write("Test Status: Passed\n")
                fp.write(f"Number of permutations tested: {permutations_tried}\n")
                fp.write(f"Time Spent: {(now - start)/60} minutes\n")
                if failed:
                    fp.write("Failed test cases\n")
                    count = 1
                    for fail, wrong_val in failed:
                        fp.write(f'--------------failed: {count} ----------------\n')
                        for line in fail:
                            fp.write(line)
                        fp.write(wrong_val)
                        fp.write('\n')
                        count += 1

            except Exception as e:
                print(e)

    print(open(test_folder + "/" + result_file, "r").read())


def remove_comments(s):
    if "#" in s:
        return s[0:s.index("#")]
    return s


def execute_lines(code_lines):
    current_probabilistic = set()
    current_deterministic = set()
    syntax_errors = []
    for i in range(len(code_lines)):
        code_line = remove_comments(code_lines[i])
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
                        code_line = remove_comments(code_lines[i])
                        if code_line.startswith("    "):
                            function_code += code_line + ';'
                            function_lines.append(code_line + ';')
                            if code_line.strip().startswith("return"):
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

            elif not code_line.startswith("    "):
                try:
                    if '=' in code_line:
                        variable = parser.parse(code_line).value.split('|')[0].strip()
                        current_deterministic.add(variable)
                    elif '~' in code_line:
                        variable = parser.parse(code_line).value.split('|')[0].strip()
                        current_probabilistic.add(variable)
                    elif code_line.strip():
                        # We have some code that will throw syntax error (i.e., no = or ~)
                        parser.parse(code_line).value.split('|')[0].strip()

                except NoMatch as e:
                    syntax_errors.append((i+1, e.position))

    if syntax_errors:
        raise Exception({'status': 'failed', 'type': 'syntax_error', 'value': syntax_errors})

    keep_private_variables = {'NumberOfSamples', 'NumberOfTuningSamples', 'NumberOfChains', 'rhat', 'ess', 'loo',
                              'waic'}
    delete_probabilistic = graph.probabilistic.difference(current_probabilistic)
    delete_deterministic = graph.deterministic.difference(current_deterministic).difference(graph.builtins).difference(
        keep_private_variables)

    for v in delete_probabilistic:
        graph.delete(v, is_prob=True)

    for v in delete_deterministic:
        graph.delete(v, is_prob=False)

    function_code = ""
    for line in code_lines:
        input_line = remove_comments(line[0:-1])
        if input_line.startswith("def"):
            function_code += input_line + '\n'
            continue

        if input_line.startswith("    "):
            function_code += input_line + ';'
            if input_line.strip().startswith("return"):
                execute(function_code)
                function_code = ""
            continue

        elif input_line.strip() != "":
            execute(input_line)


parser = get_private_parser()
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
    elif input_line.startswith("test"):
        args = input_line.strip().split()
        test = args[1]
        permutation_limit = 50
        time_limit = 60
        if len(args) > 2:
            options_str = input_line.strip().split('-')[1:]
            options = {}
            for option_str in options_str:
                op, val = option_str.strip().split()
                if op == 'p':
                    permutation_limit = int(val)
                elif op == 't':
                    time_limit = int(val)
        else:
            permutation_limit = 1
        x = threading.Thread(target=execute_test, args=(test, permutation_limit, time_limit))
        x.start()
        x.join()
    elif input_line != "":
        execute(input_line)

    input_line = input("> ")


exit()
