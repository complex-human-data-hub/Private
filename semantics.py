import sys
import io

import numpy as np
import networkx as nx
import pp
import time
import pydot
import graphviz
import logging

from networkx.drawing.nx_pydot import write_dot
from testpp import *

from arpeggio import SemanticActionResults, PTNodeVisitor, visit_parse_tree

debug = False

class result:

  def __init__(self, result_type, code = None, depend = None):
    #print "create ", result_type, code, depend
    self.result_type = result_type
    self.code = code
    self.depend = None
    if depend:
      if type(depend) == SemanticActionResults:
        self.depend = []
        for child in depend:
          if child.__class__.__name__ == "result":
            if child.depend:
              self.depend.extend(child.depend)
      elif type(depend) == str:
        self.depend = [depend]
      else:
        raise Exception("result in InputVisitor got a depend that was not None, or SemanticActionResults or a string: " + str(depend) + " is a " + str(type(depend)))

  def __repr__(self):
    return "type: " + self.result_type + " code: " + self.code + "  depend: " + str(self.depend)


class InputVisitor(PTNodeVisitor):

    def visit_identifier(self, node, children):               return result("identifier", node.value, node.value)
    def visit_number(self, node, children):                   return result("number", node.value)
    def visit_string(self, node, children):                   return result("string", node.value)
    def visit_boolean(self, node, children):                  return result("boolean", node.value)
    def visit_atom(self, node, children):
        if debug: print "atom: ", children
        return result("atom", children[0].code, children)
    def visit_list(self, node, children):
        return result("list", "[" + ", ".join([c.code for c in children]) + "]", children)
    def visit_factor(self, node, children):                   
        if debug: print "factor: ", children
        if len(children) == 1:
           return result("factor", children[0].code, children)
        else:
          return result("factor", "(" + " ".join(c if type(c) == unicode else c.code for c in children) + ")", children)

    def visit_term(self, node, children):
        if debug: print "term: ", children
        if len(children) == 1:
           return result("term", children[0].code, children)
        else:
          return result("term", "(" + " ".join(c if type(c) == unicode else c.code for c in children) + ")", children)
        
    #def visit_arithmetic_expression(self, node, children):
    #    if debug: print "arithmetic_expression: ", children
    #    if len(children) == 1:
    #       return result("arthimetic_expression", children[0].code, children)
    #    else:
    #      return result("arthimetic_expression", "(" + " ".join(c if type(c) == unicode else c.code for c in children) + ")", children)

    #def visit_boolean_expression(self, node, children):       return result("boolean_expression", node.value)  # FIX

    def visit_function_call(self, node, children):
        if debug: print "function: ", children
        fn = children[0].code
        if fn == "set":
          fn = "frozenset"
        elif fn == "list":
          fn = "tuple"
        return result("function_call", fn + "(" + ", ".join(c.code for c in children[1:]) + ")", children)

    def visit_simple_expression(self, node, children):
        if debug: print "simple_expression: ", children
        if len(children) == 1:
           return result("simple_expression", children[0].code, children)
        else:
          return result("simple_expression", "(" + " ".join(c if type(c) == unicode else c.code for c in children) + ")", children)

    def visit_expression(self, node, children):
        if debug: print "expression: ", children
        if len(children) == 1:
           return result("expression", children[0].code, children)
        else:
          return result("expression", "(" + " ".join(c if type(c) == unicode else c.code for c in children) + ")", children)

    def visit_deterministic_assignment(self, node, children):
        depGraph.define(children[0].code, children[1].code, dependson=children[1].depend)
        depGraph.compute()
        return None

    def visit_probabilistic_assignment(self, node, children): return children[0] + " ~ " + children[1], []
    def visit_assignment(self, node, children):               return 
    def visit_command(self, node, children):                  return 
    def visit_draw_tree(self, node, children):                write_dot(depGraph.graph, "VariableDependencyGraph.dot")
    def visit_show_variables(self, node, children):           print str(depGraph)
      
    def visit_line(self, node, children):
      if len(children) > 0:
        return children[0]
      else:
        return

    def visit_value(self, node, children):
      print depGraph.getValue(node.value)
         
    def visit_command_line_expression(self, node, children):
      print "Because expressions may take a long time to compute you must assign them to a variable"
      print "and then query the variable to see the result. For example, instead of 4*b+5 type"
      print "t = 4*b+5 and then t."

