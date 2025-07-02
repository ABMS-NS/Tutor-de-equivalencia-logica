# levels_selection_window.py - Seleção de níveis de exercícios

import customtkinter as ctk
from tkinter import messagebox
from src.config import NIVEIS_CONFIG
from src.screens.exercise_window import ExerciseWindow
from src.perfil.perfil import carregar_perfil
from src.perfil.progresso import resetar_nivel
from src.pedagogico.liberacao import verificar_status_nivel

class LevelsSelectionWindow:
    def __init__(self, parent, app_instance, perfil, perfil_path):
        self.parent = parent
        self.app_instance = app_instance
        self.dados_perfil = perfil
        self.perfil_path = perfil_path

        try:
            dados_atualizados = carregar_perfil(perfil_path)
            if dados_atualizados:
                self.dados_perfil = dados_atualizados
                print(f"✅ Perfil atualizado com sucesso")
            else:
                print("⚠️ Nenhum dado de perfil encontrado.")
        except Exception as e:
            print(f"❌ Erro ao carregar perfil: {e}")
            
        # Janela de seleção de níveis
        largura, altura = 800, 700
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Seleção de Níveis")
        x = int(self.window.winfo_screenwidth() / 2 - largura / 2)
        y = int(self.window.winfo_screenheight() / 2 - altura / 2)
        self.window.geometry(f"{largura}x{altura}+{x}+{y}")
        self.window.resizable(True, True)

        self.window.grab_set()
        self.window.focus_set()

        self.criar_interface()

    def criar_interface(self):
        """Cria a interface da janela de seleção de níveis"""
        # Limpa a janela para redesenhar (caso de reset)
        for widget in self.window.winfo_children():
            widget.destroy()

        frame_principal = ctk.CTkFrame(self.window, fg_color="transparent")
        frame_principal.pack(expand=True, fill="both", padx=30, pady=30)

        titulo = ctk.CTkLabel(frame_principal, text="Escolha o Nível", font=ctk.CTkFont(size=28, weight="bold"))
        titulo.pack(pady=(10, 20))

        # Container para os botões dos níveis
        frame_niveis = ctk.CTkFrame(frame_principal)
        frame_niveis.pack(expand=True, fill="both", pady=10)

        niveis_ids = sorted([int(k) for k in NIVEIS_CONFIG.keys()])
        for nivel_id in niveis_ids:
            self.criar_botao_nivel(frame_niveis, nivel_id)

    def criar_botao_nivel(self, parent, nivel):
        """Cria um frame para cada nível com status e botões de ação."""
        status, info = verificar_status_nivel(self.dados_perfil, nivel)

        # ✅ DEBUG: Verificar se status está sendo atualizado
        nivel_data = self.dados_perfil["niveis"].get(str(nivel), {})
        questoes_respondidas = len(nivel_data.get("questoes_respondidas", []))
        concluido = nivel_data.get("concluido_com_sucesso", False)
        liberado = nivel_data.get("liberado", False)
        
        print(f"🔍 DEBUG Nível {nivel}:")
        print(f"   - Status: {status}")
        print(f"   - Liberado: {liberado}")  
        print(f"   - Concluído: {concluido}")
        print(f"   - Questões: {questoes_respondidas}")

        frame_nivel = ctk.CTkFrame(parent, border_width=1, border_color="gray25")
        frame_nivel.pack(fill="x", padx=20, pady=10, ipady=10)
        frame_nivel.grid_columnconfigure(1, weight=1)

        # Ícone de Status
        icone_status = {"Concluído": "✅", "Disponível": "▶️", "Bloqueado": "🔒"}
        label_icone = ctk.CTkLabel(frame_nivel, text=icone_status.get(status, ""), font=ctk.CTkFont(size=20))
        label_icone.grid(row=0, column=0, rowspan=2, padx=15, sticky="ns")

        # Título e Status
        label_titulo = ctk.CTkLabel(frame_nivel, text=f"Nível {nivel}", font=ctk.CTkFont(size=18, weight="bold"), anchor="w")
        label_titulo.grid(row=0, column=1, sticky="ew", padx=5)

        label_status = ctk.CTkLabel(frame_nivel, text=info, font=ctk.CTkFont(size=12), text_color="gray", anchor="w")
        label_status.grid(row=1, column=1, sticky="ew", padx=5)

        # Botões de Ação
        frame_botoes = ctk.CTkFrame(frame_nivel, fg_color="transparent")
        frame_botoes.grid(row=0, column=2, rowspan=2, padx=15)

        # ✅ CORREÇÃO: Lógica dos botões baseada no status atual
        if status in ["Disponível", "Concluído"]:
            # ✅ Texto e cor do botão baseado no status ATUALIZADO
            if status == "Concluído":
                texto_botao = "🎮 Continuar"  # Pode jogar novamente
                cor_botao = "#28a745"  # Verde para concluído
            else:
                texto_botao = "🚀 Iniciar"   # Primeira vez
                cor_botao = "#007bff"  # Azul para disponível
                
            btn_iniciar = ctk.CTkButton(
                frame_botoes, 
                text=texto_botao, 
                width=100,
                fg_color=cor_botao,
                command=lambda n=nivel: self.iniciar_nivel(n)
            )
            btn_iniciar.pack(side="left", padx=(0, 5))

            # ✅ CORREÇÃO: Botão "Nova Tentativa" para QUALQUER nível liberado
            # (Tanto concluído quanto não concluído com progresso)
            nivel_data = self.dados_perfil["niveis"].get(str(nivel), {})
            tem_progresso = len(nivel_data.get("questoes_respondidas", [])) > 0
            
            if tem_progresso:  # Se já respondeu pelo menos uma questão
                btn_nova_tentativa = ctk.CTkButton(
                    frame_botoes, 
                    text="🔄 Nova Tentativa", 
                    width=120,
                    fg_color="#ff6b35", 
                    hover_color="#e55a2b",
                    command=lambda n=nivel: self.nova_tentativa(n)
                )
                btn_nova_tentativa.pack(side="left")
        else:
            # Nível bloqueado
            btn_bloqueado = ctk.CTkButton(
                frame_botoes,
                text="🔒 Bloqueado",
                width=200,
                fg_color="#6c757d",
                state="disabled"
            )
            btn_bloqueado.pack()

    def iniciar_nivel(self, nivel):
        """Fecha a janela atual e abre a janela de exercícios."""
        self.window.destroy()
        ExerciseWindow(self.parent, nivel, self.app_instance, self.perfil_path)

    def nova_tentativa(self, nivel):
        """✅ NOVA FUNÇÃO: Permite refazer qualquer nível liberado"""
        nivel_data = self.dados_perfil["niveis"].get(str(nivel), {})
        questoes_respondidas = len(nivel_data.get("questoes_respondidas", []))
        concluido = nivel_data.get("concluido_com_sucesso", False)
        
        # Mensagem personalizada baseada no status
        if concluido:
            msg_titulo = "🔄 Refazer Nível Concluído"
            msg_texto = (
                f"Deseja fazer uma nova tentativa do Nível {nivel}?\n\n"
                f"✅ Você já concluiu este nível com sucesso\n"
                f"📊 Progresso atual: {questoes_respondidas} questões\n\n"
                f"🔄 Seu progresso será arquivado\n"
                f"🎯 Você começará uma nova tentativa\n\n"
                f"Continuar?"
            )
        else:
            msg_titulo = "🔄 Nova Tentativa"
            msg_texto = (
                f"Deseja recomeçar o Nível {nivel}?\n\n"
                f"📊 Progresso atual: {questoes_respondidas} questões respondidas\n"
                f"❌ Nível ainda não foi concluído\n\n"
                f"🔄 Seu progresso será arquivado\n"
                f"🎯 Você começará do zero novamente\n\n"
                f"Continuar?"
            )
        
        resposta = messagebox.askyesno(
            msg_titulo,
            msg_texto,
            icon="question"
        )
        
        if resposta:
            try:
                # Reseta o nível (arquiva progresso atual)
                resetar_nivel(nivel, self.perfil_path)
                
                # Recarrega o perfil atualizado
                self.dados_perfil = carregar_perfil(self.perfil_path)
                
                # Atualiza a interface
                self.criar_interface()
                
                # Mensagem de confirmação
                messagebox.showinfo(
                    "✅ Nova Tentativa Preparada", 
                    f"O Nível {nivel} está pronto para uma nova tentativa!\n\n"
                    f"📁 Seu progresso anterior foi arquivado\n"
                    f"🎯 Você pode começar agora mesmo"
                )
                
            except Exception as e:
                messagebox.showerror(
                    "❌ Erro", 
                    f"Erro ao preparar nova tentativa:\n{str(e)}"
                )