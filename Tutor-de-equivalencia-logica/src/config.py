"""
Arquivo de configuração global do sistema Tutor de Equivalências Lógicas.
Use para centralizar caminhos, constantes e parâmetros globais.
"""
import os
import customtkinter as ctk

# --- PATHS ---
# Define caminhos absolutos para garantir que o programa encontre os arquivos
# independentemente de onde for executado.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUESTOES_PATH = os.path.join(BASE_DIR, 'questoes')
DADOS_PATH = os.path.join(BASE_DIR, 'dados')
PERFIS_PATH = os.path.join(DADOS_PATH, 'perfis')
LOGS_PATH = os.path.join(DADOS_PATH, 'logs')

# -- Configurações Gerais---
NIVEIS = ['1', '2', '3']
ARQUIVO_LOG = 'log.txt'
ARQUIVO_CONFIG_PERFIL = 'perfil.json'

# Configurações específicas para cada nível
NIVEIS_CONFIG = {
    "1": {
        "tempo_limite_por_questao": 300,  # 5 minutos
        "min_acerto_para_liberar": 70,
        "max_dificuldade_para_liberar": 2.0,
        "total_questoes": 10
    },
    "2": {
        "tempo_limite_por_questao": 240,  # 4 minutos
        "min_acerto_para_liberar": 70,
        "max_dificuldade_para_liberar": 2.0,
        "total_questoes": 10
    },
    "3": {
        "tempo_limite_por_questao": 180,  # 3 minutos
        "min_acerto_para_liberar": 70,
        "max_dificuldade_para_liberar": 2.0,
        "total_questoes": 10
    }
}

# --- UI Tema da Interface---
APPEARANCE_MODE = "dark"
COLOR_THEME = "blue"

# --- UI Dimensões das Telas ---
MAIN_WINDOW = {"width":800,"height": 700}
LEVELS_WINDOW = {"width": 500, "height": 400}
EXERCISE_WINDOW = {"width": 800, "height": 700}
REQUIREMENTS_WINDOW = {"width": 350, "height": 200}

# --- Perfil do Aluno Estrutura Inicial ---
INITIAL_DATA_STRUCTURE = {
    "nome": "",
    "usa_llm": True,
    "nivel_atual": 1,
    "modulos_liberados": {
        "nivel_1": True,
        "nivel_2": False,
        "nivel_3": False
    },
    "respostas": {
        "nivel_1": [],
        "nivel_2": [],
        "nivel_3": []
    },
    "notas": {
        "nivel_1": None,
        "nivel_2": None,
        "nivel_3": None
    },
    "dificuldade_media": {
        "nivel_1": None,
        "nivel_2": None,
        "nivel_3": None
    },
    "tentativas_por_nivel": {
        "nivel_1": 0,
        "nivel_2": 0,
        "nivel_3": 0
    }
}

# Métricas de Dificuldade
DIFFICULTY_WEIGHTS = {
    "dica_fixa_1": 0.5,
    "dica_fixa_2": 1.0,
    "dica_llm_1": 1.0,
    "dica_llm_2": 2.0,
    "dica_llm_3": 3.0,
    "tempo_excedido": 1.0,
    "erro_final": 2.0
}

# Critérios de Avanço
ADVANCEMENT_CRITERIA = {
    "min_grade": 7.0,
    "max_difficulty": 2.0
}

# --- Funções de Configuracao de Tema ---
def setup_theme():
    """Configura o tema padrão da aplicação"""
    ctk.set_appearance_mode(APPEARANCE_MODE)
    ctk.set_default_color_theme(COLOR_THEME)