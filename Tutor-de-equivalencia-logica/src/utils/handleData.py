from loadData import loadData
from calculoAcertos import calculoAcertos

nome, questoesNivelUm, questoesNivelDois, questoesNivelTres = loadData()

acertosNivelUm, quantidadeAcertosNivelUm = calculoAcertos(questoesNivelUm)

acertosNivelDois, quantidadeAcertosNivelDois = calculoAcertos(questoesNivelDois)

acertosNivelTres, quantidadeAcertosNivelTres = calculoAcertos(questoesNivelTres)