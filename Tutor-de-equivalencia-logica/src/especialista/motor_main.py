"""
Arquivo principal que executa o sistema, lida com a entrada do usuário
e apresenta os resultados da análise de equivalência.
"""
from src.especialista.resolvedor import Resolvedor
from src.utils import verificar_equivalencia, formatar_expressao, substituir_simbolos, local_dict
from sympy.parsing.sympy_parser import parse_expr

def processar_entrada_usuario(texto):
    """
    Processa a entrada do usuário, substitui símbolos e converte para expressão SymPy.
    """
    texto = substituir_simbolos(texto)
    try:
        expr = parse_expr(texto, local_dict=local_dict)
        return expr, None
    except Exception as e:
        return None, f"Erro ao processar a expressão: {e}"

def formatar_passo(expr, regra=None, inicial=False):
    if inicial:
        return f"{formatar_expressao(expr):40} (Expressão inicial)"
    if regra:
        return f"{formatar_expressao(expr):40} ({regra})"
    return f"{formatar_expressao(expr):40}"

if __name__ == "__main__":
    resolvedor = Resolvedor()

    print("=" * 80)
    print("                    RESOLVEDOR DE EQUIVALÊNCIAS LÓGICAS")
    print("=" * 80)

    # Entrada do usuário
    while True:
        entrada1 = input("Expressão inicial: ").strip()
        expr1, erro = processar_entrada_usuario(entrada1)
        if not erro: break
        print(f"Erro: {erro}. Tente novamente.")

    while True:
        entrada2 = input("Expressão objetivo: ").strip()
        expr2, erro = processar_entrada_usuario(entrada2)
        if not erro: break
        print(f"Erro: {erro}. Tente novamente.")

    print("-" * 80)
    print(f"Expressão inicial:  {formatar_expressao(expr1)}")
    print(f"Expressão objetivo: {formatar_expressao(expr2)}")
    print("-" * 80)

    # Verifica se são idênticas antes de buscar transformação
    if expr1 == expr2:
        print("\nAs duas expressões são idênticas!")
        print("Nenhuma transformação necessária.")
        print("-" * 80)
    else:
        # Busca a transformação
        sucesso, caminho = resolvedor.buscar_equivalencia(expr1, expr2)

        if sucesso:
            print("\nAs duas expressões são equivalentes!\n")
            print("Passo a passo da resolução:")
            print("-" * 80)
            for i, (passo_expr, passo_regra) in enumerate(caminho):
                if i == 0:
                    print(formatar_passo(passo_expr, inicial=True))
                else:
                    print(formatar_passo(passo_expr, passo_regra))
            print("-" * 80)
        else:
            print("\nFALHA. Não foi possível transformar a expressão inicial na objetivo com as regras atuais.")
            equivalente, contraexemplo = verificar_equivalencia(expr1, expr2)
            if equivalente:
                print("\nAs duas expressões são equivalentes (confirmado por simplificação lógica),")
                print("mas o resolvedor não encontrou um caminho de transformação.")
            else:
                print("\nCONFIRMADO: As expressões NÃO são logicamente equivalentes.")
                if contraexemplo:
                    print(f"Um contraexemplo é: {contraexemplo}")