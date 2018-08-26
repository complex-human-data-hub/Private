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
def number_literal(): return Optional(["+", "-"]), _(r'(\d)+\.?(\d)*')
def string_literal(): return [_(r'(["\'])(?:(?=(\\?))\2.)*?\1'), _(r"([''])(?:(?=(\\?))\2.)*?\1")]

# Identifier
def identifier(): return _(r'[a-zA-Z]\w*')
def index_identifier(): return identifier, OneOrMore("[", [index, expression], "]"), Optional(".", any_identifier)
def attribute_identifier(): return identifier, OneOrMore((".", any_identifier))
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

class InputVisitor(PTNodeVisitor):

    def visit_user_entry(self, node, children):
        return "\n".join(children)

    def visit_statement(self, node, children):
        return " ".join(children)

    def visit_assign_statement(self, node, children):
        return " ".join(children)

    def visit_attribute_identifier(self, node, children):
        return node.value.replace(" | ", "")

    def visit_index_identifier(self, node, children):
        return node.value.replace(" | ", "")

    def visit_identifier(self, node, children):
        return node.value

    def visit_atom(self, node, children):
        return children[0]

    def visit_expression(self, node, children):
        return " ".join(children)

    def visit_expression_atom(self, node, children):
        return children[0]

    def visit_dictionary(self, node, children):
        return node.value.replace(" | ", "")

    def visit_comprehension(self, node, children):
        return node.value.replace(" | ", " ")

    def visit_list(self, node, children):
        return "[" + children[0] + "]"

    def visit_array(self, node, children):
        return ", ".join(children)

    def visit_set(self, node, children):
        return "{" + ", ".join(children) + "}"

    def visit_function(self, node, children):
        return children[0] + "(" + ", ".join(children[1:]) + ")"

    def visit_import_statement(self, node, children):
        return node.value.replace(" | ", " ")

result = visit_parse_tree(parse_tree, InputVisitor())
# Test
print(result)
