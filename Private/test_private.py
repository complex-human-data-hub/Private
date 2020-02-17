from __future__ import print_function
from __future__ import absolute_import
import sys
import time
import traceback
import logging
import argparse
from Private.config import logfile
import warnings
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument("filename", nargs="?", default = None)
args = parser.parse_args()

_log = logging.getLogger("Private")
logging.basicConfig(filename=logfile,level=logging.DEBUG)
_log.debug("============================= Starting new interpreter =============================")

from Private.parser import PrivateParser
from Private.semantics import PrivateSemanticAnalyser

current_graph = None


def execute(line):
    if line != "":
        try:
            parse_tree = parser.parse(line)
        except Exception as e:  # didn't parse
            print("Syntax Error: " + line[:e.position] + "*" + line[e.position:])
        else:
            try:
                result = PrivateSemanticAnalyser(parse_tree, update_graph=current_graph)
                if result:
                    return result
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                return "Error: " + str(e)


def load_code(filename):
    f = open(filename, "r").readlines()
    test_name = ""
    for line in f:
        if line.startswith("test"):
            if test_name != "":
                check_test(test_name)
            test_name = line.split(" ")[1][:-1]
            execute("clear")
        else:
            execute(line[0:-1])
    check_test(test_name)


def check_test(test_name):
    result_ready = False
    while not result_ready:
        results = execute("result")
        if results.startswith("["):
            result = execute("all(result)")
            value = execute("sum(result)")
            length = execute("len(result)")
            if result == "True":
                print(test_name, ": All Tests Passed -", value, "/", length)
                result_ready = True
            elif result == "False":
                print(test_name, ": Some Tests Failed-", value, "/", length)
                result_ready = True
        elif "result is undefined" in results:
            print(test_name, ": No Tests Defined")
            result_ready = True
        elif "Error" in results or "Exception" in results or "undefined" in results:
            print(test_name, ": Tests Failed, Exception ", results)
            result_ready = True
        time.sleep(2)


parser = PrivateParser()
if args.filename:
    load_code(args.filename)

exit()
