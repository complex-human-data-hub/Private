import sys
import io
import traceback

from parser import PrivateParser
from semantics import PrivateSemanticAnalyser
from testpp import graph

def draw_graph(graph):
    write_dot(graph, "test.dot")
    return

parser = PrivateParser()
#depGraph = graph()
# import distributions
parse_tree = parser.parse("from distributions import normal")
result = PrivateSemanticAnalyser(parse_tree)


input_line = raw_input("> ")
while input_line != 'exit':
  if input_line != "":
    try:
      parse_tree = parser.parse(input_line)
    except Exception as e:  # didn't parse
      print(e)
    else:
      try:
        result = PrivateSemanticAnalyser(parse_tree)
        if result:
          print(result)
      except Exception as e:
        print(e)
        traceback.print_exc(file=sys.stdout)

  input_line = raw_input("> ")


exit()
