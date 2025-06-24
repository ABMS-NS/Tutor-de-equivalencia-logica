from sympy.parsing.sympy_parser import parse_expr
from sympy.logic.boolalg import to_cnf
from sympy import symbols
from src.utils import verificar_equivalencia, substituir_simbolos, formatar_expressao,local_dict

def analisar_equivalencia(expr1_str, expr2_str):
    print("\n--- Etapa 1: Interpretando expressões ---")
    try:
        expr1_str = substituir_simbolos(expr1_str)
        expr2_str = substituir_simbolos(expr2_str)
        expr1 = parse_expr(expr1_str, local_dict= local_dict)
        expr2 = parse_expr(expr2_str, local_dict= local_dict)
        print(f"Expressão 1: {formatar_expressao(expr1)}")
        print(f"Expressão 2: {formatar_expressao(expr2)}")
    except Exception as e:
        print("Erro ao interpretar as fórmulas:", e)
        return

    print("\n--- Etapa 2: Forma Normal Conjuntiva (FNC) ---")
    cnf1 = to_cnf(expr1, simplify=True)
    cnf2 = to_cnf(expr2, simplify=True)
    print(f"FNC da Expressão 1: {formatar_expressao(cnf1)}")
    print(f"FNC da Expressão 2: {formatar_expressao(cnf2)}")

    print("\n--- Etapa 3: Verificando equivalência lógica ---")
    equivalente, contraexemplo = verificar_equivalencia(expr1, expr2)
    if equivalente:
        print("✔️ As expressões são logicamente equivalentes.")
    else:
        print("❌ As expressões NÃO são logicamente equivalentes.")
        print("\n--- Etapa 4: Mostrando diferença (se houver) ---")
        if contraexemplo is False:
            print("Não há modelo onde as expressões sejam diferentes.")
        else:
            print("Há pelo menos um modelo onde elas diferem:")
            for k, v in contraexemplo.items():
                print(f"{k} = {v}")

# Exemplo de uso:
if __name__ == "__main__":
    print("Exemplo de entrada: (A >> B) & A e B ou (A → B)  A e B")
    entrada1 = input("Digite a primeira expressão: ")
    entrada2 = input("Digite a segunda expressão: ")
    analisar_equivalencia(entrada1, entrada2)