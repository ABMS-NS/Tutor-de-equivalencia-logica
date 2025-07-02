import json

def loadData():
    with open('../../dados/dados.json', 'r', encoding='utf-8') as arquivo:
        dados = json.load

    with open('../../questoes/nivel1.json', 'r', encoding='utf-8') as nivelUm:
        questoesNivelUm = nivelUm.load

    with open('../../questoes/nivel2.json', 'r', encoding='utf-8') as nivelDois:
        questoesNivelDois = nivelDois.load

    with open('../../questoes/nivel3.json', 'r', encoding='utf-8') as nivelTres:
        questoesNivelTres = nivelTres.load
    
    return dados, questoesNivelUm, questoesNivelDois, questoesNivelTres