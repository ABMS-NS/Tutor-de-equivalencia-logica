"""
Utilitários para o sistema de equivalências lógicas.
"""

from sympy import Equivalent, Implies, Xor, Not,And, Or,simplify_logic, Symbol
from sympy.logic.inference import satisfiable
import re

letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
local_dict = {letra: Symbol(letra) for letra in letras}
local_dict['V'] = True
local_dict['F'] = False
local_dict['True'] = True
local_dict['False'] = False
local_dict['Equivalent'] = Equivalent
local_dict['Xor'] = Xor
local_dict['Implies'] = Implies
local_dict['And'] = And
local_dict['Or'] = Or
local_dict['Not'] = Not


def substituir_simbolos(expr_str):
    """
    Troca símbolos lógicos por operadores do SymPy.
    """

    expr_str = re.sub(r'([a-zA-Z_]\w*)\s*↔\s*([a-zA-Z_]\w*)', r'Equivalent(\1, \2)', expr_str)
    expr_str = re.sub(r'([a-zA-Z_]\w*)\s*⇔\s*([a-zA-Z_]\w*)', r'Equivalent(\1, \2)', expr_str)
    expr_str = re.sub(r'([a-zA-Z_]\w*)\s*≡\s*([a-zA-Z_]\w*)', r'Equivalent(\1, \2)', expr_str)
    
   
    return (expr_str
            .replace('→', '>>')
            .replace('⇒', '>>')
            .replace('∧', '&')
            .replace('∨', '|')
            .replace('¬', '~')
            .replace('⊻', '^')
            )

def formatar_expressao(expr):
    if not hasattr(expr, 'func'):
        return str(expr)
    if isinstance(expr, Implies):
        args = [formatar_expressao(arg) for arg in expr.args]
        return f"({args[0]} → {args[1]})"
    if isinstance(expr, Equivalent):
        args = [formatar_expressao(arg) for arg in expr.args]
        return f"({args[0]} ↔ {args[1]})"
    if isinstance(expr, Xor):
        args = [formatar_expressao(arg) for arg in expr.args]
        return f"({args[0]} ⊻ {args[1]})"
    if isinstance(expr, Not):
        return f"¬{formatar_expressao(expr.args[0])}"
    if expr.func == And:
        args = [formatar_expressao(arg) for arg in expr.args]
        return "(" + " ∧ ".join(args) + ")"
    if expr.func == Or:
        args = [formatar_expressao(arg) for arg in expr.args]
        return "(" + " ∨ ".join(args) + ")"
    return str(expr)

def validar_nome_usuario(nome):
    """Checa se o nome do usuário é válido."""
    return isinstance(nome, str) and len(nome.strip()) > 2

def verificar_equivalencia(expr1, expr2):
    """
    Retorna True se expr1 e expr2 são equivalentes, senão retorna um contraexemplo.
    """
    equivalencia = Equivalent(expr1, expr2)
    simplificada = simplify_logic(equivalencia)
    if simplificada is True:
        return True, None
    else:
        contraexemplo = satisfiable(~equivalencia)
        return False, contraexemplo