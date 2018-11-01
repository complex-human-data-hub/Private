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

def command():                  return [draw_tree, show_variables]
def draw_tree():                return "dt"
def show_variables():           return "sv"
def identifier():               return _(r'[a-zA-Z_]+')
def module_name():              return _(r'[a-zA-Z_]+')

def number():                   return Optional(["+", "-"]), _(r'[0-9]+')
def string():                   return [_(r'(["\'])(?:(?=(\\?))\2.)*?\1'), _(r"([''])(?:(?=(\\?))\2.)*?\1")]
def boolean():                  return ["True", "False"]
def relation():                 return ["==" , "!=" , "<=" , ">=" , "<" , ">" , "in"]
def atom():                     return [number, boolean, string, identifier]
def list():                     return "[", ZeroOrMore(expression, ","), expression, "]"
def factor():                   return [function_call, ("(", expression, ")"), ("not", factor), list, atom]
def term():                     return factor, ZeroOrMore(["*","/", "or"], factor)
def simple_expression():        return term, ZeroOrMore(["+", "-", "and"], term)
def function_call():            return identifier, "(", ZeroOrMore(expression, ","), expression, ")"
def expression():               return simple_expression, Optional(relation, simple_expression)
def deterministic_assignment(): return identifier, "=", expression
def probabilistic_assignment(): return identifier, "~", expression
def assignment():               return [deterministic_assignment, probabilistic_assignment]
def value():                    return identifier
def command_line_expression():  return expression # this is here to catch when people enter an expression and explain why that isn't allowed.
def short_import():             return "import", module_name
def identifier_list():          return identifier, ZeroOrMore(",", identifier)
def long_import():              return "from", module_name, "import", [identifier_list, "*"]
def all_import():               return [short_import, long_import]
def line():                     return [command, all_import, assignment, value, command_line_expression], EOF

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
