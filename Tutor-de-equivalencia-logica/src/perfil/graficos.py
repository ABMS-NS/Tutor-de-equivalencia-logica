"""
Gera gráficos de desempenho do aluno com análises pedagógicas.
"""
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from src.perfil.perfil import carregar_perfil
import customtkinter as ctk
from tkinter import Text, Scrollbar, RIGHT, Y, END
import tkinter as tk

def grafico_progresso_nivel(nivel, perfil_path):
    """
    Gera um gráfico de barras mostrando o desempenho do aluno em todas as tentativas de um nível.
    """
    dados = carregar_perfil(perfil_path)
    nivel_str = str(nivel)
    tentativas = dados["niveis"].get(nivel_str, {}).get("tentativas_anteriores", [])
    
    if not tentativas:
        return

    tentativas_labels = [f"Tentativa {i+1}" for i in range(len(tentativas))]
    acertos = [t["acertos"] for t in tentativas]
    total = [t["total_questoes"] for t in tentativas]
    dificuldade = [t["dificuldade_media"] for t in tentativas]
    percentuais = [(a/t)*100 if t > 0 else 0 for a, t in zip(acertos, total)]

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Barras de percentual de acerto
    bars = ax1.bar(tentativas_labels, percentuais, color='lightblue', edgecolor='navy', alpha=0.7)
    ax1.axhline(y=70, color='green', linestyle='--', alpha=0.8, label='Meta: 70%')
    ax1.set_ylabel('Taxa de Acerto (%)')
    ax1.set_ylim(0, 105)
    ax1.set_xlabel('Tentativas')
    ax1.legend(loc='upper left')
    
    # Adicionar valores nas barras
    for bar, perc in zip(bars, percentuais):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                f'{perc:.0f}%', ha='center', va='bottom', fontweight='bold')

    # Linha de dificuldade média
    ax2 = ax1.twinx()
    ax2.plot(tentativas_labels, dificuldade, color='red', marker='s', linewidth=2, markersize=6)
    ax2.set_ylabel('Dificuldade Média')
    ax2.set_ylim(0, max(dificuldade + [2.0]) + 0.5)
    ax2.axhline(2.0, color='orange', linestyle='--', alpha=0.8, label='Limite: 2.0')
    ax2.legend(loc='upper right')

    plt.title(f"Progresso no Nível {nivel}")
    plt.tight_layout()
    plt.show()
    
    # Análise em interface
    mostrar_analise_nivel(nivel, tentativas, percentuais, dificuldade)

