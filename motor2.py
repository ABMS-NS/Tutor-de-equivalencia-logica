from sympy import symbols, Not, And, Or, Implies, Equivalent, simplify_logic
from sympy.logic.boolalg import BooleanFunction

# Criamos variáveis simbólicas comuns
A, B, C, D = symbols('A B C D')

# Lista de tuplas com nome da regra e função que aplica a transformação
REGRAS = [
    # Regra 1: p → q ≡ ¬p ∨ q
    ("Regra 1 (Imp → OU)", lambda e: e.replace(Implies, lambda p, q: Or(Not(p), q))),
    
    # Regra 2: ¬p ∨ q ≡ p → q
    ("Regra 2 (OU → Imp)", lambda e: e.replace(Or, lambda p, q: Implies(Not(p), q)) if isinstance(e, Or) and isinstance(e.args[0], Not) else e),
    
    # Regra 3: p → q ≡ ¬q → ¬p (Contraposição)
    ("Regra 3 (Contraposição)", lambda e: e.replace(Implies, lambda p, q: Implies(Not(q), Not(p)))),
    
    # Regra 5: ¬(p → q) ≡ p ∧ ¬q
    ("Regra 5 (Negação do Imp)", lambda e: Not(Implies(e.args[0], e.args[1])) if isinstance(e, Not) and isinstance(e.args[0], Implies) else e),
    
    # Regra 6: p ↔ q ≡ (p → q) ∧ (q → p)
    ("Regra 6 (Bicondicional → DUAS Implicações)", lambda e: e.replace(Equivalent, lambda p, q: And(Implies(p, q), Implies(q, p)))),
    
    # Regra 7: p ↔ q ≡ (p ∧ q) ∨ (¬p ∧ ¬q)
    ("Regra 7 (Bicondicional → conjunção de iguais)", lambda e: e.replace(Equivalent, lambda p, q: Or(And(p, q), And(Not(p), Not(q))))),
    
    # Regra 9: ¬¬p ≡ p
    ("Regra 9 (Dupla negação)", lambda e: e.replace(Not, lambda p: p if isinstance(p, Not) else Not(p))),
    
    # Regra 10: ¬(p ∧ q) ≡ ¬p ∨ ¬q
    ("Regra 10 (De Morgan ∧)", lambda e: e.replace(Not, lambda p: Or(Not(p.args[0]), Not(p.args[1])) if isinstance(p, And) else Not(p))),
    
    # Regra 11: ¬(p ∨ q) ≡ ¬p ∧ ¬q
    ("Regra 11 (De Morgan ∨)", lambda e: e.replace(Not, lambda p: And(Not(p.args[0]), Not(p.args[1])) if isinstance(p, Or) else Not(p))),
    
    # Regra 30: p ⊕ q ≡ (p ∨ q) ∧ ¬(p ∧ q)
    # Aqui fazemos substituição manual da função XOR
    ("Regra 30 (OU Exclusivo)", lambda e: e.replace(lambda expr: expr.func.__name__ == 'Xor',
                                                    lambda p, q: And(Or(p, q), Not(And(p, q)))))
]

def aplicar_regras(expr, max_passos=5):
    """
    Aplica um número limitado de regras passo a passo.
    Retorna uma lista com os passos aplicados: (nome_da_regra, antes, depois)
    """
    passos = []     # Lista de (nome, antes, depois)
    atual = expr    # Expressão que será transformada

    for i in range(max_passos):
        for nome, regra in REGRAS:
            # Aplica a regra
            novo = regra(atual)
            # Se houve mudança, salva o passo e reinicia com a nova expressão
            if novo != atual:
                passos.append((nome, atual, novo))
                atual = novo
                break
        else:
            # Nenhuma regra foi aplicada nesta rodada → encerrar
            break
    return passos

# --- MODO DE TESTE INTERATIVO ---

if __name__ == "__main__":
    from sympy.parsing.sympy_parser import parse_expr

    # Exemplo: Equivalent(A, B) ou Not(Implies(A, B))
    entrada = input("Digite a expressão lógica: ")

    try:
        # Interpreta string como expressão simbólica
        expr = parse_expr(entrada)

        # Mostra expressão original
        print(f"\nExpressão original: {expr}")

        # Aplica regras
        passos = aplicar_regras(expr)

        # Exibe resultado passo a passo
        if not passos:
            print("Nenhuma regra aplicada.")
        for i, (nome, antes, depois) in enumerate(passos):
            print(f"\nPasso {i+1}: {nome}")
            print(f"Antes: {antes}")
            print(f"Depois: {depois}")

    except Exception as e:
        print("Erro ao interpretar a expressão:", e)