from __future__ import print_function

import inspect
import sys
import io

import numpy as np
import networkx as nx
# import pp
import time
import pydot
import graphviz
import logging
import importlib
import json
from Private.builtins import prob_builtins, showBuiltins, showProbBuiltins, commands, plot_builtins

from networkx.drawing.nx_pydot import write_dot
from Private.graph import *

from arpeggio import SemanticActionResults, PTNodeVisitor, visit_parse_tree
#import logging
#_log = logging.getLogger("Private")
#logging.basicConfig(filename='private.log',level=logging.WARNING)

def _debug(msg):
    with open('/tmp/private-debug.log', 'a') as fp:
        if not isinstance(msg, str):
            msg = json.dumps(msg)
        fp.write("{}\n".format( msg ))


#debug = False
depGraph = graph()

class result:

    def __init__(self, result_type, code = None, depend = None, evalcode = None, pyMC3code = None, defines =()):
        self.result_type = result_type
        self.code = code
        if evalcode == None:
            self.evalcode = code
        else:
            self.evalcode = evalcode
        self.pyMC3code = pyMC3code
        self.depend = None
        self.defines = defines
        if depend:
            if type(depend) == SemanticActionResults:
                self.depend = []
                for child in depend:
                    if child.__class__.__name__ == "result":
                        if child.depend:
                            self.depend.extend(child.depend)
            elif type(depend) == str:
                self.depend = [depend]
            elif type(depend) == str:
                self.depend = [depend]
            else:
                raise Exception("result in InputVisitor got a depend that was not None, or SemanticActionResults or a string or a str: " + str(depend) + " is a " + str(type(depend)))

    def remove_dependencies(self, dependenciesToRemove):
        self.depend = list(set(self.depend) - set(dependenciesToRemove))

    def __repr__(self):
        return "type: " + self.result_type + " code: " + self.code + " evalcode: " + str(self.evalcode) + "  depend: " + str(self.depend) + " defines: " + str(self.defines)

