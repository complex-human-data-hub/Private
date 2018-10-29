import sys
import io
import traceback

#import numpy as np
#import networkx as nx
#import pp
#import time
#import _thread
#import pydot
#import graphviz
#import logging

#from networkx.drawing.nx_pydot import write_dot
#from itertools import count
#from testpp import *

#from arpeggio import *
from parser import PrivateParser
from semantics import *

def draw_graph(graph):
    write_dot(graph, "test.dot")
    return

parser = PrivateParser()
#parse_tree = parser.parse(input_line)
#result = visit_parse_tree(parse_tree, InputVisitor())
depGraph = graph()

input_line = raw_input("> ")
while input_line != 'exit':
  try:
    parse_tree = parser.parse(input_line)
  except Exception as e:  # didn't parse
    print(e)
  else:
    try:
      result = visit_parse_tree(parse_tree, InputVisitor())
      if result:
        print(result)
    except Exception as e:
      print(e)
      traceback.print_exc(file=sys.stdout)

  input_line = raw_input("> ")


exit()
