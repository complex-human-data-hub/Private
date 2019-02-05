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
                                        draw_tree, \
                                        show_variables, \
                                        clear_variables, \
                                        show_dependencies, \
                                        show_code, \
                                        show_eval_code, \
                                        show_mccode, \
                                        show_sampler_status, \
                                        show_sampler_chains, \
                                        show_sampler_results, \
                                        show_pp_stats, \
                                        show_sets, \
                                        show_globals, \
                                        show_jobs, \
                                        variables_to_calculate, \
                                        variables_to_sample, \
                                        show_builtins, \
                                        show_prob_builtins, \
                                        show_ncpus, \
                                        help]
def comment():                  return identifier, comment_string
def delete():                   return "del", identifier
def comment_line():             return comment_string    # need this to stop interpreter from printing the comment_string
def draw_tree():                return "dt"
def show_variables():           return "sv"
def clear_variables():          return "clear"
def show_dependencies():        return "sd"
def show_code():                return "scode"
def show_eval_code():           return "sevalcode"
def show_mccode():              return "smccode"
def show_sampler_status():      return "sss"
def show_sampler_chains():      return "ssc"
def show_sampler_results():     return "ssr"
def show_pp_stats():            return "spp"
def show_sets():                return "ss"
def show_globals():             return "sg"
def show_jobs():                return "sj"
def variables_to_calculate():   return "vc"
def variables_to_sample():      return "vs"
def show_builtins():            return "sb"
def show_prob_builtins():       return "spb"
def show_ncpus():               return "sncpus"
def help():                     return "help"

def identifier():               return _(r'[a-zA-Z][a-zA-Z0-9]*')   # Note removed _ from identifier names to make sure that an attacker doesn't have access 
                                                                    # to reflection interface

def comment_string():           return _(r'#[a-zA-Z0-9_ ~=()\.,*#\[\]\///+-]*')
def module_name():              return _(r'[a-zA-Z_]+')
def notsym():                   return "not"
def starsym():                  return "*"
def colon():                    return ":"
def leftsquarebrack():          return "["
def rightsquarebrack():         return "]"

def dottedidentifier():         return identifier, ZeroOrMore(".", identifier)

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
def factor():                   return [function_call, method_call, indexed_variable, bracketed_expression, (notsym, factor), list, atom], Optional(leftsquarebrack, expression, colon, expression, rightsquarebrack)
def term():                     return factor, ZeroOrMore(["*","/", "or"], factor)
def simple_expression():        return Optional(["+", "-"]), term, ZeroOrMore(["+", "-", "and"], term)
def named_argument():           return identifier, "=", expression
def argument():                 return [named_argument, expression]
def function_call():            return identifier, "(", ZeroOrMore(argument, ","), argument, ")"
def method_call():              return dottedidentifier, "(", ZeroOrMore(expression, ","), expression, ")"
def indexed_variable():         return dottedidentifier, "[", ZeroOrMore(expression, ","), expression, "]"
def expression():               return simple_expression, Optional(relation, simple_expression)
def deterministic_assignment(): return identifier, "=", expression
def distribution_name():        return ["Normal", "HalfNormal", "Uniform", "SkewNormal", "Beta", "Kumaraswamy", "Exponential", "Laplace", "StudentT", "halfStudentT", "Cauchy", "HalfCauchy", "Gamma", "Weibull", "Lognormal", "ChiSquared", "Wald", "Pareto", "InverseGamma", "Exgaussian", "VonMises", "Triangular", "Gumbel", "Logistic", "LogitNormal", "Binomial", "ZeroInflatedBinomial", "Bernoulli", "Poisson", "ZeroInflatedPoisson", "NegativeBinomial", "ZeroInflatedNegativeBinomial", "DiscreteUniform", "Geometric", "Categorical", "DiscreteWeibull", "Constant", "OrderedLogistic"]
def distribution_parameter():   return [number, (identifier, Optional("[", identifier, "]"))]
def distribution_call():        return distribution_name, "(", ZeroOrMore(distribution_parameter, ","), distribution_parameter, ")"
def distribution_assignment():  return identifier, Optional("[", identifier, "]"), "~", distribution_call
def expression_assignment():    return identifier, "~", expression   # deterministic link within probabilistic model
def probabilistic_assignment(): return [distribution_assignment, expression_assignment]
def assignment():               return [deterministic_assignment, probabilistic_assignment], Optional(comment_string)
def command_line_expression():  return expression 
def line():                     return [command, assignment, command_line_expression, comment_line], EOF

def PrivateParser():
  return(ParserPython(line, debug = False, autokwd=True))

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
      parser = ParserPython(rule, debug=True, autokwd=True)
      parse_tree = parser.parse(input_line)
      print parse_tree
      print input_line, " is valid"
    except:
      print input_line, " is invalid"
