import sys
import io


from arpeggio import *
from arpeggio import RegExMatch as _

# To do
# - Handle indents?
# - Handle probablistic dependencies (?)
# - Semantic analysis can't handle booleans
# - Can SA do functions? imports?
# - Can't pick up dependency between a and b where a = b[c]
# - Dependencies in list comprehensions?

# Entry
def user_entry(): return ZeroOrMore([
                                      (statement, Optional(comment)),
                                      (declare_function, Optional(comment)),
                                      comment,
                                      command
                                    ]), EOF

# Statement
def statement(): return [
                          assign_statement,
                          import_statement,
                        ]
def assign_statement(): return any_identifier, ["=", "~"], [function, list, expression, dictionary, set], Optional(kw_in, any_identifier)
def import_statement(): return Optional("from", identifier), "import", identifier, Optional("as", identifier)
def return_statement(): return "return", [("(", [expression, list], ")"), expression, list]
def define_statement(): return "def", identifier, "(", identifier, ZeroOrMore(",", identifier), ")", ":"

# Commands
def command(): return [show_variables, draw_tree, delete_variable, exit, value]
def draw_tree(): return "drawTree"
def show_variables(): return "sv"
def delete_variable(): return "delete(", local_identifier, ")"
def exit(): return "exit"
def value(): return "value(", local_identifier, ")"

# Building blocks
def atom(): return [identifier, literal]
def literal(): return [number_literal, string_literal]
def number_literal(): return Optional(["+", "-"]), _(r'(\d)+\.?(\d)*')
def string_literal(): return [_(r'(["\'])(?:(?=(\\?))\2.)*?\1'), _(r"([''])(?:(?=(\\?))\2.)*?\1")]

# Identifier
def identifier(): return _(r'[a-zA-Z]\w*')
def local_identifier(): return [index_identifier, attribute_identifier, identifier]
def index_identifier(): return identifier, OneOrMore("[", [index, expression], "]"), Optional(".", [attribute_identifier, index_identifier, identifier])
def attribute_identifier(): return identifier, OneOrMore((".", [attribute_identifier, index_identifier, identifier]))
def any_identifier(): return [index_identifier, attribute_identifier, identifier]

# Function
def function(): return (identifier, "(",
                        Optional([assign_statement, list, expression],
                        ZeroOrMore((",", [assign_statement, list, expression]))),
                        ")")
def declare_function(): return define_statement, ZeroOrMore(statement), return_statement

# Expressions
def expression_atom(): return [function, list, set, any_identifier, literal]
def expression(): return [
                            ("(", expression, ")", ZeroOrMore(["+", "-", "/", "**", "*", "%"], expression)),
                            (expression_atom, ZeroOrMore(["+", "-", "/", "**", "*", "%"], expression))
                         ]
def local_expression_atom(): return [function, list, set, local_identifier, literal]
def local_expression(): return [
                            ("(", local_expression, ")", ZeroOrMore(["+", "-", "/", "**", "*", "%"], local_expression)),
                            (local_expression_atom, ZeroOrMore(["+", "-", "/", "**", "*", "%"], local_expression))
                         ]

# Data structures
def list(): return "[", [comprehension, array], "]"
def comprehension(): return local_expression, kw_for, local_expression, kw_in, expression, ZeroOrMore(comp_if)
def comp_if(): return kw_if, local_boolean_expression
def array(): return expression, ZeroOrMore(",", expression)
def dictionary(): return "{", atom, ":", expression, ZeroOrMore(",", atom, ":", expression), "}"
def set(): return "{", expression, ZeroOrMore(",", expression), "}"

# Boolean
def boolean(): return expression, ["==", "!="], expression
def boolean_expression(): return [
                                   (Optional(kw_not), "(", boolean_expression, ")", ZeroOrMore([kw_and, kw_or], Optional(kw_not), boolean_expression)),
                                   (boolean, ZeroOrMore([kw_and, kw_or], Optional(kw_not), boolean_expression))
                                 ]
def local_boolean(): return local_expression, ["==", "!="], local_expression
def local_boolean_expression(): return [
                                   (Optional(kw_not), "(", local_boolean_expression, ")", ZeroOrMore([kw_and, kw_or], Optional(kw_not), local_boolean_expression)),
                                   (local_boolean, ZeroOrMore([kw_and, kw_or], Optional(kw_not), local_boolean_expression))
                                 ]


# Misc.
def comment(): return _(r'\#.+')
def index(): return Optional(identifier), ":", Optional(identifier), ZeroOrMore(":", Optional(identifier))

# Keywords
def kw_for(): return _(r'for')
def kw_in(): return _(r'in')
def kw_else(): return _(r'else')
def kw_if(): return _(r'if')
def kw_or(): return _(r'or')
def kw_and(): return _(r'and')
def kw_not(): return _(r'not')
# as, import, return, def, from

def PrivateParser():
  return(ParserPython(user_entry, debug=False))

if __name__ == "__main__":
  parser = PrivateParser()
  parse_tree = parser.parse("a=b")

