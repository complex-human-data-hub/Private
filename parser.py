from arpeggio import *
from arpeggio import RegExMatch as _

def user_entry(): return ZeroOrMore(statement), EOF
def statement(): return identifier, ["=", "~"], [function, list, expression]
def atom(): return [identifier, literal]
def literal(): return [number_literal, string_literal]
def number_literal(): return Optional(["+", "-"]), _(r'(\d)+\.?(\d)+')
def string_literal(): return [_(r'\".+\"'), _(r'\'.+\'')]
def identifier(): return _(r'(\w)+')
def identifier_index(): return identifier, OneOrMore("[", expression, "]")
def identifier_attribute(): return identifier, OneOrMore((".", identifier))
def function(): return identifier, "(", Optional([list, expression], ZeroOrMore((",", [list, expression]))), ")"
def list(): return "[", comprehension, "]"
def expression(): return [
                           identifier_index, # eg. mu[subjects]
                           identifier_attribute, # eg. latitude.hier.mu
                           atom # eg. "IFTTTButton"
                         ]
def comprehension(): return expression, comp_for
def comp_for(): return "for", expression, "in", expression, ZeroOrMore([comp_for, comp_if])
def comp_if(): return "if", boolean_expression
def boolean(): return expression, ["==", "!="], expression
def boolean_expression(): return [
                                   (Optional("!"), "(", boolean_expression, ")", ZeroOrMore(["and", "or"], boolean_expression)),
                                   (boolean, ZeroOrMore(["and", "or"], boolean_expression))
                                 ]

test = "HappyDays = unique([e.day for e in events if e.type == 'IFTTTButton'])"

# Parse
parser = ParserPython(user_entry)
parse_tree = parser.parse(test)

# Test
print(parse_tree)
