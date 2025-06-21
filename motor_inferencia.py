from sympy import symbols, simplify_logic, Equivalent
from sympy.logic.boolalg import to_cnf
from sympy.logic.inference import satisfiable
from sympy.parsing.sympy_parser import parse_expr
from sympy.abc import _clash1

def analisar_equivalencia(expr1_str, expr2_str):
    print("\n--- Etapa 1: Interpretando expressões ---")
    try:
        expr1 = parse_expr(expr1_str, local_dict=_clash1)
        expr2 = parse_expr(expr2_str, local_dict=_clash1)
        print(f"Expressão 1: {expr1}")
        print(f"Expressão 2: {expr2}")
    except Exception as e:
        print("Erro ao interpretar as fórmulas:", e)
        return

    print("\n--- Etapa 2: Forma Normal Conjuntiva (FNC) ---")
    cnf1 = to_cnf(expr1, simplify=True)
    cnf2 = to_cnf(expr2, simplify=True)
    print(f"FNC da Expressão 1: {cnf1}")
    print(f"FNC da Expressão 2: {cnf2}")

    print("\n--- Etapa 3: Verificando equivalência lógica ---")
    equivalencia = Equivalent(expr1, expr2)
    simplificada = simplify_logic(equivalencia)

    if simplificada == True:
        print("✔️ As expressões são logicamente equivalentes.")
    else:
        print("❌ As expressões NÃO são logicamente equivalentes.")

    print("\n--- Etapa 4: Mostrando diferença (se houver) ---")
    inequivalente = satisfiable(~equivalencia)
    if inequivalente is False:
        print("Não há modelo onde as expressões sejam diferentes.")
    else:
        print("Há pelo menos um modelo onde elas diferem:")
        for k, v in inequivalente.items():
            print(f"{k} = {v}")

# Exemplo de uso:
if __name__ == "__main__":
    print("Exemplo de entrada: (A >> B) & A    e     B")
    entrada1 = input("Digite a primeira expressão: ")
    entrada2 = input("Digite a segunda expressão: ")
    analisar_equivalencia(entrada1, entrada2)