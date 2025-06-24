"""
Utilitários para o sistema de equivalências lógicas.
"""

from .especialista.nos_logicos import Symbol, Equivalent, Xor, Implies, And, Or, Not, V, F
from sympy import symbols, simplify_logic, And as sAnd, Or as sOr, Not as sNot, Implies as sImplies, Equivalent as sEquivalent

def formatar_expressao(expr):
    if isinstance(expr, Symbol):
        return expr.nome
    if isinstance(expr, Implies):
        return f"({formatar_expressao(expr.a)} → {formatar_expressao(expr.b)})"
    if isinstance(expr, Equivalent):
        return f"({formatar_expressao(expr.a)} ↔ {formatar_expressao(expr.b)})"
    if isinstance(expr, Xor):
        return f"({formatar_expressao(expr.a)} ⊻ {formatar_expressao(expr.b)})" 
    if isinstance(expr, Not):
        return f"¬{formatar_expressao(expr.arg)}"
    if isinstance(expr, And):
        return "(" + " ∧ ".join(formatar_expressao(arg) for arg in expr.args) + ")"
    if isinstance(expr, Or):
        return "(" + " ∨ ".join(formatar_expressao(arg) for arg in expr.args) + ")"
    if isinstance(expr, V):
        return "V"
    if isinstance(expr, F):
        return "F"
    return str(expr)

def validar_nome_usuario(nome):
    """Checa se o nome do usuário é válido."""
    return isinstance(nome, str) and len(nome.strip()) > 2

def para_sympy(expr):
    if isinstance(expr, Symbol):
        return symbols(expr.nome)
    if isinstance(expr, Not):
        return sNot(para_sympy(expr.arg))
    if isinstance(expr, And):
        return sAnd(*[para_sympy(arg) for arg in expr.args])
    if isinstance(expr, Or):
        return sOr(*[para_sympy(arg) for arg in expr.args])
    if isinstance(expr, Implies):
        return sImplies(para_sympy(expr.a), para_sympy(expr.b))
    if isinstance(expr, Equivalent):
        return sEquivalent(para_sympy(expr.a), para_sympy(expr.b))
    if isinstance(expr, Xor):
        return para_sympy(expr.a) ^ para_sympy(expr.b)
    if isinstance(expr, V):
        return True
    if isinstance(expr, F):
        return False
    raise ValueError("Expressão desconhecida para conversão ao SymPy")

def para_cnf(expr):
    """
    Converter para Forma Normal Conjuntiva(FNC).
    """
    expr =  elimina_bicondicional(expr)
    expr = elimina_implicacao(expr)
    expr = distribui_not(expr)
    expr = distribui_or(expr)
    expr = simplifica(expr)
    return expr

def elimina_bicondicional(expr):
    """
    Elimina bicondicionais da expressão.
    """
    if isinstance(expr, Equivalent):
        return And(
            elimina_bicondicional(Implies(expr.a, expr.b)),
            elimina_bicondicional(Implies(expr.b, expr.a))
        )
    if isinstance(expr, (And, Or)):
        return expr.__class__(*map(elimina_bicondicional, expr.args))
    if isinstance(expr, Not):
        return Not(elimina_bicondicional(expr.arg))
    if isinstance(expr, Implies):
        return Implies(elimina_bicondicional(expr.a), elimina_bicondicional(expr.b))
    return expr

def elimina_implicacao(expr):
    """
    Elimina implicações da expressão.
    """
    if isinstance(expr, Implies):
        return Or(Not(elimina_implicacao(expr.a)), elimina_implicacao(expr.b))
    if isinstance(expr, (And, Or)):
        return expr.__class__(*map(elimina_implicacao, expr.args))
    if isinstance(expr, Not):
        return Not(elimina_implicacao(expr.arg))
    return expr

def distribui_not(expr):
    """
    Distribui negações na expressão.
    """
    if isinstance(expr, Not):
        arg = expr.arg
        if isinstance(arg, Not):
            return distribui_not(arg.arg)
        if isinstance(arg, And):
            return Or(*[Not(distribui_not(x)) for x in arg.args])
        if isinstance(arg, Or):
            return And(*[Not(distribui_not(x)) for x in arg.args])
        return Not(distribui_not(arg))
    if isinstance(expr, (And, Or)):
        return expr.__class__(*map(distribui_not, expr.args))
    return expr

