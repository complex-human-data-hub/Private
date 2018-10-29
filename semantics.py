import sys
import io

import numpy as np
import networkx as nx
import pp
import time
#import _thread
import pydot
import graphviz
import logging

from networkx.drawing.nx_pydot import write_dot
from testpp import *

from arpeggio import *

def flatten(x):
    return [i for e in x for i in (flatten(e) if isinstance(e,list) else [e])]

def getDeps(children):
    return flatten(c[1] for c in children)

class InputVisitor(PTNodeVisitor):

# the return value for each visit is (code to be executed, list of dependencies)

    def visit_identifier(self, node, children):               return node.value, [node.value]
    def visit_number(self, node, children):                   return node.value, []
    def visit_string(self, node, children):                   return node.value, []
    def visit_atom(self, node, children):                     return children[0]
    def visit_list(self, node, children):                     return "[" + ", ".join([c[0] for c in children]) + "]", getDeps(children)
    def visit_factor(self, node, children):                   return "(" + children[0][0] + ")" if len(children) > 1 else children[0][0], children[0][1]
    def visit_term(self, node, children):                     return children[0]
    def visit_arithmetic_expression(self, node, children):    return " ".join(c[0] for c in children), getDeps(children)
    def visit_boolean_expression(self, node, children):       return node.value  # FIX
    def visit_expression(self, node, children):               return children[0]
    def visit_deterministic_assignment(self, node, children):
      depGraph.define(children[0][0], children[1][0], dependson=children[1][1])
      depGraph.compute()
      return None, []
    def visit_probabilistic_assignment(self, node, children): return children[0] + " ~ " + children[1], []
    def visit_assignment(self, node, children):               return None, []
    def visit_command(self, node, children):                  return children[0]
    def visit_draw_tree(self, node, children):                return "drawtree", []
    def visit_show_variables(self, node, children):           return str(depGraph), []
    def visit_line(self, node, children):
      if len(children) > 0:
        return children[0]
      else:
        return

def PrivateSemanticAnalyser(parse_tree):
     return visit_parse_tree(parse_tree, InputVisitor())[0]
 
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
