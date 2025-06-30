import json

def loadData():
    with open('../../dados/dados.json', 'r', encoding='utf-8') as arquivo:
        dados = json.load

    return dados