"""
Gerencia criação, login e carregamento do perfil do aluno.
"""

import json
import os
from datetime import datetime
from src.config import PERFIS_PATH, INITIAL_DATA_STRUCTURE

def criar_perfil(nome, respostas_questionario, caminho_arquivo):
    """Cria um novo perfil com nome e respostas do questionário inicial e salva no arquivo especificado."""
    
    dados = INITIAL_DATA_STRUCTURE.copy()
    
    # Dados básicos
    dados["nome"] = nome
    dados["questionario"] = respostas_questionario
    dados["data_criacao"] = datetime.now().isoformat()
    
    # Calcula o score do questionário
    score = sum(respostas_questionario)
    dados["score_questionario"] = score
    
    dados["niveis"] = {
        "1": {
            "liberado": True,  
            "concluido_com_sucesso": False,
            "dificuldade_media": 0.0,  
            "questoes_respondidas": [],
            "tentativas_anteriores": []
        },
        "2": {
            "liberado": (score > 1),  
            "concluido_com_sucesso": False,
            "dificuldade_media": 0.0,
            "questoes_respondidas": [],
            "tentativas_anteriores": []
        },
        "3": {
            "liberado": (score > 3),  
            "concluido_com_sucesso": False,
            "dificuldade_media": 0.0,
            "questoes_respondidas": [],
            "tentativas_anteriores": []
        }
    }
    
  
    dados["modulos_liberados"] = {
        "nivel_1": True,
        "nivel_2": (score > 1),
        "nivel_3": (score > 3)
    }
    
    return dados

def carregar_perfil(caminho_arquivo):
    """Carrega o perfil do usuário do arquivo especificado, ou retorna None se não existir."""
    if not os.path.exists(caminho_arquivo):
        return None
    
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)
            
        
            if not isinstance(dados, dict):
                return None
            if 'nome' not in dados or 'niveis' not in dados:
                return None
                
            return dados
    except (json.JSONDecodeError, FileNotFoundError, PermissionError):
        return None

def salvar_perfil(dados, caminho_arquivo):
    """Salva o perfil do usuário no arquivo especificado."""
    try:
        if not os.path.isabs(caminho_arquivo):
            caminho_arquivo = os.path.join(PERFIS_PATH, caminho_arquivo)
            
        os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
        
        dados["ultima_modificacao"] = datetime.now().isoformat()
        
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar perfil: {e}")
        raise

def verificar_requisitos_nivel(dados, nivel_desejado):
    """Verifica se o usuário atende os requisitos para acessar determinado nível."""
    nivel_str = str(nivel_desejado)
    return dados.get("niveis", {}).get(nivel_str, {}).get("liberado", False)

def atualizar_liberacao_nivel(dados, nivel_concluido):
    """Libera o próximo nível após conclusão bem-sucedida."""
    nivel_str = str(nivel_concluido)
    proximo_nivel = str(nivel_concluido + 1)
    
    
    if nivel_str in dados["niveis"]:
        dados["niveis"][nivel_str]["concluido_com_sucesso"] = True
    

    if proximo_nivel in dados["niveis"]:
        dados["niveis"][proximo_nivel]["liberado"] = True
        dados["modulos_liberados"][f"nivel_{proximo_nivel}"] = True
    
    return dados