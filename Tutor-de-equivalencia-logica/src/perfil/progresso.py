from src.perfil.perfil import carregar_perfil, salvar_perfil, atualizar_liberacao_nivel
from datetime import datetime
from src.config import DIFFICULTY_WEIGHTS, ADVANCEMENT_CRITERIA

def calcular_dificuldade_questao(tempo, tempo_limite, erros, dicas_fixas, dicas_llm):
    """
    Calcula um score de dificuldade para uma questão baseada na performance do aluno.
    Usa os pesos definidos em DIFFICULTY_WEIGHTS do config.py.
    """
    dificuldade = 0.0
    
    # Penalidade por exceder o tempo
    if tempo > tempo_limite:
        dificuldade += DIFFICULTY_WEIGHTS.get('tempo_excedido', 1.0) * (tempo / tempo_limite)

    # Penalidade por erros
    dificuldade += erros * DIFFICULTY_WEIGHTS.get('erro_final', 2.0)

    # Penalidade por uso de dicas fixas e LLM
    dificuldade += dicas_fixas * DIFFICULTY_WEIGHTS.get('dica_fixa_1', 0.5)
    dificuldade += dicas_llm * DIFFICULTY_WEIGHTS.get('dica_llm_1', 1.0)

    return max(0.0, dificuldade)

def verificar_criterios_avanco(dados, nivel):
    """
    Verifica se o aluno atende aos critérios de avanço para o próximo nível.
    """
    nivel_str = str(nivel)
    if nivel_str not in dados["niveis"]:
        return False
    
    questoes = dados["niveis"][nivel_str]["questoes_respondidas"]
    if not questoes:
        return False
    
   
    min_questoes = 5  
    taxa_acerto_minima = ADVANCEMENT_CRITERIA.get("min_grade", 7.0) / 10.0
    dificuldade_maxima = ADVANCEMENT_CRITERIA.get("max_difficulty", 2.0)  
    
    # Verifica número mínimo de questões
    if len(questoes) < min_questoes:
        return False
    
    # Verifica taxa de acerto
    acertos = sum(1 for q in questoes if q.get("acertou", False))
    taxa_atual = acertos / len(questoes)
    
    if taxa_atual < taxa_acerto_minima:
        return False
    
    # Verifica dificuldade média
    dificuldade_atual = dados["niveis"][nivel_str].get("dificuldade_media", 0)
    if dificuldade_atual > dificuldade_maxima:
        return False
    
    return True
def registrar_questao(nivel, questao_id, tempo, erros, dicas_fixas, dicas_llm, tempo_limite, acertou, resposta_aluno, perfil_path):
    """
    Registra o resultado de uma questão no perfil do aluno.
   
    """
    dados = carregar_perfil(perfil_path)
    nivel_str = str(nivel)

    dificuldade_questao = calcular_dificuldade_questao(tempo, tempo_limite, erros, dicas_fixas, dicas_llm)

    questao_info = {
        "id": questao_id,
        "tempo_gasto": tempo,
        "erros": erros,
        "dicas_fixas_usadas": dicas_fixas,
        "dicas_llm_usadas": dicas_llm,
        "acertou": acertou,
        "resposta_final": resposta_aluno,
        "dificuldade_calculada": dificuldade_questao,
        "data": datetime.now().isoformat()
    }

    if "questoes_respondidas" not in dados["niveis"][nivel_str]:
        dados["niveis"][nivel_str]["questoes_respondidas"] = []

    dados["niveis"][nivel_str]["questoes_respondidas"].append(questao_info)

    # Atualiza dificuldade média do nível
    questoes = dados["niveis"][nivel_str]["questoes_respondidas"]
    if questoes:
        dados["niveis"][nivel_str]["dificuldade_media"] = sum(q["dificuldade_calculada"] for q in questoes) / len(questoes)
    else:
        dados["niveis"][nivel_str]["dificuldade_media"] = 0

    if verificar_criterios_avanco(dados, nivel):
        dados = atualizar_liberacao_nivel(dados, nivel)
        print(f"🎉 Parabéns! Você desbloqueou o nível {nivel + 1}!")

    salvar_perfil(dados, perfil_path)
    return dados

def resetar_nivel(nivel, perfil_path):
    """
    Arquiva a tentativa atual de um nível e o prepara para uma nova tentativa.
    """
    dados = carregar_perfil(perfil_path)
    nivel_str = str(nivel)

    if nivel_str not in dados["niveis"]:
        return

    if "tentativas_anteriores" not in dados["niveis"][nivel_str]:
        dados["niveis"][nivel_str]["tentativas_anteriores"] = []

    if "questoes_respondidas" in dados["niveis"][nivel_str] and dados["niveis"][nivel_str]["questoes_respondidas"]:
        questoes_atuais = dados["niveis"][nivel_str]["questoes_respondidas"]
        
        acertos = sum(1 for q in questoes_atuais if q.get("acertou", False))
        total_questoes = len(questoes_atuais)
        dificuldade_media = dados["niveis"][nivel_str].get("dificuldade_media", 0)

        dados["niveis"][nivel_str]["tentativas_anteriores"].append({
            "data_conclusao": datetime.now().isoformat(),
            "acertos": acertos,
            "total_questoes": total_questoes,
            "dificuldade_media": dificuldade_media,
            "resumo_questoes": questoes_atuais
        })

    # Limpa o progresso atual para a nova tentativa
    dados["niveis"][nivel_str]["questoes_respondidas"] = []
    dados["niveis"][nivel_str]["dificuldade_media"] = 0
    
    salvar_perfil(dados, perfil_path)