def mostrar_analise_nivel(nivel, tentativas, percentuais, dificuldade):
    """Mostra análise pedagógica em janela customtkinter"""
    ultima_tentativa = tentativas[-1]
    ultimo_percentual = percentuais[-1]
    ultima_dificuldade = dificuldade[-1]
    
    # Criar janela de análise
    janela = ctk.CTk()
    janela.title(f"Análise - Nível {nivel}")
    janela.geometry("500x400")
    janela.resizable(True, True)
    
    frame = ctk.CTkFrame(janela)
    frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    # Título
    titulo = ctk.CTkLabel(frame, text=f"Análise - Nível {nivel}", 
                         font=ctk.CTkFont(size=20, weight="bold"))
    titulo.pack(pady=(10, 20))
    
    # Área de texto para análise
    text_frame = tk.Frame(frame)
    text_frame.pack(expand=True, fill="both", padx=10, pady=10)
    
    text_area = Text(text_frame, wrap="word", font=("Arial", 12), 
                     bg="#f0f0f0", relief="flat", borderwidth=0)
    scroll = Scrollbar(text_frame, command=text_area.yview)
    text_area.configure(yscrollcommand=scroll.set)
    
    text_area.pack(side="left", fill="both", expand=True)
    scroll.pack(side=RIGHT, fill=Y)
    
    # Conteúdo da análise
    analise = f"""DESEMPENHO ATUAL
Última performance: {ultimo_percentual:.0f}% de acerto
Dificuldade atual: {ultima_dificuldade:.1f}

STATUS DO DESEMPENHO
"""
    
    if ultimo_percentual >= 80:
        analise += "Excelente! Você domina este nível.\n\n"
    elif ultimo_percentual >= 70:
        analise += "Bom desempenho, continue praticando.\n\n"
    else:
        analise += "Precisa melhorar. Revise os conceitos básicos.\n\n"
    
    analise += "RECOMENDAÇÕES\n"
    if ultima_dificuldade > 2.5:
        analise += "• Use mais dicas fixas e consulte a IA quando tiver dúvidas.\n\n"
    elif ultima_dificuldade > 2.0:
        analise += "• Tente usar menos dicas para aumentar a confiança.\n\n"
    
    if len(tentativas) > 1:
        melhoria_perc = percentuais[-1] - percentuais[-2]
        melhoria_dif = dificuldade[-2] - dificuldade[-1]
        
        analise += "EVOLUÇÃO ENTRE TENTATIVAS\n"
        if melhoria_perc > 10:
            analise += "Grande melhoria na taxa de acerto!\n"
        elif melhoria_perc > 0:
            analise += "Melhorando gradualmente.\n"
        elif melhoria_perc < -10:
            analise += "Atenção! Performance caiu significativamente.\n"
        
        if melhoria_dif > 0.5:
            analise += "Está resolvendo com menos dificuldade!\n"
    
    text_area.insert("1.0", analise)
    text_area.config(state="disabled")
    
    # Botão fechar
    btn_fechar = ctk.CTkButton(frame, text="Fechar", command=janela.destroy)
    btn_fechar.pack(pady=10)
    
    janela.mainloop()

