import json
import os
from .resolvedor import Resolvedor

def avaliar_traducao(aluno_s1, aluno_s2, gabarito_s1, gabarito_s2):
    """
    Avalia se as traduções simbólicas do aluno para S1 e S2 são logicamente equivalentes.
    """
    resolvedor = Resolvedor()
    equivalente, caminho = resolvedor.buscar_equivalencia(aluno_s1, aluno_s2)
    gabarito_equivalente, _ = resolvedor.buscar_equivalencia(gabarito_s1, gabarito_s2)
    return equivalente, caminho, gabarito_equivalente

if __name__ == "__main__":
    # Caminho relativo ao arquivo atual
    caminho_json = os.path.join(os.path.dirname(__file__), '..', '..', 'questoes', 'nivel3.json')
    caminho_json = os.path.abspath(caminho_json)

    with open(caminho_json, encoding='utf-8') as f:
        questoes = json.load(f)
    questao = questoes[0]

    gabarito_s1 = questao["gabarito_traducao_s1"]
    gabarito_s2 = questao["gabarito_traducao_s2"]

    print(questao["enunciado"])
    print("\nLegenda das proposições:")
    for letra, significado in questao["legenda"].items():
        print(f"{letra}: {significado}")

    print("\nDigite sua tradução simbólica para cada sentença:")
    aluno_s1 = input("S1: ")
    aluno_s2 = input("S2: ")

    equivalente, caminho, gabarito_equivalente = avaliar_traducao(aluno_s1, aluno_s2, gabarito_s1, gabarito_s2)

    if equivalente:
        print("\nParabéns! Suas traduções são logicamente equivalentes.")
        print("Passo a passo encontrado:")
        for passo in caminho:
            print(passo)
    else:
        print("\nAs traduções não são equivalentes. Reveja sua resposta.")

    print("\nExemplo de caminho do gabarito:")
    for passo in questao["exemplo_caminho"]:
        print(passo)