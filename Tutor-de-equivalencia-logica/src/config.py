"""
Arquivo de configuração global do sistema Tutor de Equivalências Lógicas.
Use para centralizar caminhos, constantes e parâmetros globais.
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUESTOES_PATH = os.path.join(BASE_DIR, 'questoes')
DADOS_PATH = os.path.join(BASE_DIR, 'dados')
PERFIS_PATH = os.path.join(DADOS_PATH, 'perfis')
LOGS_PATH = os.path.join(DADOS_PATH, 'logs')


NIVEIS = ['nivel1', 'nivel2', 'nivel3']

LIMITE_DICAS_LLM = 3  # Máximo de dicas LLM por questão
ARQUIVO_LOG = 'log.txt'
ARQUIVO_CONFIG_PERFIL = 'perfil.json'