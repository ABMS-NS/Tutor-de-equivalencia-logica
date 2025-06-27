from lark import Lark, Transformer
from .nos_logicos import Symbol, Not, And, Or, Implies, Equivalent, Xor, V, F

grammar = r"""
    ?start: expr
    ?expr: equiv
    ?equiv: implies
          | equiv "↔" implies   -> equiv
          | equiv "<->" implies -> equiv
    ?implies: xor
          | xor "→" implies   -> implies
          | xor "->" implies  -> implies
    ?xor: or_
        | xor "⊻" or_   -> xor
        | xor "^" or_   -> xor
    ?or_: and_
         | or_list

    or_list: and_ (("∨" and_) | ("|" and_))+   -> or_list

    ?and_: not_
         | and_list

    and_list: not_ (("∧" not_) | ("&" not_))+  -> and_list

    ?not_: atom
         | "¬" not_      -> not_
         | "~" not_      -> not_
    ?atom: "(" expr ")"
         | SYMBOL
         | "V"           -> v_true
         | "F"           -> f_false

    SYMBOL: /[a-zA-Z][a-zA-Z0-9_]*/
    %ignore " "
"""

class ASTTransformer(Transformer):
    def SYMBOL(self, token):
        return Symbol(str(token))
    def not_(self, args):
        return Not(args[0])
    def and_(self, args):
        return And(*args)
    def and_list(self, args):
        return And(*args)
    def or_(self, args):
        return Or(*args)
    def or_list(self, args):
        return Or(*args)
    def implies(self, args):
        return Implies(args[0], args[1])
    def equiv(self, args):
        return Equivalent(args[0], args[1])
    def xor(self, args):
        return Xor(args[0], args[1])
    def v_true(self, *args):
        return V()
    def f_false(self, *args):
        return F()
parser = Lark(grammar, parser="lalr", transformer=ASTTransformer())

def parser_expr(expr_str):
    return parser.parse(expr_str)