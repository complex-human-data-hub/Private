from arpeggio import *
from arpeggio import RegExMatch as _

# Entry
def user_entry(): return ZeroOrMore([
                                      (statement, Optional(comment)),
                                      (declare_function, Optional(comment)),
                                      comment,
                                    ]), EOF

# Statement
def statement(): return [
                          assign_statement,
                          import_statement,
                        ]
def assign_statement(): return any_identifier, ["=", "~"], [function, list, expression, dictionary, set], Optional("in", any_identifier)
def import_statement(): return Optional("from", identifier), "import", identifier, Optional("as", identifier)
def return_statement(): return "return", [("(", [expression, list], ")"), expression, list]
def define_statement(): return "def", identifier, "(", identifier, ZeroOrMore(",", identifier), ")", ":"

# Building blocks
def atom(): return [identifier, literal]
def literal(): return [number_literal, string_literal]
def number_literal(): return Optional(["+", "-"]), _(r'(\d)+\.?(\d)+')
def string_literal(): return [_(r'(["\'])(?:(?=(\\?))\2.)*?\1'), _(r"([''])(?:(?=(\\?))\2.)*?\1")]

# Identifier
def identifier(): return _(r'(\w)+')
def index_identifier(): return identifier, OneOrMore("[", [index, expression], "]")
def attribute_identifier(): return identifier, OneOrMore((".", identifier))
def any_identifier(): return [index_identifier, attribute_identifier, identifier]

# Function
def function(): return (identifier, "(",
                        Optional([assign_statement, list, expression],
                        ZeroOrMore((",", [assign_statement, list, expression]))),
                        ")")
def declare_function(): return define_statement, ZeroOrMore(statement), return_statement

# Expressions
def expression_atom(): return [index_identifier, attribute_identifier, function, list, set, atom]
def expression(): return [
                            ("(", expression, ")", ZeroOrMore(["+", "-", "/", "**", "*"], expression)),
                            (expression_atom, ZeroOrMore(["+", "-", "/", "**", "*"], expression))
                         ]

# Data structures
def list(): return "[", [comprehension, array], "]"
def comprehension(): return expression, comp_for
def comp_for(): return Optional("for", expression), "in", expression, ZeroOrMore([comp_for, comp_if])
def comp_if(): return "if", boolean_expression
def array(): return expression, ZeroOrMore(",", expression)
def dictionary(): return "{", atom, ":", expression, ZeroOrMore(",", atom, ":", expression), "}"
def set(): return "{", expression, ZeroOrMore(",", expression), "}"

# Boolean
def boolean(): return expression, ["==", "!="], expression
def boolean_expression(): return [
                                   (Optional("not"), "(", boolean_expression, ")", ZeroOrMore(["and", "or"], Optional("not"), boolean_expression)),
                                   (boolean, ZeroOrMore(["and", "or"], Optional("not"), boolean_expression))
                                 ]

# Misc.
def comment(): return _(r'\#.+')
def index(): return Optional(identifier), ":", Optional(identifier), ZeroOrMore(":", Optional(identifier))

with open('test_input.txt', 'r') as f:
    test = f.read()

#test = "EventsToAnalyse = [event(latitude = e.latitude, happy = e.day in HappyDays) for e in AppEvents]"

# Parse
parser = ParserPython(user_entry, debug = True)
parse_tree = parser.parse(test)

# Test
print(parse_tree)