def grafico_resumo_geral(perfil_path):
    """
    Gera um gráfico de radar mostrando o desempenho geral do aluno em todos os níveis.
    """
    dados = carregar_perfil(perfil_path)
    niveis = sorted([int(k) for k in dados["niveis"].keys()])
    if not niveis:
        return
        
    acertos = []
    dificuldade_normalizada = []
    labels = []
    
    for n in niveis:
        nivel_str = str(n)
        labels.append(f"Nível {n}")
        tentativas = dados["niveis"][nivel_str].get("tentativas_anteriores", [])
        if tentativas:
            ultima = tentativas[-1]
            taxa_acerto = ultima["acertos"] / ultima["total_questoes"] if ultima["total_questoes"] > 0 else 0
            facilidade = max(0, 1 - (ultima["dificuldade_media"] / 4.0))
            acertos.append(taxa_acerto)
            dificuldade_normalizada.append(facilidade)
        else:
            acertos.append(0)
            dificuldade_normalizada.append(0)

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    acertos += acertos[:1]
    dificuldade_normalizada += dificuldade_normalizada[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.plot(angles, acertos, 'o-', linewidth=2, color='green', label='Taxa de Acerto')
    ax.fill(angles, acertos, alpha=0.25, color='green')
    ax.plot(angles, dificuldade_normalizada, 's-', linewidth=2, color='blue', label='Facilidade')
    ax.fill(angles, dificuldade_normalizada, alpha=0.15, color='blue')
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_ylim(0, 1.1)
    plt.title("Resumo Geral de Desempenho")
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.tight_layout()
    plt.show()
    
    # Análise em interface
    mostrar_resumo_geral(acertos, niveis)

def mostrar_resumo_geral(acertos, niveis):
    """Mostra resumo geral em interface"""
    niveis_com_dados = [i for i, a in enumerate(acertos[:-1]) if a > 0]
    if not niveis_com_dados:
        return
        
    janela = ctk.CTk()
    janela.title("Resumo Geral")
    janela.geometry("400x300")
    
    frame = ctk.CTkFrame(janela)
    frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    titulo = ctk.CTkLabel(frame, text="Resumo Geral", 
                         font=ctk.CTkFont(size=20, weight="bold"))
    titulo.pack(pady=(10, 20))
    
    media_acerto = np.mean([acertos[i] for i in niveis_com_dados])
    
    resumo = f"""ESTATÍSTICAS GERAIS
Níveis iniciados: {len(niveis_com_dados)} de 3
Taxa média de acerto: {media_acerto*100:.0f}%

AVALIAÇÃO GERAL
"""
    
    if media_acerto >= 0.8:
        resumo += "Excelente domínio!"
    elif media_acerto >= 0.7:
        resumo += "Bom, continue assim."
    else:
        resumo += "Precisa de mais prática."
        
    if len(niveis_com_dados) > 1:
        acertos_niveis = [(i, acertos[i]) for i in niveis_com_dados if acertos[i] > 0]
        if acertos_niveis:
            pior_nivel_idx, menor_acerto = min(acertos_niveis, key=lambda x: x[1])
            resumo += f"\n\nRECOMENDAÇÃO\nFoco: Nível {niveis[pior_nivel_idx]} ({menor_acerto*100:.0f}% acerto)"
    
    label_resumo = ctk.CTkLabel(frame, text=resumo, font=ctk.CTkFont(size=14), 
                               justify="left")
    label_resumo.pack(pady=20)
    
    btn_fechar = ctk.CTkButton(frame, text="Fechar", command=janela.destroy)
    btn_fechar.pack(pady=10)
    
    janela.mainloop()

def grafico_status_niveis(perfil_path):
    """
    Mostra um gráfico vertical de nós conectados representando o status de cada nível.
    """
    from matplotlib.patches import FancyBboxPatch
    import matplotlib.lines as mlines
    from matplotlib.patches import Patch
    
    dados = carregar_perfil(perfil_path)
    niveis = sorted([int(k) for k in dados["niveis"].keys()])
    
    fig, ax = plt.subplots(figsize=(6, len(niveis)*2))
    y_positions = list(range(len(niveis)))[::-1]
    
    status_cores = {
        'concluido': '#228B22',      # Verde escuro
        'liberado': '#90EE90',       # Verde claro  
        'bloqueado': '#8B0000',      # Vermelho escuro
        'tentado': '#FF7F7F',        # Vermelho claro
    }
    
    status_info = []
    
    for i, n in enumerate(niveis):
        nivel_str = str(n)
        nivel_key = f"nivel_{n}"
        y = y_positions[i]
        
        if dados["niveis"][nivel_str].get("concluido_com_sucesso", False):
            cor = status_cores['concluido']
            status = "Concluído"
        elif dados.get("modulos_liberados", {}).get(nivel_key, False):
            tentativas = dados["niveis"][nivel_str].get("tentativas_anteriores", [])
            if tentativas:
                cor = status_cores['tentado']
                ultima_taxa = tentativas[-1]["acertos"] / tentativas[-1]["total_questoes"] if tentativas[-1]["total_questoes"] > 0 else 0
                status = f"Tentado ({ultima_taxa*100:.0f}%)"
            else:
                cor = status_cores['liberado']
                status = "Liberado"
        else:
            cor = status_cores['bloqueado']
            status = "Bloqueado"
        
        status_info.append((n, status, cor))
        
        box = FancyBboxPatch((0.3, y-0.2), 1.4, 0.4, boxstyle="round,pad=0.1", 
                           linewidth=2, edgecolor='black', facecolor=cor)
        ax.add_patch(box)
        
        ax.text(1, y, f"Nível {n}", va='center', ha='center', 
               fontsize=13, color='black', fontweight='bold')
        ax.text(1.8, y, status, va='center', ha='left', fontsize=10, color='black')
        
        if i < len(niveis)-1:
            ax.add_line(mlines.Line2D([1, 1], [y-0.2, y_positions[i+1]+0.2], 
                                    color='gray', linewidth=2, zorder=0))

    ax.set_xlim(0, 3)
    ax.set_ylim(-0.5, len(niveis)-0.5)
    ax.axis('off')
    plt.title("Progresso dos Níveis", fontsize=15, fontweight='bold')
    
    legend_elements = [
        Patch(facecolor=status_cores['concluido'], edgecolor='black', label='Concluído'),
        Patch(facecolor=status_cores['liberado'], edgecolor='black', label='Liberado'),
        Patch(facecolor=status_cores['tentado'], edgecolor='black', label='Tentado'),
        Patch(facecolor=status_cores['bloqueado'], edgecolor='black', label='Bloqueado'),
    ]
    ax.legend(handles=legend_elements, loc='lower right')
    plt.tight_layout()
    plt.show()
    
    # Análise em interface
    mostrar_status_progressao(status_info)

def mostrar_status_progressao(status_info):
    """Mostra status de progressão em interface"""
    concluidos = len([s for _, s, _ in status_info if "Concluído" in s])
    tentados = len([s for _, s, _ in status_info if "Tentado" in s])
    liberados = len([s for _, s, _ in status_info if "Liberado" in s])
    
    janela = ctk.CTk()
    janela.title("Status de Progressão")
    janela.geometry("350x250")
    
    frame = ctk.CTkFrame(janela)
    frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    titulo = ctk.CTkLabel(frame, text="Status de Progressão", 
                         font=ctk.CTkFont(size=18, weight="bold"))
    titulo.pack(pady=(10, 20))
    
    status_text = f"""ESTATÍSTICAS
Níveis concluídos: {concluidos} de 3
Níveis em progresso: {tentados}
Níveis disponíveis: {liberados}

"""
    
    # Próximo passo
    for nivel, status, _ in status_info:
        if "Liberado" in status:
            status_text += f"Próximo passo: Iniciar Nível {nivel}"
            break
        elif "Tentado" in status and not status.startswith("Tentado (100"):
            status_text += f"Próximo passo: Melhorar Nível {nivel}"
            break
    
    label_status = ctk.CTkLabel(frame, text=status_text, font=ctk.CTkFont(size=12), 
                               justify="left")
    label_status.pack(pady=10)
    
    btn_fechar = ctk.CTkButton(frame, text="Fechar", command=janela.destroy)
    btn_fechar.pack(pady=10)
    
    janela.mainloop()

def extrair_conceitos_de_questao(questao_data):
    """
    ✅ NOVA FUNÇÃO: Extrai conceitos reais das questões baseado nos dados disponíveis
    """
    conceitos = set()
    
    # 1. Buscar no campo 'conceitos' (lista)
    if 'conceitos' in questao_data and questao_data['conceitos']:
        if isinstance(questao_data['conceitos'], list):
            conceitos.update(questao_data['conceitos'])
        else:
            conceitos.add(str(questao_data['conceitos']))
    
    # 2. Buscar no campo 'conceito' (string única)
    if 'conceito' in questao_data and questao_data['conceito']:
        conceitos.add(str(questao_data['conceito']))
    
    # 3. Buscar nos campos 'topico' ou 'topicos'
    for campo in ['topico', 'topicos']:
        if campo in questao_data and questao_data[campo]:
            if isinstance(questao_data[campo], list):
                conceitos.update(questao_data[campo])
            else:
                conceitos.add(str(questao_data[campo]))
    
    # 4. Inferir conceitos baseado no ID e tipo da questão (fallback)
    if not conceitos:
        q_id = questao_data.get("id", 0)
        tipo = questao_data.get("tipo", "simbolica")
        
        if tipo == "traducao":
            if q_id <= 3:
                conceitos.add("Tradução Básica")
            elif q_id <= 6:
                conceitos.add("Conectivos Lógicos")
            else:
                conceitos.add("Tradução Avançada")
        else:
            if q_id <= 2:
                conceitos.add("Equivalências Básicas")
            elif q_id <= 4:
                conceitos.add("Lei de De Morgan")
            elif q_id <= 6:
                conceitos.add("Distributividade")
            elif q_id <= 8:
                conceitos.add("Associatividade")
            else:
                conceitos.add("Comutatividade")
    
    # 5. Se ainda não há conceitos, usar categoria genérica
    if not conceitos:
        conceitos.add("Lógica Proposicional")
    
    return list(conceitos)

def carregar_questoes_para_analise():
    """
    ✅ NOVA FUNÇÃO: Carrega todas as questões dos arquivos JSON para análise completa
    """
    import os
    import json
    from src.config import QUESTOES_PATH
    
    todas_questoes = {}
    
    # Carregar questões de todos os níveis
    for nivel in [1, 2, 3]:
        caminho_arquivo = os.path.join(QUESTOES_PATH, f"nivel{nivel}.json")
        if os.path.exists(caminho_arquivo):
            try:
                with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                    dados = json.load(arquivo)
                    if isinstance(dados, list):
                        questoes = dados
                    elif isinstance(dados, dict) and "questoes" in dados:
                        questoes = dados["questoes"]
                    else:
                        questoes = []
                    
                    # Indexar por ID
                    for q in questoes:
                        q_id = q.get("id")
                        if q_id is not None:
                            todas_questoes[str(q_id)] = q
                            
            except Exception as e:
                print(f"Erro ao carregar questões do nível {nivel}: {e}")
    
    return todas_questoes

def grafico_por_conceito(perfil_path):
    """
    ✅ MELHORADA: Mostra um gráfico radar com desempenho por conceito/tópico REAL das questões
    """
    dados = carregar_perfil(perfil_path)
    
    # ✅ Carregar questões reais dos arquivos JSON
    todas_questoes = carregar_questoes_para_analise()
    
    # Buscar conceitos REAIS em resumo_questoes
    conceitos_stats = defaultdict(lambda: {
        "acertos": 0, "total": 0, "dificuldades": [], "questoes_ids": []
    })
    
    # Processar todas as tentativas de todos os níveis
    for nivel in dados["niveis"].values():
        for tentativa in nivel.get("tentativas_anteriores", []):
            for q in tentativa.get("resumo_questoes", []):
                q_id = str(q.get("id", ""))
                
                # ✅ Buscar questão real no arquivo JSON
                questao_real = todas_questoes.get(q_id, {})
                
                if questao_real:
                    # ✅ Extrair conceitos REAIS da questão
                    conceitos_questao = extrair_conceitos_de_questao(questao_real)
                else:
                    # Fallback se não encontrar a questão
                    conceitos_questao = extrair_conceitos_de_questao({"id": q.get("id", 0)})
                
                # Registrar dados para cada conceito
                for conceito in conceitos_questao:
                    conceitos_stats[conceito]["acertos"] += int(q.get("acertou", False))
                    conceitos_stats[conceito]["total"] += 1
                    conceitos_stats[conceito]["dificuldades"].append(q.get("dificuldade_calculada", 0.0))
                    conceitos_stats[conceito]["questoes_ids"].append(q_id)

    if not conceitos_stats:
        # Se não há dados, mostrar mensagem
        janela = ctk.CTk()
        janela.title("Análise por Conceito")
        janela.geometry("400x200")
        
        frame = ctk.CTkFrame(janela)
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        label = ctk.CTkLabel(frame, text="Nenhum dado de conceito encontrado\n\nComplete alguns exercícios primeiro!", 
                           font=ctk.CTkFont(size=16))
        label.pack(expand=True)
        
        btn_fechar = ctk.CTkButton(frame, text="Fechar", command=janela.destroy)
        btn_fechar.pack(pady=10)
        
        janela.mainloop()
        return

    conceitos = list(conceitos_stats.keys())
    acertos = []
    facilidades = []
    
    for c in conceitos:
        stats = conceitos_stats[c]
        taxa_acerto = stats["acertos"] / stats["total"] if stats["total"] > 0 else 0
        dif_media = np.mean(stats["dificuldades"]) if stats["dificuldades"] else 0
        facilidade = max(0, 1 - (dif_media / 4.0))
        
        acertos.append(taxa_acerto)
        facilidades.append(facilidade)

    # ✅ Gráfico radar melhorado
    angles = np.linspace(0, 2 * np.pi, len(conceitos), endpoint=False).tolist()
    acertos += acertos[:1]
    facilidades += facilidades[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    ax.plot(angles, acertos, 'o-', linewidth=3, color='green', label='Taxa de Acerto', markersize=8)
    ax.fill(angles, acertos, alpha=0.25, color='green')
    ax.plot(angles, facilidades, 's-', linewidth=3, color='blue', label='Facilidade', markersize=8)
    ax.fill(angles, facilidades, alpha=0.15, color='blue')
    
    # ✅ Melhorar labels dos conceitos (quebrar linhas se necessário)
    conceitos_quebrados = [c.replace(' ', '\n') if len(c) > 12 else c for c in conceitos]
    ax.set_thetagrids(np.degrees(angles[:-1]), conceitos_quebrados, fontsize=10)
    ax.set_ylim(0, 1.1)
    ax.set_title("Desempenho por Conceito/Tópico", fontsize=16, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=12)
    
    # ✅ Grid radial
    ax.grid(True, alpha=0.3)
    ax.set_rlabel_position(45)
    
    plt.tight_layout()
    plt.show()

    # Análise em interface
    mostrar_analise_conceitos(conceitos, acertos, conceitos_stats)

def mostrar_analise_conceitos(conceitos, acertos, conceitos_stats):
    """
    ✅ MELHORADA: Mostra análise detalhada de conceitos em interface
    """
    pontos_fracos = []
    pontos_fortes = []
    
    for i, c in enumerate(conceitos):
        stats = conceitos_stats[c]
        taxa = acertos[i]
        dif_media = np.mean(stats["dificuldades"]) if stats["dificuldades"] else 0
        total_questoes = stats["total"]
        
        if taxa < 0.6 or dif_media > 2.5:
            pontos_fracos.append((c, taxa, dif_media, total_questoes))
        elif taxa >= 0.85 and dif_media <= 1.5:
            pontos_fortes.append((c, taxa, dif_media, total_questoes))
    
    janela = ctk.CTk()
    janela.title("Análise Detalhada por Conceitos")
    janela.geometry("600x500")
    janela.resizable(True, True)
    
    frame = ctk.CTkFrame(janela)
    frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    titulo = ctk.CTkLabel(frame, text="📊 Análise Detalhada por Conceitos", 
                         font=ctk.CTkFont(size=20, weight="bold"))
    titulo.pack(pady=(10, 20))
    
    text_frame = tk.Frame(frame)
    text_frame.pack(expand=True, fill="both", padx=10, pady=10)
    
    text_area = Text(text_frame, wrap="word", font=("Arial", 11), 
                     bg="#f0f0f0", relief="flat", borderwidth=0)
    scroll = Scrollbar(text_frame, command=text_area.yview)
    text_area.configure(yscrollcommand=scroll.set)
    
    text_area.pack(side="left", fill="both", expand=True)
    scroll.pack(side=RIGHT, fill=Y)
    
    # ✅ Análise mais detalhada
    analise = "🧠 ANÁLISE DETALHADA POR CONCEITOS\n"
    analise += "=" * 50 + "\n\n"
    
    # Estatísticas gerais
    total_conceitos = len(conceitos)
    media_geral = np.mean(acertos[:-1]) if acertos[:-1] else 0
    analise += f"📈 VISÃO GERAL:\n"
    analise += f"• Total de conceitos identificados: {total_conceitos}\n"
    analise += f"• Taxa média geral: {media_geral*100:.1f}%\n"
    analise += f"• Conceitos com dificuldade: {len(pontos_fracos)}\n"
    analise += f"• Conceitos dominados: {len(pontos_fortes)}\n\n"
    
    # Pontos fortes
    if pontos_fortes:
        analise += "✅ CONCEITOS BEM DOMINADOS:\n"
        pontos_fortes.sort(key=lambda x: x[1], reverse=True)
        for i, (conceito, taxa, dif, total) in enumerate(pontos_fortes[:5]):  # Top 5
            analise += f"{i+1}. {conceito}:\n"
            analise += f"   • Taxa de acerto: {taxa*100:.1f}%\n"
            analise += f"   • Dificuldade média: {dif:.2f}\n"
            analise += f"   • Questões resolvidas: {total}\n\n"
    
    # Pontos fracos
    if pontos_fracos:
        analise += "⚠️ CONCEITOS QUE PRECISAM DE ATENÇÃO:\n"
        pontos_fracos.sort(key=lambda x: (x[1], -x[2]))  # Pior taxa primeiro, maior dificuldade depois
        for i, (conceito, taxa, dif, total) in enumerate(pontos_fracos):
            prioridade = "🔴 CRÍTICO" if taxa < 0.4 or dif > 3.0 else "🟡 MODERADO"
            analise += f"{i+1}. {conceito} ({prioridade}):\n"
            analise += f"   • Taxa de acerto: {taxa*100:.1f}%\n"
            analise += f"   • Dificuldade média: {dif:.2f}\n"
            analise += f"   • Questões resolvidas: {total}\n"
            
            # ✅ Sugestões específicas por conceito
            if "De Morgan" in conceito:
                analise += f"   💡 Dica: Revise as leis de De Morgan (¬(A∧B) = ¬A∨¬B)\n"
            elif "Distributiv" in conceito:
                analise += f"   💡 Dica: Pratique A∧(B∨C) = (A∧B)∨(A∧C)\n"
            elif "Tradução" in conceito:
                analise += f"   💡 Dica: Identifique conectivos no português (e, ou, se...então)\n"
            elif "Conectivos" in conceito:
                analise += f"   💡 Dica: Memorize: ∧=e, ∨=ou, →=se...então, ↔=se e somente se\n"
            else:
                analise += f"   💡 Dica: Revise teoria e pratique exercícios similares\n"
            analise += "\n"
        
        # ✅ Plano de estudos
        analise += "📚 PLANO DE ESTUDOS RECOMENDADO:\n"
        if len(pontos_fracos) <= 2:
            analise += "• Dedique 45-60 minutos por conceito\n"
            analise += "• Foque 1 conceito por dia\n"
        elif len(pontos_fracos) <= 4:
            analise += "• Dedique 30-45 minutos por conceito\n"
            analise += "• Estude 1-2 conceitos por semana\n"
        else:
            analise += "• Dedique 20-30 minutos por conceito\n"
            analise += "• Priorize os conceitos críticos primeiro\n"
        
        analise += "• Use dicas fixas para compreender a teoria\n"
        analise += "• Consulte a IA quando tiver dúvidas específicas\n\n"
    else:
        analise += "🎉 PARABÉNS! Nenhum ponto fraco crítico identificado.\n"
        analise += "Você está dominando bem todos os conceitos!\n\n"
        analise += "📈 PRÓXIMOS PASSOS:\n"
        analise += "• Tente resolver exercícios usando menos dicas\n"
        analise += "• Avance para níveis mais desafiadores\n"
        analise += "• Pratique exercícios de tempo limitado\n\n"
    
    # ✅ Resumo final
    analise += "=" * 50 + "\n"
    analise += f"📊 RESUMO FINAL: {media_geral*100:.1f}% de domínio geral\n"
    if media_geral >= 0.85:
        analise += "🏆 Status: EXCELENTE - Continue assim!"
    elif media_geral >= 0.70:
        analise += "👍 Status: BOM - Pequenos ajustes necessários"
    elif media_geral >= 0.50:
        analise += "📖 Status: REGULAR - Foque nos pontos fracos"
    else:
        analise += "📚 Status: INICIANTE - Revise conceitos básicos"
    
    text_area.insert("1.0", analise)
    text_area.config(state="disabled")
    
    btn_fechar = ctk.CTkButton(frame, text="Fechar", command=janela.destroy)
    btn_fechar.pack(pady=10)
    
    janela.mainloop()