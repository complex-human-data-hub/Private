from arpeggio import ParserPython, EOF, ZeroOrMore, Optional
from arpeggio import RegExMatch as _

# To do
# - Handle indents?
# - Handle probablistic dependencies (?)
# - Semantic analysis can't handle booleans
# - Can SA do functions? imports?
# - Can't pick up dependency between a and b where a = b[c]
# - Dependencies in list comprehensions?


def command():                  return [delete, comment, draw_generative_graph, draw_inferential_graph,
                                        draw_privacy_graph, draw_raw_graph, show_variables, show_variables_dict,
                                        show_values, clear_variables, show_dependencies, show_code, show_eval_code,
                                        show_mccode, show_sampler_results, show_pp_stats, show_globals, show_jobs,
                                        show_jobs_dict, show_builtins, show_prob_builtins, show_ncpus, show_stats,
                                        help]
def comment():                  return identifier, comment_string
def delete():                   return "del", identifier
def comment_line():             return comment_string    # need this to stop interpreter from printing the comment_string
def draw_generative_graph():    return "dgg"
def draw_inferential_graph():   return "dig"
def draw_privacy_graph():       return "dpg"
def draw_raw_graph():           return "drg"
def show_variables():           return "sv", Optional(identifier)
def show_variables_dict():      return "svdict", Optional(identifier)
def show_values():              return "sval"
def clear_variables():          return "clear"
def show_dependencies():        return "sd"
def show_code():                return "scode"
def show_eval_code():           return "sevalcode"
def show_mccode():              return "smccode"
def show_sampler_results():     return "ssr"
def show_pp_stats():            return "spp"
def show_globals():             return "sg"
def show_jobs():                return "sj"
def show_jobs_dict():           return "sjdict"
def show_builtins():            return "sb"
def show_prob_builtins():       return "spb"
def show_ncpus():               return "sncpus"
def show_stats():               return "showstats"
def help():                     return "help"
def identifier():               return _(r'[a-zA-Z][a-zA-Z0-9]*')   # Note removed _ from identifier names to make sure that an attacker doesn't have access to reflection interface
def comment_string():           return _(r'#[a-zA-Z0-9_ ~=()\.,*#\[\]\///+-]*')
def notsym():                   return "not"
def colon():                    return ":"
def leftsquarebrack():          return "["
def rightsquarebrack():         return "]"
def comma():                    return ","
def left_bracket():             return "("
def right_bracket():            return ")"
def keyword_define():           return "def"
def keyword_return():           return "return"
def dottedidentifier():         return identifier, ZeroOrMore(".", identifier)
def number():                   return _(r'[+-]?((\d+(\.\d*)?)|(\.\d+))')
def string():                   return [_(r'(["\'])(?:(?=(\\?))\2.)*?\1'), _(r"([''])(?:(?=(\\?))\2.)*?\1")]
def boolean():                  return ["True", "False"]
def relation():                 return ["==" , "!=" , "<=" , ">=" , "<" , ">" , "in"]
def atom():                     return [number, boolean, string, dottedidentifier]
def identifier_list():          return identifier, ZeroOrMore(",", identifier)
def list_comprehension():       return "[", expression, "for", identifier_list, "in", expression, Optional("if", expression), "]"
def enumerated_list():          return "[", ZeroOrMore(expression, ","), expression, "]"
def private_list():             return [list_comprehension, enumerated_list]
def bracketed_expression():     return "(", expression, ")"
def list_index():               return [(expression, Optional(colon, Optional(expression)), Optional(colon, Optional(expression))), (colon, Optional(expression), Optional(colon, Optional(expression)))]
def factor():                   return [function_call, method_call, indexed_variable, bracketed_expression, (notsym, factor), private_list, atom], ZeroOrMore(leftsquarebrack, list_index, ZeroOrMore(comma, list_index), rightsquarebrack)
def term():                     return factor, ZeroOrMore(["*", "//", "/", "%"], factor)
def simple_expression():        return Optional(["+", "-"]), term, ZeroOrMore(["+", "-"], term)
def comparison():               return simple_expression, ZeroOrMore(relation, simple_expression)
def boolean_expression():       return comparison, ZeroOrMore(["and","or"], comparison)
def named_argument():           return identifier, "=", expression
def argument():                 return [named_argument, expression]
def function_call():            return identifier, "(", [(ZeroOrMore(argument, ","), argument), ""], ")"
def method_call():              return dottedidentifier, "(", [(ZeroOrMore(expression, ","), expression), ""], ")"
def indexed_variable():         return dottedidentifier, leftsquarebrack, ZeroOrMore(expression, ","), expression, rightsquarebrack, ZeroOrMore([(".", [identifier, indexed_variable, dottedidentifier]), ("[", expression, "]")])
def expression():               return [boolean_expression, simple_expression]
def deterministic_assignment(): return identifier, "=", expression
def func_det_assignment():      return identifier, "=", expression
def distribution_name():        return ["Normal", "HalfNormal", "Uniform", "SkewNormal", "Beta", "Kumaraswamy", "Exponential", "Laplace", "StudentT", "halfStudentT", "Cauchy", "HalfCauchy", "Gamma", "Weibull", "Lognormal", "ChiSquared", "Wald", "Pareto", "InverseGamma", "Exgaussian", "VonMises", "Triangular", "Gumbel", "Logistic", "LogitNormal", "Binomial", "ZeroInflatedBinomial", "Bernoulli", "Poisson", "ZeroInflatedPoisson", "NegativeBinomial", "ZeroInflatedNegativeBinomial", "DiscreteUniform", "Geometric", "Categorical", "DiscreteWeibull", "Constant", "OrderedLogistic"]
def distribution_parameter():   return [number, (identifier, "[", identifier, "]"), argument]
def distribution_call():        return distribution_name, "(", ZeroOrMore(distribution_parameter, ","), distribution_parameter, ")"
def distribution_assignment():  return identifier, Optional("[", identifier, "]"), "~", distribution_call
def expression_assignment():    return identifier, "~", expression   # deterministic link within probabilistic model
def probabilistic_assignment(): return [distribution_assignment, expression_assignment]
def assignment():               return [deterministic_assignment, probabilistic_assignment], Optional(comment_string)
def command_line_expression():  return identifier
def line():                     return [command, assignment, command_line_expression, comment_line], EOF
def function_body_line():       return [func_det_assignment, comment_line], ";"
def function_header():          return keyword_define, identifier, left_bracket, [(argument, ZeroOrMore(comma, argument)), ""], right_bracket, colon
def function_return():          return keyword_return, expression, ";"
def function():                 return function_header,  ZeroOrMore(function_body_line), function_return, EOF
def code_block():               return [function, line]


def get_private_parser():
    return ParserPython(code_block, debug=False, autokwd=True)
