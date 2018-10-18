import numpy as np
import pp

from arpeggio import *
from arpeggio import RegExMatch as _
from networkx.drawing.nx_pydot import write_dot
from testpp import *


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
def command(): return [draw_tree, delete_variable, exit, value]
def draw_tree(): return "drawTree"
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
        #draw_dependency_graph(dependencies.graph)
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

commands = ["drawTree", "delete_variable"]
input_lines = []
input_line = ''
parser = ParserPython(user_entry, debug = False)
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
        result = visit_parse_tree(parse_tree, InputVisitor())[0]

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
