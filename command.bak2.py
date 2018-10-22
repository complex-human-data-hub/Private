import sys
import io

import numpy as np
import networkx as nx
import pp
import time
import _thread
import pydot
import graphviz
import logging

from networkx.drawing.nx_pydot import write_dot
from itertools import count
from testpp import *

from arpeggio import *
from parser import PrivateParser

class InputVisitor(PTNodeVisitor):

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

    def visit_exit(self, node, children):
        exit()

    def visit_draw_tree(self, node, children):
        draw_graph(depGraph.graph)
        return

    def visit_show_variables(self, node, children):
        print(depGraph)
        return

    def visit_delete_variable(self, node, children):
        depGraph.delete(children[0])
        return

    def visit_statement(self, node, children):
        return children[0]

    def visit_assign_statement(self, node, children):

        variables = []
        deterministic = (children[1] == "=")
        if (False and not deterministic):
            # Need to change this


            # We are sampling from a distribution
            partitioned = children[2].partition("(")
            distribution_type = partitioned[0]
            return children[0] + " = np.random.{}(".format(distribution_type) + partitioned[2]
        else:

            # Add python code to node
            execute = children[2]

            return children

    def visit_attribute_identifier(self, node, children):
        return node.value.replace(" | ", "")

    def visit_index_identifier(self, node, children):
        return node.value.replace(" | ", "")

    def visit_identifier(self, node, children):
        return node.value

    def visit_any_identifier(self, node, children):
        new = "".join(node.value.replace(" | ", ""))
        return "ID__" + "".join(node.value.replace(" | ", "")) + "__ID"

    def visit_atom(self, node, children):
        return children[0]

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
        children[0] = "FN__" + children[0] + "__FN"
        return children[0] + "(" + ", ".join(children[1:]) + ")"

    def visit_import_statement(self, node, children):
        return node.value.replace(" | ", " ")

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

def draw_graph(graph):
    write_dot(graph, "test.dot")
    return

commands = ["sv", "drawTree", "delete_variable"]
input_lines = []
input_line = ''
parser = PrivateParser()
parse_tree = parser.parse(input_line)
result = visit_parse_tree(parse_tree, InputVisitor())
depGraph = graph()

# List of all functions accepted by private
func_dict = {"unique": "numpy.unique", "mean": "numpy.mean"}


input_line = input("> ")
while input_line != 'exit':

    input_lines.append(input_line)
    try:
        parse_tree = parser.parse(input_line)
    except:
        pass

    try:
        result = visit_parse_tree(parse_tree, InputVisitor())
        print(result)
        result = result[0]
        print(result)

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

        # Check and see if we need to start any jobs
        #if (result and input_line not in commands):
            #dependencies.scan_jobs()
    except:
        pass

    input_line = input("> ")


exit()
