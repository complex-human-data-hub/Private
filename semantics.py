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
from builtins import prob_builtins, showBuiltins, showProbBuiltins

from networkx.drawing.nx_pydot import write_dot
from graph import *

from arpeggio import SemanticActionResults, PTNodeVisitor, visit_parse_tree
#import logging
#_log = logging.getLogger("Private")
#logging.basicConfig(filename='private.log',level=logging.WARNING)


#debug = False

class result:

  def __init__(self, result_type, code = None, depend = None, evalcode = None, pyMC3code = None):
    self.result_type = result_type
    self.code = code
    if evalcode == None:
      self.evalcode = code
    else:
      self.evalcode = evalcode
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
      elif type(depend) == unicode:
        self.depend = [depend]
      else:
        raise Exception("result in InputVisitor got a depend that was not None, or SemanticActionResults or a string or a unicode: " + str(depend) + " is a " + str(type(depend)))

  def remove_dependencies(self, dependenciesToRemove):
    self.depend = list(set(self.depend) - set(dependenciesToRemove)) 

  def __repr__(self):
    return "type: " + self.result_type + " code: " + self.code + " evalcode: " + str(self.evalcode) + "  depend: " + str(self.depend)

class InputVisitor(PTNodeVisitor):

    def visit_identifier(self, node, children):
        return result("identifier", node.value, node.value)

    def visit_distribution_name(self, node, children):
        return result("distribution_name", node.value, node.value)

    def visit_dottedidentifier(self, node, children):
        n = ".".join(c if type(c) == unicode else c.code for c in children)
        # any dotted identifiers reduce to ther first identifier as a dependency
        #depend = children[0] if type(children[0]) == unicode else children[0].code
        return result("dottedidentifier", n, children[0].code)

    def visit_number(self, node, children):                   return result("number", node.value)
    def visit_string(self, node, children):                   return result("string", node.value)
    def visit_comment_string(self, node, children):           return result("comment_string", node.value)
    def visit_boolean(self, node, children):                  return result("boolean", node.value)
    def visit_notsym(self, node, children):
        return result("notsym", node.value)
    def visit_starsym(self, node, children):
        return result("notsym", node.value)
    def visit_atom(self, node, children):
        return result("atom", children[0].code, children)
    def visit_identifier_list(self, node, children):
        if len(children) == 1:
           return result("identifier_list", children[0].code, children)
        else:
          return result("identifier_list", ", ".join(c if type(c) == unicode else c.code for c in children), children)
    def visit_enumerated_list(self, node, children):
        return result("enumerated_list", "[" + ", ".join([c.code for c in children]) + "]", children)
    def visit_list_comprehension(self, node, children):
        if len(children) == 3:
          res = result("list_comprehension", "[" + children[0].code + " for " + children[1].code + " in " + children[2].code + "]", children)
        else:
          res = result("list_comprehension", "[" + children[0].code + " for " + children[1].code + " in " + children[2].code + " if " + children[3].code + "]", children)
        res.remove_dependencies(children[1].depend)
        return res
    def visit_list(self, node, children):
        return result("list", children[0].code, children)
    
    def visit_bracketed_expression(self, node, children):
        return result("bracketed_expression", "(" + " ".join(c if type(c) == unicode else c.code for c in children) + ")", children)

    def visit_factor(self, node, children):                   
        if len(children) == 1:
           return result("factor", children[0].code, children, evalcode = children[0].evalcode)
        else:
          code = " ".join(c if type(c) == unicode else c.code for c in children)
          evalcode = " ".join(c if type(c) == unicode else c.evalcode for c in children)
          return result("factor", code, children, evalcode=evalcode)

    def visit_term(self, node, children):
        if len(children) == 1:
           return result("term", children[0].code, children, evalcode = children[0].evalcode)
        else:
          code = " ".join(c if type(c) == unicode else c.code for c in children)
          evalcode = " ".join(c if type(c) == unicode else c.evalcode for c in children)
          return result("term", code, children, evalcode=evalcode)
        
    def visit_method_call(self, node, children):
        fn = children[0].code
        return result("method_call", fn + "(" + ", ".join(c.code for c in children[1:]) + ")", children)

    def visit_indexed_variable(self, node, children):
        fn = children[0].code
        return result("indexed_variable", fn + "[" + ", ".join(c.code for c in children[1:]) + "]", children)

    def visit_function_call(self, node, children):
        fn = children[0].code
        if fn == "set":
          fn = "frozenset"
        elif fn == "list":
          fn = "tuple"
        code = fn + "("+ ", ".join(c.code for c in children[1:]) + ")"
        evalcode = fn + "(" + ", ".join(c.code for c in children[1:]) + ")"
        return result("function_call", code, children, evalcode=evalcode)

    def visit_simple_expression(self, node, children):
        if len(children) == 1:
           return result("simple_expression", children[0].code, children, evalcode = children[0].evalcode)
        else:
          code = " ".join(c if type(c) == unicode else c.code for c in children)
          evalcode = " ".join(c if type(c) == unicode else c.evalcode for c in children)
          return result("simple_expression", code, children, evalcode=evalcode)

    def visit_expression(self, node, children):
        if len(children) == 1:
           return result("expression", children[0].code, children, evalcode = children[0].evalcode)
        else:
          code = " ".join(c if type(c) == unicode else c.code for c in children)
          evalcode = " ".join(c if type(c) == unicode else c.evalcode for c in children)
          return result("expression", code, children, evalcode=evalcode)

    def visit_deterministic_assignment(self, node, children):
        depGraph.define(children[0].code, children[1].code, evalcode=children[1].evalcode, dependson=children[1].depend)
        return result("deterministic_assignment", children[0].code, evalcode=children[0].evalcode)

    def visit_distribution_call(self, node, children):
        fn = children[0].code
        private_code = fn + "(" + ", ".join(c.code for c in children[1:]) + ")"
        #if fn not in prob_builtins:
        #  raise Exception("Unknown distribution: " + fn)
        pyMC3_code = "pymc3." + fn + "(\'%s\', " + ", ".join(c.code for c in children[1:]) + "%%s)"
        return result("distribution_call", private_code, children, pyMC3code=pyMC3_code)
 
    def visit_distribution_assignment(self, node, children): 
        depGraph.define(children[0].code, children[1].code, dependson=children[1].depend, prob = True, pyMC3code=children[0].code + " = " + children[1].pyMC3code % children[0].code)
        return result("distribution_assignment", children[0].code)

    def visit_expression_assignment(self, node, children): 
        depGraph.define(children[0].code, children[1].code, dependson=children[1].depend, prob = True, pyMC3code=children[0].code + " = " + children[1].code + "%s")
        return result("expression_assignment", children[0].code)

    def visit_probabilistic_assignment(self, node, children): 
        return result("probabilistic_assignment", children[0].code)

    def visit_assignment(self, node, children):
        if len(children) > 1:
          depGraph.add_comment(children[0].code, children[1].code)
        #depGraph.compute()
    def visit_command(self, node, children):                  return result("command", children[0].code)
    def visit_draw_tree(self, node, children):                write_dot(depGraph.graph, "VariableDependencyGraph.dot")
    def visit_show_variables(self, node, children):           return result("show_variables", str(depGraph))
    def visit_show_dependencies(self, node, children):        return result("show_dependencies", depGraph.show_dependencies())
    def visit_show_code(self, node, children):                return result("show_code", depGraph.show_code())
    def visit_show_eval_code(self, node, children):           return result("show_eval_code", depGraph.show_eval_code())
    def visit_show_mccode(self, node, children):              return result("show_mccode", depGraph.constructPyMC3code()[1])
    def visit_show_sampler_status(self, node, children):      return result("show_sampler_status", depGraph.canRunSampler(verbose=True))
    def visit_show_sampler_chains(self, node, children):      return result("show_sampler_chains", depGraph.showSamplerChains())
    def visit_show_sampler_results(self, node, children):     return result("show_sampler_results", depGraph.showSamplerResults())
    def visit_show_pp_stats(self, node, children):            return result("show_pp_stats", repr(depGraph.server.get_stats()['local']))
    def visit_show_sets(self, node, children):                return result("show_sets", depGraph.show_sets())
    def visit_show_jobs(self, node, children):                return result("show_jobs", depGraph.show_jobs())
    def visit_variables_to_calculate(self, node, children):   return result("show_variables_to_calculate", depGraph.variablesToBeCalculated())
    def visit_variables_to_sample(self, node, children):      return result("show_variables_to_sample", depGraph.variablesToBeSampled())
    def visit_show_builtins(self, node, children):            return result("show_builtins", showBuiltins())
    def visit_show_prob_builtins(self, node, children):       return result("show_prob_builtins", showProbBuiltins())
    def visit_show_ncpus(self, node, children):               return result("show_ncpus", str(depGraph.server.get_ncpus()))
    def visit_comment_line(self, node, children):             return result("comment_line", "")
    def visit_delete(self, node, children):                   return result("show_delete", depGraph.delete(children[0].code))
    def visit_help(self, node, children):
        res = """
dt: draw variable dependency tree
sv: show variables
sd: show dependencies
scode: show code
sevalcode: show eval code
smccode: show pyMC3 code
sss: show sampler status
ssc: show sampler chains
ssr: show sampler results
ss: show sets
sj: show jobs
vc: variables to calculate
vs: variables to sample
sb: show builtins
spb: show probabilistic builtins
sncpus: show number of cpus
del <name>: delete variable
help: this message
"""
        return result("help", res)
      
