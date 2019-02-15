import sys
import io
import traceback
import logging
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("filename", nargs="?", default = None)
args = parser.parse_args()

print "args", args
_log = logging.getLogger("Private")
logging.basicConfig(filename='private.log',level=logging.DEBUG)
_log.debug("============================= Starting new interpreter ======================================")

from parser import PrivateParser
from semantics import PrivateSemanticAnalyser

def execute(line):
    if line != "":
        try:
            parse_tree = parser.parse(line)
        except Exception as e:  # didn't parse
            print("Syntax Error: " + str(e))
        else:
            try:
                result = PrivateSemanticAnalyser(parse_tree)
                if result:
                    print(result)
            except Exception as e:
                print("Error: " + str(e))
                traceback.print_exc(file=sys.stdout)

def load_code(filename):
    f = open(filename, "r").readlines()
    for line in f:
        print line[0:-1]
        execute(line[0:-1])

parser = PrivateParser()
if args.filename:
    load_code(args.filename)

input_line = raw_input("> ")
while input_line != 'exit':
    if input_line != "":
        execute(input_line)

    input_line = raw_input("> ")


exit()
