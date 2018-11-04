import sys
import io

import numpy as np
import networkx as nx
import pp
import time
import pydot
import graphviz
import logging
import importlib

from networkx.drawing.nx_pydot import write_dot
from testpp import *

from arpeggio import SemanticActionResults, PTNodeVisitor, visit_parse_tree

debug = False

class result:

  def __init__(self, result_type, code = None, depend = None, pyMC3code = None):
    #print "create ", result_type, code, depend
    self.result_type = result_type
    self.code = code
    self.pyMC3code = pyMC3code
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

    def visit_identifier(self, node, children):
        if debug: print "identifier: ", node.value, children
        return result("identifier", node.value, node.value)
    def visit_dottedidentifier(self, node, children):
        if debug: print "dottedidentifier: ", children
        n = "_".join(c if type(c) == unicode else c.code for c in children)
        return result("dottedidentifier", n, n)

    def visit_number(self, node, children):                   return result("number", node.value)
    def visit_string(self, node, children):                   return result("string", node.value)
    def visit_boolean(self, node, children):                  return result("boolean", node.value)
    def visit_notsym(self, node, children):
        if debug: print "notsym: ", children
        return result("notsym", node.value)
    def visit_starsym(self, node, children):
        if debug: print "starsym: ", children
        return result("notsym", node.value)
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

    def visit_distribution_call(self, node, children):
        if debug: print "distribution_call: ", children
        fn = children[0].code
        private_code = fn + "(" + ", ".join(c.code for c in children[1:]) + ")"
        if fn == "normal":
          fn = "Normal"
        elif fn == "halfnormal":
          fn = "HalfNormal"
        else:
          raise Exception("Unknown distribution: " + fn)
        pyMC3_code = "pm." + fn + "(\'%s\', " + ", ".join(c.code for c in children[1:]) + "%%s)"
        return result("distribution_call", private_code, children, pyMC3_code)
 
    def visit_probabilistic_assignment(self, node, children): 
        depGraph.define(children[0].code, children[1].code, dependson=children[1].depend, prob = True, pyMC3code=children[0].code + " = " + children[1].pyMC3code % children[0].code)
        depGraph.compute()

    def visit_assignment(self, node, children):               return 
    def visit_command(self, node, children):                  return 
    def visit_draw_tree(self, node, children):                write_dot(depGraph.graph, "VariableDependencyGraph.dot")
    def visit_show_variables(self, node, children):           print str(depGraph)
    def visit_show_dependencies(self, node, children):        depGraph.show_dependencies()
    def visit_show_mccode(self, node, children):              print depGraph.constructPyMC3code()[1]
    def visit_show_sampler_status(self, node, children):      depGraph.canRunSampler(verbose=True)
    def visit_help(self, node, children):
        print """
dt: draw variable dependency tree
sv: show variables
sd: show dependencies
sm: show pyMC3 code
sss: show sampler status
help: this message
"""
      
    def visit_short_import(self, node, children):
        if debug: print "short_import: ", children
        themodule = importlib.import_module("private_"+children[0])
        for k,v in themodule.__private_globals__.items():
          depGraph.globals[children[0]+"_"+k] = v
        depGraph.compute()

    def visit_import_list(self, node, children):
        if debug: print "import_list: ", children
        return result("import_list", " " + ", ".join(c if type(c) == unicode else c.code for c in children), children)

    def visit_long_import(self, node, children):
        if debug: print "long_import: ", children
        themodule = importlib.import_module("private_"+children[0])
        for k,v in themodule.__private_globals__.items():
          depGraph.globals[k] = v
        depGraph.compute()

    def visit_all_import(self, node, children):
        if debug: print "all_import: ", children

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
 
