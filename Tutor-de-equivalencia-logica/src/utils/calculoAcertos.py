from typing import List, Dict, Any, Tuple

#TESTAR ISSO AQUI, POIS FOI GERADO PELO GPT E EU ESTOU CONFIANDO

def calculoAcertos(lista_questoes: List[Dict[str, Any]]) -> Tuple[List[bool], int]:
    """
    Avalia uma lista de questões e retorna os resultados.

    Esta função percorre uma lista de dicionários, onde cada dicionário representa
    uma questão. Ela verifica o valor da chave 'acertou' para cada questão.

    Args:
        lista_questoes: Uma lista de dicionários, onde cada dicionário contém
                        os dados de uma questão, incluindo a chave 'acertou'.

    Returns:
        Uma tupla contendo dois valores:
        1. Uma lista de booleanos (True/False) correspondente ao resultado de cada questão.
        2. Um inteiro com a contagem total de questões corretas (acertos).
    """
    resultados_booleanos = [
        str(questao.get('acertou', '')).lower() == 'true' 
        for questao in lista_questoes
    ]

    total_acertos = sum(resultados_booleanos)

    return resultados_booleanos, total_acertos