def PrivateSemanticAnalyser(parse_tree):
    return visit_parse_tree(parse_tree, InputVisitor())
 
'''
    def visit_user_entry(self, node, children):
        return children

    def visit_value(self, node, children):
        var = children[0]
        if var in depGraph.uptodate:
            print(depGraph.value[var])
        elif var in depGraph.computing:
            print("Still computing...")
        else:
            print("A value has not been defined yet.")
        return False

    def visit_local_identifier(self, node, children):
        return node.value.replace(" | ", "")

    def visit_delete_variable(self, node, children):
        depGraph.delete(children[0])
        return

    def visit_statement(self, node, children):
        return children[0]

    def visit_assign_statement(self, node, children):

        print "here: ", node, children
        return(node)
        #variables = []
        #deterministic = (children[1] == "=")
        #if (False and not deterministic):
        #    # Need to change this
#
#
#            # We are sampling from a distribution
#            partitioned = children[2].partition("(")
#            distribution_type = partitioned[0]
#            return children[0] + " = np.random.{}(".format(distribution_type) + partitioned[2]
#        else:
#
#            # Add python code to node
#            execute = children[2]
#
#            return children

    def visit_attribute_identifier(self, node, children):
        return node.value.replace(" | ", "")

    def visit_index_identifier(self, node, children):
        return node.value.replace(" | ", "")

    def visit_identifier(self, node, children):
        return node

    def visit_any_identifier(self, node, children):
        print "any_identifier: ", node, children
        #new = "".join(node.value.replace(" | ", ""))
        #return "ID__" + "".join(node.value.replace(" | ", "")) + "__ID"
        return(node)

    def visit_atom(self, node, children):
        #return children[0]
        return(node)

    def visit_expression(self, node, children):
        return " ".join(children)

    def visit_dictionary(self, node, children):
        return node.value.replace(" | ", "")

    def visit_comprehension(self, node, children):
        return " ".join(children)

    def visit_list(self, node, children):
        return "[" + children[0] + "]"

    def visit_array(self, node, children):
        return ", ".join(children)

    def visit_set(self, node, children):
        return "{" + ", ".join(children) + "}"

    def visit_function(self, node, children):
        #children[0] = "FN__" + children[0] + "__FN"
        return children[0] + "(" + ", ".join(children[1:]) + ")"

    def visit_import_statement(self, node, children):
        return node.value

    def command_line_expression(self, node, children):

def extract_variables_from_index_variable(variable):
    split_variable = variable.split("[")
    split_variable[-1] = split_variable[-1][:-len(split_variable)+1]
    dependencies.graph.add_node(split_variable[0])
    dependencies.graph.node[split_variable[0]]["var_defined"] = True
    return split_variable

def remove_id_tags(code):
    output = code
    vars = re.findall(r'ID__[\w\[\(\]\)\.\d]+__ID', code)
    for var in vars:
        output = output.replace(var, var[4:-4])
    return output, [v[4:-4] for v in vars]

def remove_fn_tags(code, func_dict):
    output = code
    funcs = re.findall(r'FN__[\w\[\(\]\)\.\d]+__FN', code)
    for func in funcs:
        output = output.replace(func, func_dict[func[4:-4]])
    return output

#def draw_graph(graph):
#    write_dot(graph, "test.dot")
#    return


# List of all functions accepted by private
func_dict = {"unique": "numpy.unique", "mean": "numpy.mean"}

'''

depGraph = graph()