#    def visit_short_import(self, node, children):
#        if debug: print "short_import: ", children
#        themodule = importlib.import_module("private_"+children[0])
#        #for k,v in themodule.__private_globals__.items():
#        #  depGraph.globals[children[0]+"_"+k] = v
#        #  depGraph.imports.add(children[0]+"_"+k)
#        depGraph.compute()

#    def visit_import_list(self, node, children):
#        if debug: print "import_list: ", children
#        return result("import_list", " " + ", ".join(c if type(c) == unicode else c.code for c in children), children)

#    def visit_long_import(self, node, children):
#        if debug: print "long_import: ", children
#        themodule = importlib.import_module("private_"+children[0])
#        #for k,v in themodule.__private_globals__.items():
#        #  depGraph.globals[k] = v
#        #  depGraph.imports.add(k)
#        depGraph.compute()

#    def visit_all_import(self, node, children):
#        if debug: print "all_import: ", children

    def visit_comment(self, node, children):
        #_log.debug("comment: " + str(children))
        depGraph.add_comment(children[0].code, children[1].code)

    def visit_line(self, node, children):
      if len(children) > 0:
        return children[0].code
      else:
        return

    def visit_value(self, node, children):
      print depGraph.getValue(node.value, longFormat=True)
         
    def visit_command_line_expression(self, node, children):
      return result("command_line_expression", str(depGraph.eval_command_line_expression(children[0].evalcode, children[0].depend)))
      #print "Because expressions may take a long time to compute you must assign them to a variable"
      #print "and then query the variable to see the result. For example, instead of 4*b+5 type"
      #print "t = 4*b+5 and then t."

def PrivateSemanticAnalyser(parse_tree):
    return visit_parse_tree(parse_tree, InputVisitor())
 
