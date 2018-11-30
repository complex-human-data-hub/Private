from __future__ import unicode_literals
import sys
import io


from arpeggio import ParserPython, EOF, ZeroOrMore, Optional
from arpeggio import RegExMatch as _

# To do
# - Handle indents?
# - Handle probablistic dependencies (?)
# - Semantic analysis can't handle booleans
# - Can SA do functions? imports?
# - Can't pick up dependency between a and b where a = b[c]
# - Dependencies in list comprehensions?

def command():                  return [delete, \
                                        comment, \
                                        comment_string, \
                                        draw_tree, \
                                        show_variables, \
                                        show_dependencies, \
                                        show_code, \
                                        show_mccode, \
                                        show_sampler_status, \
                                        show_sets, \
                                        variables_to_calculate, \
                                        variables_to_sample, \
                                        show_builtins, \
                                        show_prob_builtins, \
                                        show_ncpus, \
                                        show_cluster_stats, \
                                        help]
def draw_tree():                return "dt"
def show_variables():           return "sv"
def show_dependencies():        return "sd"
def show_code():                return "scode"
def show_mccode():              return "smccode"
def show_sampler_status():      return "sss"
def show_sets():                return "ss"
def variables_to_calculate():   return "vc"
def variables_to_sample():      return "vs"
def show_builtins():            return "sb"
def show_prob_builtins():       return "spb"
def show_ncpus():               return "sncpus"
def show_cluster_stats():       return "scs"
def help():                     return "help"

def identifier():               return _(r'[a-zA-Z_][a-zA-Z0-9_]*')
def comment_string():           return _(r'#[a-zA-Z0-9_ ~=(),*]*')
def module_name():              return _(r'[a-zA-Z_]+')
def notsym():                   return "not"
def starsym():                  return "*"

def dottedidentifier():         return identifier, ZeroOrMore(".", identifier)

#def number():                   return _(r'[+-]?[0-9]+(\.[0-9]+)?')
def number():                   return _(r'[+-]?((\d+(\.\d*)?)|(\.\d+))')
def string():                   return [_(r'(["\'])(?:(?=(\\?))\2.)*?\1'), _(r"([''])(?:(?=(\\?))\2.)*?\1")]
def boolean():                  return ["True", "False"]
def relation():                 return ["==" , "!=" , "<=" , ">=" , "<" , ">" , "in"]
def atom():                     return [number, boolean, string, dottedidentifier]
def identifier_list():          return identifier, ZeroOrMore(",", identifier)
def list_comprehension():       return "[", expression, "for", identifier_list, "in", expression, Optional("if", expression), "]"
def enumerated_list():          return "[", ZeroOrMore(expression, ","), expression, "]"
def list():                     return [list_comprehension, enumerated_list]
def bracketed_expression():     return "(", expression, ")"
def factor():                   return [function_call, method_call, bracketed_expression, (notsym, factor), list, atom]
def term():                     return factor, ZeroOrMore(["*","/", "or"], factor)
def simple_expression():        return Optional(["+", "-"]), term, ZeroOrMore(["+", "-", "and"], term)
def argument():                 return [expression, (identifier, "=", expression)]
def function_call():            return identifier, "(", ZeroOrMore(argument, ","), argument, ")"
def method_call():              return dottedidentifier, "(", ZeroOrMore(expression, ","), expression, ")"
def expression():               return simple_expression, Optional(relation, simple_expression)
def deterministic_assignment(): return identifier, "=", expression

def distribution_call():        return identifier, "(", ZeroOrMore(atom, ","), atom, ")"
def distribution_assignment():  return identifier, "~", distribution_call
def expression_assignment():    return identifier, "~", expression   # deterministic link within probabilistic model
def probabilistic_assignment(): return [distribution_assignment, expression_assignment]
def assignment():               return [deterministic_assignment, probabilistic_assignment], Optional(comment_string)
def value():                    return identifier
def command_line_expression():  return expression # this is here to catch when people enter an expression and explain why that isn't allowed.
#def short_import():             return "import", module_name
#def identifier_list():          return identifier, ZeroOrMore(",", identifier)
#def long_import():              return "from", module_name, "import", [identifier_list, starsym]
#def all_import():               return [short_import, long_import]
def comment():                  return identifier, comment_string
def delete():                   return "del", identifier
def line():                     return [command, assignment, value, command_line_expression, comment_string], EOF

def PrivateParser():
  return(ParserPython(line, debug = False))

if __name__ == "__main__":

  input_lines = [(arithmetic_expression, "9"), \
                 (expression, "True or False"), \
                 (identifier, "a"), \
                 (line, "a="), \
                 (boolean_expression, "True"), \
                 (deterministic_assignment, "a = 9"),
                 (line, "AlisonSimon=9"),
                 (line, "Alison_Simon=9"),
                 (line, "Alison+Simon=9"),
                 (line, "a=b*3"),
                 (line, "a=[b, 3]")]
  
  for rule, input_line in input_lines:
    try: 
      parser = ParserPython(rule, debug=False)
      parse_tree = parser.parse(input_line)
      print parse_tree
      print input_line, " is valid"
    except:
      print input_line, " is invalid"
