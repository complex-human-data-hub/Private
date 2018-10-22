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

input_line = input("> ")
while input_line != 'exit':
    if input_line.strip() == "sv":
      print(depGraph)
    elif input_line.strip() == "drawTree":
      draw_graph(depGraph.graph)
    else:
      try:
        parse_tree = parser.parse(input_line)

      except Exception as e:  # didn't parse
        print(e)
      else:
        try:
            result = visit_parse_tree(parse_tree, InputVisitor())
            print(result)
            result = result[0]

            variable = result[0][4:-4] # The variable that is being assigned
            relation = result[1] # Either "=" or "~", deterministic or probabalistic
            code = result[2] # The code that needs to be evaluated to get the value
                             # of the variable

            # Remove ID tags and get a list of all predecessor variables in code
            code, preds = remove_id_tags(code)

            # Remove FN tags and prepare code for eval
            code = remove_fn_tags(code, func_dict)
    
            # Add new relation to the dependency graph
            graph_updated, cycle = depGraph.updateGraph(variable, preds)
            if graph_updated:
                depGraph.define(variable, code, preds)
                depGraph.compute()
            else:
                print("Cycle Error:")
                print(cycle)
        except Exception as e:
            print(e)
            traceback.print_exc(file=sys.stdout)

    input_line = input("> ")


exit()
