"""
Módulo para controlar a liberação de níveis e processar a conclusão de tentativas.
Agora todas as funções aceitam perfil_path para múltiplos perfis.
"""
from src.config import NIVEIS_CONFIG
from src.perfil.perfil import salvar_perfil, carregar_perfil
from datetime import datetime

def verificar_status_nivel(dados_perfil, nivel_id):
    """
    Verifica o status de um nível (Bloqueado, Disponível, Concluído) com base em modulos_liberados do perfil.

    Args:
        dados_perfil (dict): O dicionário com os dados do perfil do aluno.
        nivel_id (int): O ID do nível a ser verificado.

    Returns:
        tuple: (str: Status, str: Mensagem de informação)
    """
    nivel_str = str(nivel_id)
    nivel_key = f"nivel_{nivel_id}"
    # Se já foi concluído
    if dados_perfil["niveis"].get(nivel_str, {}).get("concluido_com_sucesso", False):
        acertos = dados_perfil["niveis"][nivel_str].get("acertos_ultima_tentativa", 0)
        total = dados_perfil["niveis"][nivel_str].get("total_questoes_ultima_tentativa", 1)
        percentual = (acertos / total) * 100 if total > 0 else 0
        return "Concluído", f"{percentual:.0f}% de acerto na última tentativa."
    # Liberação baseada no perfil
    if not dados_perfil.get("modulos_liberados", {}).get(nivel_key, False):
        return "Bloqueado", "Este nível ainda não está liberado pelo seu perfil inicial."
    return "Disponível", "Pronto para ser iniciado!"


def processar_conclusao_de_nivel(nivel_id, perfil_path):
    """
    Arquiva a tentativa atual, avalia o desempenho e marca o nível como concluído
    se os critérios forem atendidos. Agora recebe perfil_path.

    Args:
        nivel_id (int): O ID do nível que foi finalizado.
        perfil_path (str): O caminho do perfil a ser carregado/salvo.

    Returns:
        dict: A tentativa que foi processada e arquivada, ou None se não havia nada a processar.
    """
    dados = carregar_perfil(perfil_path)
    nivel_str = str(nivel_id)

    if "questoes_respondidas" not in dados["niveis"][nivel_str] or not dados["niveis"][nivel_str]["questoes_respondidas"]:
        return None # Não há nada para processar

    # Pega os dados da tentativa atual
    questoes_atuais = dados["niveis"][nivel_str]["questoes_respondidas"]
    acertos = sum(1 for q in questoes_atuais if q.get("acertou", False))
    total_questoes = len(questoes_atuais)
    dificuldade_media = dados["niveis"][nivel_str].get("dificuldade_media", 0)

    # Arquiva a tentativa
    tentativa_arquivada = {
        "data_conclusao": datetime.now().isoformat(),
        "acertos": acertos,
        "total_questoes": total_questoes,
        "dificuldade_media": dificuldade_media,
        "resumo_questoes": questoes_atuais
    }
    if "tentativas_anteriores" not in dados["niveis"][nivel_str]:
        dados["niveis"][nivel_str]["tentativas_anteriores"] = []
    dados["niveis"][nivel_str]["tentativas_anteriores"].append(tentativa_arquivada)

    # Salva as métricas desta tentativa para exibição na tela de seleção de nível
    dados["niveis"][nivel_str]["acertos_ultima_tentativa"] = acertos
    dados["niveis"][nivel_str]["total_questoes_ultima_tentativa"] = total_questoes
    dados["niveis"][nivel_str]["dificuldade_media_ultima_tentativa"] = dificuldade_media

    # === LÓGICA DE LIBERAÇÃO ===
    percentual_acerto = (acertos / total_questoes) * 100 if total_questoes > 0 else 0
    criterio_acerto = percentual_acerto >= NIVEIS_CONFIG[nivel_str].get("min_acerto_para_liberar", 70)
    criterio_dificuldade = dificuldade_media < NIVEIS_CONFIG[nivel_str].get("max_dificuldade_para_liberar", 2.0)

    # Marca como concluído com sucesso apenas se ambos os critérios forem atendidos
    if criterio_acerto and criterio_dificuldade:
        dados["niveis"][nivel_str]["concluido_com_sucesso"] = True
    else:
        # Se não atingiu, garante que o status não fique como sucesso
        dados["niveis"][nivel_str]["concluido_com_sucesso"] = False

    # Limpa o progresso da tentativa atual, pois ela já foi arquivada
    dados["niveis"][nivel_str]["questoes_respondidas"] = []
    dados["niveis"][nivel_str]["dificuldade_media"] = 0

    salvar_perfil(dados, perfil_path)
    return tentativa_arquivada