def distribui_or(expr):
    """
    Distribui disjunções sobre conjunções (distribuição de OR sobre AND).
    """
    if isinstance(expr, Or):
        # Garante binaridade (Or(a, b))
        if len(expr.args) != 2:
            left = distribui_or(expr.args[0])
            right = distribui_or(Or(*expr.args[1:]))
            return distribui_or(Or(left, right))
        a, b = expr.args
        a = distribui_or(a)
        b = distribui_or(b)
        if isinstance(a, And):
            return And(*[distribui_or(Or(x, b)) for x in a.args])
        if isinstance(b, And):
            return And(*[distribui_or(Or(a, y)) for y in b.args])
        return Or(a, b)
    if isinstance(expr, And):
        return And(*[distribui_or(x) for x in expr.args])
    return expr

def simplifica(expr):
    """
    Remove duplicidades, aplica identidade, dominação, idempotência e contradição/tautologia.
    """
    if isinstance(expr, And) or isinstance(expr, Or):
        novos_args = []
        vistos = set()
        for arg in expr.args:
            arg_simp = simplifica(arg)
            # Identidade: p ∧ V = p, p ∨ F = p
            if isinstance(expr, And) and isinstance(arg_simp, V):
                continue
            if isinstance(expr, Or) and isinstance(arg_simp, F):
                continue
            # Dominação: p ∧ F = F, p ∨ V = V
            if isinstance(expr, And) and isinstance(arg_simp, F):
                return F()
            if isinstance(expr, Or) and isinstance(arg_simp, V):
                return V()
            # Idempotência: p ∧ p = p, p ∨ p = p
            if arg_simp not in vistos:
                novos_args.append(arg_simp)
                vistos.add(arg_simp)
        # Contradição/tautologia: p ∧ ¬p = F, p ∨ ¬p = V
        for arg in novos_args:
            if isinstance(arg, Not) and arg.arg in novos_args:
                if isinstance(expr, And):
                    return F()
                else:
                    return V()
        if not novos_args:
            return V()  
        if len(novos_args) == 1:
            return novos_args[0]
        return expr.__class__(*novos_args)
    if isinstance(expr, Not):
        arg_simp = simplifica(expr.arg)
        # Dupla negação
        if isinstance(arg_simp, Not):
            return simplifica(arg_simp.arg)
        return Not(arg_simp)
    return expr

def achatados_args(expr):
    if isinstance(expr, And) or isinstance(expr, Or):
        args = []
        for arg in expr.args:
            if isinstance(arg, expr.__class__):
                args.extend(achatados_args(arg))
            else:
                args.append(arg)
        return args
    return [expr]

def iguais_comutativos(expr1, expr2):
    if type(expr1) != type(expr2):
        return False
    if isinstance(expr1, And) or isinstance(expr1, Or):
        # Compara conjuntos de todos os argumentos achatados (comutatividade + associatividade)
        return set(achatados_args(expr1)) == set(achatados_args(expr2))
    if isinstance(expr1, Not):
        return iguais_comutativos(expr1.arg, expr2.arg)
    if isinstance(expr1, Implies):
        return iguais_comutativos(expr1.a, expr2.a) and iguais_comutativos(expr1.b, expr2.b)
    if isinstance(expr1, Equivalent):
        return ({expr1.a, expr1.b} == {expr2.a, expr2.b})
    if isinstance(expr1, Xor):
        return ({expr1.a, expr1.b} == {expr2.a, expr2.b})
    if isinstance(expr1, Symbol):
        return expr1.nome == expr2.nome
    if isinstance(expr1, V) or isinstance(expr1, F):
        return type(expr1) == type(expr2)
    return expr1 == expr2

def verificar_equivalencia(expr1, expr2):
    """
    Retorna True se expr1 e expr2 são equivalentes (por FNC ou SymPy), senão retorna None.
    """
    cnf1 = para_cnf(expr1)
    cnf2 = para_cnf(expr2)
    if iguais_comutativos(cnf1, cnf2):
        return True, None
    else:
        # Só executa SymPy se FNC falhar
        s1 = para_sympy(expr1)
        s2 = para_sympy(expr2)
        return simplify_logic(s1 ^ s2) == False, None