class InputVisitor(PTNodeVisitor):
    def __init__(self, defaults=True, **kwargs):
        self.depGraph = kwargs.get('depGraph')
        super(InputVisitor, self).__init__()

    def visit_identifier(self, node, children):
        if node.value in commands:
            raise Exception("Exception: Illegal Identifier '" + node.value + "' is a Private Command")
        return result("identifier", node.value, node.value)

    def visit_distribution_name(self, node, children):
        return result("distribution_name", node.value, node.value)

    def visit_dottedidentifier(self, node, children):
        n = ".".join(c if type(c) == str else c.code for c in children)
        # any dotted identifiers reduce to ther first identifier as a dependency
        #depend = children[0] if type(children[0]) == unicode else children[0].code
        return result("dottedidentifier", n, children[0].code)

    def visit_number(self, node, children):                   return result("number", node.value)
    def visit_string(self, node, children):                   return result("string", node.value)
    def visit_comment_string(self, node, children):           return result("comment_string", node.value)
    def visit_boolean(self, node, children):                  return result("boolean", node.value)
    def visit_notsym(self, node, children):                   return result("notsym", node.value)
    def visit_starsym(self, node, children):                  return result("starsym", node.value)
    def visit_leftsquarebrack(self, node, children):          return result("leftsquarebrack", node.value)
    def visit_rightsquarebrack(self, node, children):         return result("rightsquarebrack", node.value)
    def visit_comma(self, node, children):                    return result("comma", node.value)
    def visit_left_bracket(self, node, children):             return result("leftbracket", node.value)
    def visit_right_bracket(self, node, children):            return result("rightbracket", node.value)
    def visit_keyword_define(self, node, children):           return result("define", node.value)
    def visit_keyword_return(self, node, children):           return result("return", node.value)
    def visit_colon(self, node, children):                    return result("colon", node.value)
    def visit_atom(self, node, children):
        return result("atom", children[0].code, children)
    def visit_identifier_list(self, node, children):
        if len(children) == 1:
            return result("identifier_list", children[0].code, children)
        else:
            return result("identifier_list", ", ".join(c if type(c) == str else c.code for c in children), children)
    def visit_enumerated_list(self, node, children):
        return result("enumerated_list", "[" + ", ".join([c.code for c in children]) + "]", children)
    def visit_list_comprehension(self, node, children):
        if len(children) == 5:
            res = result("list_comprehension", "[" + children[0].code + " for " + children[2].code + " in " + children[4].code + "]", children)
        else:
            res = result("list_comprehension", "[" + children[0].code + " for " + children[2].code + " in " + children[4].code + " if " + children[6].code + "]", children)
        res.remove_dependencies(children[2].depend)
        return res
    def visit_private_list(self, node, children):
        return result("private_list", children[0].code, children)

    def visit_bracketed_expression(self, node, children):
        return result("bracketed_expression", "(" + " ".join(c if type(c) == str else c.code for c in children) + ")", children)

    def visit_factor(self, node, children):
        if len(children) == 1:
            return result("factor", children[0].code, children, evalcode = children[0].evalcode)
        else:
            code = " ".join(c if type(c) == str else c.code for c in children)
            evalcode = " ".join(c if type(c) == str else c.evalcode for c in children)
            return result("factor", code, children, evalcode=evalcode)

    def visit_list_index(self, node, children):
        code = " ".join(c if type(c) == str else c.code for c in children)
        evalcode = " ".join(c if type(c) == str else c.evalcode for c in children)
        return result("list_index", code, children, evalcode=evalcode)

    def visit_comparison(self, node, children):
        if len(children) == 1:
            return result("comparison", children[0].code, children, evalcode = children[0].evalcode)
        else:
            code = " ".join(c if type(c) == str else c.code for c in children)
            evalcode = " ".join(c if type(c) == str else c.evalcode for c in children)
            return result("comparison", code, children, evalcode=evalcode)

    def visit_boolean_expression(self, node, children):
        if len(children) == 1:
            return result("boolean_expression", children[0].code, children, evalcode = children[0].evalcode)
        else:
            code = " ".join(c if type(c) == str else c.code for c in children)
            evalcode = " ".join(c if type(c) == str else c.evalcode for c in children)
            return result("boolean_expression", code, children, evalcode=evalcode)

    def visit_term(self, node, children):
        if len(children) == 1:
            return result("term", children[0].code, children, evalcode = children[0].evalcode)
        else:
            code = " ".join(c if type(c) == str else c.code for c in children)
            evalcode = " ".join(c if type(c) == str else c.evalcode for c in children)
            return result("term", code, children, evalcode=evalcode)

    def visit_method_call(self, node, children):
        fn = children[0].code
        return result("method_call", fn + "(" + ", ".join(c.code for c in children[1:] if c != u'') + ")", children)

    def visit_indexed_variable(self, node, children):
        fn = children[0].code
        square_bracket_start = 0
        square_bracket_end = 0
        for i in range(1, len(children)):
            if children[i].result_type == "leftsquarebrack":
                square_bracket_start = i
            if children[i].result_type == "rightsquarebrack":
                square_bracket_end = i
        code_after_bracket = ""
        if len(children) - 1 > square_bracket_end:
            for c in children[square_bracket_end + 1:]:
                if c.result_type == 'expression':
                    code_after_bracket += '[' + c.code + ']'
                else:
                    code_after_bracket += '.' + c.code
        res = result("indexed_variable", fn + "[" + ", ".join(c.code for c in children[square_bracket_start+1:square_bracket_end]) + "]" + code_after_bracket, children)
        if code_after_bracket:
            res.remove_dependencies(children[square_bracket_end+1].depend)
        return res

    def visit_named_argument(self, node, children):
        return result("named_argument", children[0].code + " = " + children[1].code, defines=set(children[0].code))

    def visit_function_call(self, node, children):
        fn = children[0].code
        argument_names = ""
        kw_argument_names = ""
        if fn == "set":
            fn = "frozenset"
        elif fn == "list":
            fn = "tuple"
        elif fn in plot_builtins:
            argument_names = "\", \"".join(
                c if type(c) == str else c.code for c in children[1:] if c.result_type != "named_argument")
            kw_argument_names = "\", \"".join(
                c.replace("\"", "") if type(c) == str else c.code.replace("\"", "") for c in children[1:] if c.result_type == "named_argument")
            argument_names = "[\"" + argument_names + "\"], "
            if len(kw_argument_names)>0:
                kw_argument_names = "[\"" + kw_argument_names + "\"], "
            else:
                kw_argument_names = "[], "
        if len(children)> 1:
            arguments = ", ".join(c if type(c) == str else c.code for c in children[1:])
        else:
            arguments = ""
        code = fn + "(" + argument_names + kw_argument_names + arguments + ")"
        evalcode = fn + "(" + argument_names + kw_argument_names + arguments + ")"
        return result("function_call", code, children, evalcode=evalcode)

    def visit_simple_expression(self, node, children):
        if len(children) == 1:
            return result("simple_expression", children[0].code, children, evalcode = children[0].evalcode)
        else:
            code = " ".join(c if type(c) == str else c.code for c in children)
            evalcode = " ".join(c if type(c) == str else c.evalcode for c in children)
            return result("simple_expression", code, children, evalcode=evalcode)

    def visit_expression(self, node, children):
        if len(children) == 1:
            return result("expression", children[0].code, children, evalcode = children[0].evalcode)
        else:
            code = " ".join(c if type(c) == str else c.code for c in children)
            evalcode = " ".join(c if type(c) == str else c.evalcode for c in children)
            return result("expression", code, children, evalcode=evalcode)

    def visit_deterministic_assignment(self, node, children):
        self.depGraph.define(children[0].code, children[1].code, evalcode=children[1].evalcode, dependson=children[1].depend)
        return result("deterministic_assignment", children[0].code, evalcode=children[0].evalcode)

    def visit_distribution_parameter(self, node, children):
        if len(children) == 1:
            return result("distribution_parameter", children[0].code, children, pyMC3code= children[0].code)
        else:
            return result("distribution_parameter", children[0].code+"[" + children[1].code+"]", children, pyMC3code=children[0].code+"[__" + children[1].code+"_Indices]")

    def visit_distribution_call(self, node, children):
        fn = children[0].code
        private_code = fn + "(" + ", ".join(c.code for c in children[1:]) + ")"
        #if fn not in prob_builtins:
        #  raise Exception("Unknown distribution: " + fn)
        pyMC3_code = "pymc3." + fn + "(\'%s\', " + ", ".join(c.pyMC3code for c in children[1:]) + "%%s)"
        return result("distribution_call", private_code, children, pyMC3code=pyMC3_code)

    def visit_distribution_assignment(self, node, children):
        if len(children) > 2: # then we have a hierarchically defined variable
            dependson = children[1].depend + children[2].depend
            self.depGraph.define(children[0].code, children[2].code, dependson=dependson, prob = True, hier=children[1].code, pyMC3code=children[0].code + " = " + children[2].pyMC3code % children[0].code)
        else:
            self.depGraph.define(children[0].code, children[1].code, dependson=children[1].depend, prob = True, pyMC3code=children[0].code + " = " + children[1].pyMC3code % children[0].code)
        return result("distribution_assignment", children[0].code)

    def visit_expression_assignment(self, node, children):
        self.depGraph.define(children[0].code, children[1].code, dependson=children[1].depend, prob = True, pyMC3code=children[0].code + " = " + children[1].code + "%s")
        return result("expression_assignment", children[0].code)

    def visit_probabilistic_assignment(self, node, children):
        return result("probabilistic_assignment", children[0].code)

    def visit_assignment(self, node, children):
        if len(children) > 1:
            self.depGraph.add_comment(children[0].code, children[1].code)
        #depGraph.compute()
    def visit_command(self, node, children):                  return result("command", children[0].code)
    def visit_draw_tree(self, node, children):                return result("draw_tree", self.depGraph.draw_dependency_graph())
    def visit_show_variables(self, node, children):           return result("show_variables", str(self.depGraph))
    def visit_show_values(self, node, children):              return result("show_values", self.depGraph.show_values())
    def visit_clear_variables(self, node, children):
        self.depGraph.__init__(events=self.depGraph.globals["All"]["Events"], project_id=self.depGraph.project_id)
        return result("clear_variables", "All variables removed.")
    def visit_show_dependencies(self, node, children):        return result("show_dependencies", self.depGraph.show_dependencies())
    def visit_show_code(self, node, children):                return result("show_code", self.depGraph.show_code())
    def visit_show_eval_code(self, node, children):           return result("show_eval_code", self.depGraph.show_eval_code())
    def visit_show_mccode(self, node, children):              return result("show_mccode", self.depGraph.constructPyMC3code()[1])
    def visit_show_sampler_status(self, node, children):      return result("show_sampler_status", self.depGraph.canRunSampler("All", verbose=True))
    #def visit_show_sampler_chains(self, node, children):      return result("show_sampler_chains", self.depGraph.showSamplerChains())
    def visit_show_sampler_results(self, node, children):     return result("show_sampler_results", self.depGraph.showSamplerResults())
    def visit_show_pp_stats(self, node, children):            return result("show_pp_stats", repr(self.depGraph.server.get_stats()['local']))
    def visit_show_sets(self, node, children):                return result("show_sets", self.depGraph.show_sets())
    def visit_show_globals(self, node, children):             return result("show_globals", self.depGraph.showGlobals())
    def visit_show_jobs(self, node, children):                return result("show_jobs", self.depGraph.show_jobs())
    def visit_variables_to_calculate(self, node, children):   return result("show_variables_to_calculate", self.depGraph.variablesToBeCalculated())
    def visit_variables_to_sample(self, node, children):      return result("show_variables_to_sample", self.depGraph.variablesToBeSampled())
    def visit_show_builtins(self, node, children):            return result("show_builtins", showBuiltins())
    def visit_show_prob_builtins(self, node, children):       return result("show_prob_builtins", showProbBuiltins())
    def visit_show_ncpus(self, node, children):               return result("show_ncpus", str(self.depGraph.server.get_ncpus()))
    def visit_show_stats(self, node, children):               return result("show_stats", str(self.depGraph.server.print_stats()))
    def visit_comment_line(self, node, children):             return result("comment_line", "")
    def visit_delete(self, node, children):                   return result("show_delete", self.depGraph.delete(children[1].code))
    def visit_help(self, node, children):
        res = """
clear: remove all variables and restart
dt: draw variable dependency tree
sv: show variables
sd: show dependencies
spp: show pp stats
scode: show code
sevalcode: show eval code
smccode: show pyMC3 code
sss: show sampler status
ssr: show sampler results
ss: show sets
sg: show globals
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

    def visit_comment(self, node, children):
        #_log.debug("comment: " + str(children))
        self.depGraph.add_comment(children[0].code, children[1].code)

    def visit_line(self, node, children):
        if len(children) > 0:
            return children[0].code
        else:
            return

    def visit_func_det_assignment(self, node, children):
        code = children[0].code + " = " + " ".join(c if type(c) == str else c.code for c in children[1:])
        res = result("func_deterministic_assignment", code, children, evalcode=code, defines=set(children[0].depend))
        res.remove_dependencies(children[0].depend)
        return res

    def visit_function_header(self, node, children):
        defines = set()
        for c in children:
            defines = defines.union(c.defines)
        children[1].remove_dependencies(children[1].depend)
        code = " ".join(c if type(c) == str else c.code for c in children)
        evalcode = " ".join(c if type(c) == str else c.evalcode for c in children)
        return result("function_header", code, children, evalcode=evalcode, defines=defines)

    def visit_function_body_line(self, node, children):
        defines = set()
        for c in children:
            defines = defines.union(c.defines)
        if len(children) > 0:
            return result("function_body_line", children[0].code, children, evalcode=children[0].code, defines=defines)
        else:
            return

    def visit_function_return(self, node, children):
        code = " ".join(c if type(c) == str else c.code for c in children)
        evalcode = " ".join(c if type(c) == str else c.evalcode for c in children)
        return result("function_return", code, children, evalcode=evalcode)

    def visit_function(self, node, children):
        depends = set()
        defines = set()
        for c in children:
            defines = defines.union(set(c.defines))
        for c in children[1:]:
            depends = depends.union(set(c.depend))
        if len(children) > 1:
            func_name = children[0].code.split(" ")[1]
            code = children[0].code + "\n"
            evalcode = children[0].evalcode + "\n"
            for c in children[1:]:
                if c.result_type == "function_body_line":
                    code += '\t' + c.code + '\n'
                    evalcode += '\t' + c.evalcode + '\n'
                if c.result_type == "function_return":
                    code += '\t' + c.code
                    evalcode += '\t' + c.evalcode
            self.depGraph.define_function(func_name, code, evalcode, depends, defines, set(children[0].depend))
            return

    def visit_code_block(self, node, children):
        if len(children) > 0:
            return children[0]
        else:
            return

    def visit_value(self, node, children):
        print(self.depGraph.getValue(node.value, longFormat=True))

    def visit_command_line_expression(self, node, children):
        return result("command_line_expression",
                      str(self.depGraph.eval_command_line_expression(node.value)))

#def PrivateSemanticAnalyser(parse_tree):
#    return visit_parse_tree(parse_tree, InputVisitor())

def PrivateSemanticAnalyser(parse_tree, update_graph=None):
    if not update_graph:
        update_graph = depGraph
    return visit_parse_tree(parse_tree, InputVisitor(depGraph=update_graph))

