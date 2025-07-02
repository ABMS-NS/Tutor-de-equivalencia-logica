# exercise_window.py - Modal para exercícios de cada nível
import customtkinter as ctk
from tkinter import messagebox
import time
import os
import json
from src.config import EXERCISE_WINDOW, NIVEIS_CONFIG
from src.utils import centralizar_janela
from src.perfil.progresso import registrar_questao
from src.llm_interface.llm_client import obter_dica_gemini, avaliar_traducao_logica, obter_explicacao_avaliacao
from src.screens.modal_final_nivel import ModalFinalNivel
from src.screens.teclado_logico import TecladoLogico
from src.screens.modal_avaliacao import ModalAvaliacao
from src.especialista.avaliador import avaliar_passos
from src.pedagogico.liberacao import processar_conclusao_de_nivel

def carregar_questoes_nivel(nivel):
    """Carrega as questões do nível especificado do arquivo json"""
    from src.config import QUESTOES_PATH
    
    caminho_arquivo = os.path.join(QUESTOES_PATH, f"nivel{nivel}.json")
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            questoes = json.load(arquivo)
            if isinstance(questoes, list):
                return questoes
            elif isinstance(questoes, dict) and "questoes" in questoes:
                return questoes["questoes"]
            else:
                return []
    else:
        messagebox.showerror("Erro", f"Arquivo de questões do nível {nivel} não encontrado em {caminho_arquivo}.")
        return []

class ExerciseWindow:
    def __init__(self, parent, nivel, app_instance, perfil_path):
        self.parent = parent
        self.app_instance = app_instance
        self.nivel = nivel
        self.perfil_path = perfil_path
        self.questoes = carregar_questoes_nivel(self.nivel)
        
        if not self.questoes:
            messagebox.showwarning("Aviso", f"Nenhuma questão encontrada para o nível {self.nivel}")
            return

        # --- Estado da Janela e do Progresso ---
        self.questao_idx = 0
        self.erros_tentativa_atual = 0
        self.dicas_fixas_usadas = 0
        self.dicas_llm_usadas_total = 0
        self.dicas_llm_por_questao = {}
        self.start_time = None
        self.timer_id = None
        
        # ✅ NOVO: Controle do tipo de questão
        self.tipo_questao_atual = None

        # --- Configuração da Janela ---
        largura = EXERCISE_WINDOW.get("width", 1200)
        altura = EXERCISE_WINDOW.get("height", 800)
        self.window = ctk.CTkToplevel(parent)
        self.window.title(f"Nível {self.nivel} - Exercícios")
        self.window.geometry(f"{largura}x{altura}")
        centralizar_janela(self.window, largura, altura)
        self.window.resizable(True, True)
        
        self.window.grab_set()
        self.window.focus_set()
        
        self.criar_interface()
        self.carregar_proxima_questao()

    def criar_interface(self):
        # Frame principal com grid melhorado
        self.frame_principal = ctk.CTkFrame(self.window)
        self.frame_principal.pack(expand=True, fill="both", padx=10, pady=10)
        self.frame_principal.grid_columnconfigure(0, weight=1)
        self.frame_principal.grid_rowconfigure(0, weight=0)  # Status
        self.frame_principal.grid_rowconfigure(1, weight=0)  # Pergunta
        self.frame_principal.grid_rowconfigure(2, weight=1)  # Resposta (expansível)
        self.frame_principal.grid_rowconfigure(3, weight=0)  # Assistente

        # --- Frames ---
        self.criar_frame_status(self.frame_principal)
        self.criar_frame_pergunta(self.frame_principal)
        self.criar_frame_resposta(self.frame_principal)
        self.criar_frame_assistente(self.frame_principal)

    def criar_frame_status(self, parent):
        frame_status = ctk.CTkFrame(parent)
        frame_status.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        frame_status.grid_columnconfigure(0, weight=1)
        frame_status.grid_columnconfigure(1, weight=1)

        self.label_contador_questoes = ctk.CTkLabel(
            frame_status, 
            text=f"Questão 1/{len(self.questoes)}", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.label_contador_questoes.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.label_timer = ctk.CTkLabel(
            frame_status, 
            text="Tempo: 00:00", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.label_timer.grid(row=0, column=1, padx=10, pady=5, sticky="e")

    def criar_frame_pergunta(self, parent):
        frame_pergunta = ctk.CTkFrame(parent)
        frame_pergunta.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        
        # Título
        label_titulo = ctk.CTkLabel(
            frame_pergunta, 
            text="📋 Questão", 
            font=ctk.CTkFont(size=16, weight="bold"), 
            anchor="w"
        )
        label_titulo.pack(fill="x", padx=15, pady=(10, 5))
        
        # Frame para tópico e legenda
        self.frame_topico_legenda = ctk.CTkFrame(frame_pergunta, fg_color="transparent")
        self.frame_topico_legenda.pack(fill="x", padx=15, pady=(0, 5))
        
        # Enunciado
        self.texto_pergunta = ctk.CTkTextbox(
            frame_pergunta, 
            height=80, 
            font=ctk.CTkFont(size=14), 
            wrap="word"
        )
        self.texto_pergunta.pack(fill="x", padx=15, pady=(5, 5))
        self.texto_pergunta.configure(state="disabled")

    def atualizar_topico_legenda(self):
        """Atualiza o frame de tópico e legenda com base na questão atual"""
        # Limpar frame anterior
        for widget in self.frame_topico_legenda.winfo_children():
            widget.destroy()
        
        questao_atual = self.questoes[self.questao_idx]
        conceitos = (questao_atual.get("conceitos") or 
                    questao_atual.get("conceito") or 
                    questao_atual.get("topico") or 
                    questao_atual.get("topicos"))
        legenda = questao_atual.get("legenda", {})
        
        # Container horizontal para tópicos e legenda
        container = ctk.CTkFrame(self.frame_topico_legenda, fg_color="transparent")
        container.pack(fill="x")
        
        # Tópicos (lado esquerdo)
        if conceitos:
            if isinstance(conceitos, list):
                conceitos_str = ", ".join(str(c) for c in conceitos)
            else:
                conceitos_str = str(conceitos)
            label_conceito = ctk.CTkLabel(
                container,
                text=f"🧠 Tópico(s): {conceitos_str}",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#1a73e8",
                anchor="w"
            )
            label_conceito.pack(side="left", padx=(0, 20))
        
        # Legenda (lado direito)
        if legenda:
            legenda_str = " | ".join([f"{k}: {v}" for k, v in legenda.items()])
            label_legenda = ctk.CTkLabel(
                container,
                text=f"📖 {legenda_str}",
                font=ctk.CTkFont(size=13, weight="bold", slant="italic"),
                text_color="#1a73e8",
                anchor="w"
            )
            label_legenda.pack(side="left")
    
    def criar_frame_resposta(self, parent):
        frame_resposta = ctk.CTkFrame(parent)
        frame_resposta.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        frame_resposta.grid_columnconfigure(0, weight=1)
        
        # ✅ GUARDAR REFERÊNCIA para poder recriá-lo depois
        self.frame_resposta = frame_resposta
        
        # Título da seção
        frame_titulo = ctk.CTkFrame(frame_resposta, fg_color="transparent")
        frame_titulo.grid(row=0, column=0, sticky="ew", padx=15, pady=(10, 5))
        label_titulo = ctk.CTkLabel(
            frame_titulo, 
            text="✏️ Sua Resposta", 
            font=ctk.CTkFont(size=16, weight="bold"), 
            anchor="w"
        )
        label_titulo.pack(side="left")

        # ✅ VERIFICAÇÃO MELHORADA: Garantir que questões existem
        if not hasattr(self, 'questoes') or not self.questoes or self.questao_idx >= len(self.questoes):
            temp_label = ctk.CTkLabel(frame_resposta, text="Carregando questão...")
            temp_label.grid(row=1, column=0, pady=50)
            return

        # Inicializar variáveis
        questao_atual = self.questoes[self.questao_idx]
        self.campos_resposta = {}
        self.teclados_logicos = {}
        self.campos_passos = []
        tipo_questao = questao_atual.get("tipo", "simbolica")
        
        # ✅ ATUALIZAR TIPO ATUAL
        self.tipo_questao_atual = tipo_questao
        
        current_row = 1

        # ✅ CORREÇÃO: Só criar campos de tradução se for questão de tradução
        if tipo_questao == "traducao":
            frame_traducao = ctk.CTkFrame(frame_resposta)
            frame_traducao.grid(row=current_row, column=0, sticky="ew", padx=15, pady=5)
            frame_traducao.grid_columnconfigure(1, weight=1)
            
            # S1
            label_s1 = ctk.CTkLabel(frame_traducao, text="Tradução S1:", font=ctk.CTkFont(size=14, weight="bold"))
            label_s1.grid(row=0, column=0, sticky="w", padx=5, pady=5)
            self.campos_resposta['s1'] = ctk.CTkTextbox(frame_traducao, height=40, font=ctk.CTkFont(size=14))
            self.campos_resposta['s1'].grid(row=0, column=1, sticky="ew", padx=5, pady=5)
            self.teclados_logicos['s1'] = TecladoLogico(frame_traducao, self.campos_resposta['s1'])
            self.teclados_logicos['s1'].grid(row=0, column=2, padx=5, pady=5)
            
            # S2
            label_s2 = ctk.CTkLabel(frame_traducao, text="Tradução S2:", font=ctk.CTkFont(size=14, weight="bold"))
            label_s2.grid(row=1, column=0, sticky="w", padx=5, pady=5)
            self.campos_resposta['s2'] = ctk.CTkTextbox(frame_traducao, height=40, font=ctk.CTkFont(size=14))
            self.campos_resposta['s2'].grid(row=1, column=1, sticky="ew", padx=5, pady=5)
            self.teclados_logicos['s2'] = TecladoLogico(frame_traducao, self.campos_resposta['s2'])
            self.teclados_logicos['s2'].grid(row=1, column=2, padx=5, pady=5)
            
            # Vincular foco
            self.campos_resposta['s1'].bind("<FocusIn>", 
                lambda e: setattr(self.teclados_logicos['s1'], 'campo_destino', self.campos_resposta['s1']))
            self.campos_resposta['s2'].bind("<FocusIn>", 
                lambda e: setattr(self.teclados_logicos['s2'], 'campo_destino', self.campos_resposta['s2']))
            
            current_row += 1

        # === SEÇÃO DE PASSOS ===
        # Label + teclado + botão adicionar
        frame_label_passos = ctk.CTkFrame(frame_resposta, fg_color="transparent")
        frame_label_passos.grid(row=current_row, column=0, sticky="ew", padx=15, pady=(10, 5))
        frame_label_passos.grid_columnconfigure(0, weight=0)  # Label (tamanho fixo)
        frame_label_passos.grid_columnconfigure(1, weight=1)  # Espaço flexível no meio
        frame_label_passos.grid_columnconfigure(2, weight=0)  # Teclado (tamanho fixo)
        frame_label_passos.grid_columnconfigure(3, weight=0)  # Botão (tamanho fixo)
        
        label_passos = ctk.CTkLabel(
            frame_label_passos, 
            text="📝 Demonstre a equivalência passo a passo:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label_passos.grid(row=0, column=0, sticky="w", padx=(0, 10))

        self.teclado_passos_principal = TecladoLogico(frame_label_passos, None)
        self.teclado_passos_principal.grid(row=0, column=2, padx=10)
        
        self.btn_add_passo = ctk.CTkButton(
            frame_label_passos,
            text="+ Adicionar Passo",
            width=120,
            height=28,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.adicionar_linha_passos
        )
        self.btn_add_passo.grid(row=0, column=3, sticky="e", padx=(10, 0))
        
        current_row += 1

        # === ÁREA DE PASSOS + BOTÃO ENVIAR ===
        frame_passos_principal = ctk.CTkFrame(frame_resposta)
        frame_passos_principal.grid(row=current_row, column=0, sticky="nsew", padx=15, pady=5)
        
        frame_passos_principal.grid_columnconfigure(0, weight=3)
        frame_passos_principal.grid_columnconfigure(1, weight=1)  
        frame_passos_principal.grid_rowconfigure(0, weight=1)
        frame_resposta.grid_rowconfigure(current_row, weight=1) 
        
        # === Passos ===
        passos_container = ctk.CTkFrame(frame_passos_principal)
        passos_container.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)
        
        # Canvas + Scrollbar
        self.canvas_passos = ctk.CTkCanvas(passos_container, height=250)
        self.canvas_passos.pack(side="left", fill="both", expand=True)
        
        scrollbar = ctk.CTkScrollbar(passos_container, orientation="vertical", command=self.canvas_passos.yview)
        scrollbar.pack(side="right", fill="y")
        
        self.canvas_passos.configure(yscrollcommand=scrollbar.set, highlightthickness=0, borderwidth=0)
        
        # Frame interno para os passos
        self.frame_passos = ctk.CTkFrame(self.canvas_passos)
        self.frame_passos.bind(
            "<Configure>",
            lambda e: self.canvas_passos.configure(scrollregion=self.canvas_passos.bbox("all"))
        )
        
        self.canvas_window = self.canvas_passos.create_window((0, 0), window=self.frame_passos, anchor="nw")
        
        # Ajustar largura do frame interno
        def configure_frame_width(event):
            canvas_width = event.width
            self.canvas_passos.itemconfig(self.canvas_window, width=max(canvas_width - 20, 1))
        
        self.canvas_passos.bind('<Configure>', configure_frame_width)

        # === FRAME LATERAL (Apenas para o botão Enviar) ===
        frame_botao_lateral = ctk.CTkFrame(frame_passos_principal)
        frame_botao_lateral.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        frame_botao_lateral.grid_columnconfigure(0, weight=1)
        
        frame_botao_lateral.grid_rowconfigure(0, weight=1) 
        frame_botao_lateral.grid_rowconfigure(1, weight=0) 

        self.btn_enviar = ctk.CTkButton(
            frame_botao_lateral,
            text="📤 Enviar Resposta",
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.processar_resposta
        )
        # Posicionado na parte de baixo do frame lateral
        self.btn_enviar.grid(row=1, column=0, sticky="sew", padx=10, pady=(0, 10))

        # Adicionar primeiro passo
        if not hasattr(self, 'campos_passos') or not self.campos_passos:
            self.adicionar_linha_passos()

    def adicionar_linha_passos(self):
        # Criar numeração do passo
        numero_passo = len(self.campos_passos) + 1
        
        # Frame para este passo
        frame_passo = ctk.CTkFrame(self.frame_passos, fg_color="transparent")
        frame_passo.pack(fill="x", padx=5, pady=3)
        
        # Label do número
        label_num = ctk.CTkLabel(
            frame_passo, 
            text=f"{numero_passo}.", 
            font=ctk.CTkFont(size=14, weight="bold"),
            width=25
        )
        label_num.pack(side="left", padx=(0, 5))
        
        # Campo de texto
        campo = ctk.CTkTextbox(frame_passo, height=45, font=ctk.CTkFont(size=14))
        campo.pack(side="left", fill="x", expand=True)
        
        # Botão remover (se não for o primeiro)
        if numero_passo > 1:
            btn_remove = ctk.CTkButton(
                frame_passo,
                text="✕",
                width=30,
                height=30,
                font=ctk.CTkFont(size=12),
                fg_color="red",
                hover_color="darkred",
                command=lambda: self.remover_passo(frame_passo, campo)
            )
            btn_remove.pack(side="right", padx=(5, 0))
        
        self.campos_passos.append(campo)
        
        # Vincular foco ao teclado
        def on_focus_in(event, campo=campo):
            self.teclado_passos_principal.campo_destino = campo
        
        campo.bind("<FocusIn>", on_focus_in)
        
        # Atualizar scroll e focar
        self.frame_passos.update_idletasks()
        self.canvas_passos.yview_moveto(1.0)
        campo.focus_set()

        self.teclado_passos_principal.campo_destino = campo

    def remover_passo(self, frame_passo, campo):
        """Remove um passo específico"""
        if len(self.campos_passos) <= 1:
            messagebox.showwarning("Aviso", "Deve haver pelo menos um passo!")
            return
        
        # Remover da lista e destruir widgets
        self.campos_passos.remove(campo)
        frame_passo.destroy()
        
        # Renumerar os passos restantes
        self.renumerar_passos()

    def renumerar_passos(self):
        """Renumera os labels dos passos após remoção"""
        for i, frame in enumerate(self.frame_passos.winfo_children()):
            if hasattr(frame, 'winfo_children'):
                children = frame.winfo_children()
                if children and isinstance(children[0], ctk.CTkLabel):
                    children[0].configure(text=f"{i + 1}.")

    def get_lista_passos(self):
        return [campo.get("1.0", "end-1c").strip() for campo in self.campos_passos if campo.get("1.0", "end-1c").strip()]

    def limpar_passos(self):
        for campo in self.campos_passos:
            campo.destroy()
        self.campos_passos.clear()
        # Limpar também todos os frames de passo
        for widget in self.frame_passos.winfo_children():
            widget.destroy()
        self.adicionar_linha_passos()

    def criar_frame_assistente(self, parent):
        frame_assistente = ctk.CTkFrame(parent)
        frame_assistente.grid(row=3, column=0, sticky="ew", padx=10, pady=10)
        frame_assistente.grid_columnconfigure(0, weight=1)
        frame_assistente.grid_columnconfigure(1, weight=1)
        
        # Título
        label_titulo = ctk.CTkLabel(
            frame_assistente, 
            text="🤖 Assistente IA e Dicas", 
            font=ctk.CTkFont(size=16, weight="bold"), 
            anchor="w"
        )
        label_titulo.grid(row=0, column=0, columnspan=2, sticky="ew", padx=15, pady=(10, 5))
        
        # Área de chat
        self.area_chat = ctk.CTkTextbox(
            frame_assistente, 
            height=100, 
            font=ctk.CTkFont(size=12), 
            wrap="word"
        )
        self.area_chat.grid(row=1, column=0, columnspan=2, sticky="ew", padx=15, pady=5)
        self.area_chat.insert("1.0", "💡 Peça uma dica se precisar de ajuda!\n")
        self.area_chat.configure(state="disabled")
        
        # Contadores
        self.label_contador_dicas_fixas = ctk.CTkLabel(
            frame_assistente, 
            text="", 
            font=ctk.CTkFont(size=11, slant="italic"), 
            text_color="#1a73e8"
        )
        self.label_contador_dicas_fixas.grid(row=2, column=0, sticky="w", padx=15, pady=(5, 0))
        
        self.label_contador_dicas_llm = ctk.CTkLabel(
            frame_assistente, 
            text="", 
            font=ctk.CTkFont(size=11, slant="italic"), 
            text_color="#1a73e8"
        )
        self.label_contador_dicas_llm.grid(row=2, column=1, sticky="w", padx=15, pady=(5, 0))
        
        # Botões de dicas
        self.btn_dica_fixa = ctk.CTkButton(
            frame_assistente, 
            text="💡 Ver Dica Fixa", 
            command=self.pedir_dica_fixa,
            height=35
        )
        self.btn_dica_fixa.grid(row=3, column=0, padx=15, pady=10, sticky="ew")
        
        self.btn_dica_llm = ctk.CTkButton(
            frame_assistente, 
            text="🤖 Pedir Dica à IA", 
            command=self.pedir_dica_llm,
            height=35
        )
        self.btn_dica_llm.grid(row=3, column=1, padx=15, pady=10, sticky="ew")
        
        self.atualizar_contadores_dicas()

    def _buscar_dicas_fixas(self, questao_atual):
        dicas = []
        if 'dicas_fixas' in questao_atual:
            dicas = questao_atual['dicas_fixas']
        elif 'dica_fixa' in questao_atual:
            dicas = [questao_atual['dica_fixa']]
        else:
            i = 1
            while True:
                key = f'dica{i}'
                if key in questao_atual:
                    dicas.append(questao_atual[key])
                    i += 1
                else:
                    break
        return dicas

    def pedir_dica_fixa(self):
        questao_atual = self.questoes[self.questao_idx]
        dicas = self._buscar_dicas_fixas(questao_atual)
        total_fixas = len(dicas)
        if self.dicas_fixas_usadas >= total_fixas or total_fixas == 0:
            messagebox.showinfo("Limite de dicas", "Você já usou todas as dicas fixas disponíveis para esta questão.")
            return
        dica = dicas[self.dicas_fixas_usadas]
        self.dicas_fixas_usadas += 1
        self.area_chat.configure(state="normal")
        self.area_chat.insert("end", f"\n💡 Dica Fixa: {dica}\n")
        self.area_chat.see("end")
        self.area_chat.configure(state="disabled")
        self.atualizar_contadores_dicas()

    def pedir_dica_llm(self):
        questao_atual = self.questoes[self.questao_idx]
        id_questao = questao_atual.get("id", self.questao_idx)
        total_llm = 3
        usos_nesta_questao = self.dicas_llm_por_questao.get(id_questao, 0)
        if usos_nesta_questao >= total_llm:
            messagebox.showinfo("Limite de dicas IA", "Você já usou todas as dicas IA disponíveis para esta questão.")
            return
        self._abrir_modal_pergunta_ia()

    def _abrir_modal_pergunta_ia(self):
        modal = ctk.CTkToplevel(self.window)
        modal.title("Pedir Dica à IA")
        modal.geometry("400x220")
        modal.grab_set()
        modal.focus_set()
        
        label = ctk.CTkLabel(modal, text="Digite sua dúvida ou deixe em branco para uma dica geral:", font=ctk.CTkFont(size=13))
        label.pack(pady=(20, 10), padx=10)
        entry = ctk.CTkTextbox(modal, height=60, font=ctk.CTkFont(size=13))
        entry.pack(fill="x", padx=10)
        
        def enviar():
            pergunta = entry.get("1.0", "end-1c").strip()
            modal.destroy()
            self._enviar_pergunta_llm(pergunta)
            
        btn = ctk.CTkButton(modal, text="Enviar", command=enviar)
        btn.pack(pady=15)
        entry.focus_set()

    def atualizar_contadores_dicas(self):
        questao_atual = self.questoes[self.questao_idx]
        dicas = self._buscar_dicas_fixas(questao_atual)
        total_fixas = len(dicas)
        self.label_contador_dicas_fixas.configure(text=f"Dicas fixas: {self.dicas_fixas_usadas}/{total_fixas}")
        total_llm = 3
        usadas_llm = self.dicas_llm_por_questao.get(questao_atual.get('id', self.questao_idx), 0)
        self.label_contador_dicas_llm.configure(text=f"Dicas IA: {usadas_llm}/{total_llm}")
        
        # Desabilita botões se atingir limite
        if self.dicas_fixas_usadas >= total_fixas or total_fixas == 0:
            self.btn_dica_fixa.configure(state="disabled")
        else:
            self.btn_dica_fixa.configure(state="normal")
        if usadas_llm >= total_llm:
            self.btn_dica_llm.configure(state="disabled")
        else:
            self.btn_dica_llm.configure(state="normal")

    # ✅ NOVO MÉTODO: Recria a interface quando o tipo muda
    def _recriar_frame_resposta(self):
        """Recria completamente o frame de resposta quando o tipo de questão muda"""
        print(f"🔄 Recriando frame de resposta para tipo: {self.tipo_questao_atual}")
        
        # Destruir frame de resposta atual
        if hasattr(self, 'frame_resposta') and self.frame_resposta.winfo_exists():
            self.frame_resposta.destroy()
        
        # Recriar o frame de resposta
        self.criar_frame_resposta(self.frame_principal)
        print("✅ Frame de resposta recriado com sucesso")

    def carregar_proxima_questao(self):
        if self.timer_id:
            self.window.after_cancel(self.timer_id)

        if self.questao_idx >= len(self.questoes):
            self.finalizar_nivel()
            return

        # Resetar estado para a nova questão
        self.erros_tentativa_atual = 0
        self.dicas_fixas_usadas = 0

        # ✅ NOVO: Verificar se mudou o tipo de questão
        questao_atual = self.questoes[self.questao_idx]
        tipo_atual = questao_atual.get("tipo", "simbolica")
        
        # Se tipo mudou, recriar interface de resposta
        if self.tipo_questao_atual != tipo_atual:
            print(f"🔄 Tipo mudou de '{self.tipo_questao_atual}' para '{tipo_atual}' - Recriando interface")
            self.tipo_questao_atual = tipo_atual
            self._recriar_frame_resposta()
        
        # Limpar campos existentes (se existirem após recreação)
        if hasattr(self, 'campos_resposta'):
            for campo in self.campos_resposta.values():
                campo.delete("1.0", "end")
        if hasattr(self, 'limpar_passos'):
            self.limpar_passos()
        if hasattr(self, 'area_chat'):
            self.area_chat.configure(state="normal")
            self.area_chat.delete("1.0", "end")
            self.area_chat.insert("1.0", "💡 Peça uma dica se precisar de ajuda!")
            self.area_chat.configure(state="disabled")

        if hasattr(self, 'btn_dica_fixa') and hasattr(self, 'btn_dica_llm'):
            self.btn_dica_fixa.configure(state="normal")
            self.btn_dica_llm.configure(state="normal")
        
        # Carregar dados da questão
        enunciado = questao_atual.get("enunciado", questao_atual.get("pergunta", "[Sem enunciado]"))

        if hasattr(self, 'texto_pergunta'):
            self.texto_pergunta.configure(state="normal")
            self.texto_pergunta.delete("1.0", "end")
            self.texto_pergunta.insert("1.0", enunciado)
            self.texto_pergunta.configure(state="disabled")
        
        # Atualizar tópico e legenda
        if hasattr(self, 'atualizar_topico_legenda'):
            self.atualizar_topico_legenda()
        
        # Atualizar contadores
        if hasattr(self, 'label_contador_questoes'):
            self.label_contador_questoes.configure(text=f"Questão {self.questao_idx + 1}/{len(self.questoes)}")
        if hasattr(self, 'atualizar_contadores_dicas'):
            self.atualizar_contadores_dicas()
        
        # Iniciar timer
        self.start_time = time.time()
        self.atualizar_timer()

    def atualizar_timer(self):
        if self.start_time is None:
            return
        elapsed_seconds = int(time.time() - self.start_time)
        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60
        self.label_timer.configure(text=f"Tempo: {minutes:02d}:{seconds:02d}")
        self.timer_id = self.window.after(1000, self.atualizar_timer)

    def _avaliar_traducao_correta(self, avaliacao_texto):
        """✅ MÉTODO ROBUSTO: Avalia se a tradução foi considerada correta pela API"""
        if not avaliacao_texto or not avaliacao_texto.strip():
            return False
        
        # Normalizar texto: minúsculo, sem acentos e pontuações
        import re
        texto_normalizado = re.sub(r'[^\w\s]', '', str(avaliacao_texto).lower().strip())
        
        # Padrões que indicam INCORRETO (verificar primeiro - mais específicos)
        padroes_incorreto = [
            'incorreto',
            'incorreta', 
            'incorretas',
            'incorretos',
            'nao esta correta',
            'nao estao corretas',
            'nao esta correto',
            'nao estao corretos',
            'traducao incorreta',
            'traducoes incorretas',
            'traducao esta incorreta',
            'traducoes estao incorretas',
            'erro na traducao',
            'erros na traducao',
            'traducao errada',
            'traducoes erradas'
        ]
        
        # Verificar primeiro os padrões incorretos
        for padrao in padroes_incorreto:
            if padrao in texto_normalizado:
                return False
        
        # Padrões que indicam CORRETO
        padroes_correto = [
            'correto',
            'correta',
            'corretas', 
            'corretos',
            'traducao correta',
            'traducoes corretas',
            'traducao esta correta',
            'traducoes estao corretas',
            'esta correta',
            'estao corretas',
            'esta correto',
            'estao corretos',
            'bem traduzida',
            'bem traduzidas',
            'adequada',
            'adequadas',
            'apropriada',
            'apropriadas'
        ]
        
        # Verificar padrões corretos
        for padrao in padroes_correto:
            if padrao in texto_normalizado:
                return True
        
        # Se não encontrou nenhum padrão claro, assumir incorreto como padrão seguro
        return False

    def processar_resposta(self):
        questao_atual = self.questoes[self.questao_idx]
        tipo_questao = questao_atual.get("tipo")
        respostas = {campo: widget.get("1.0", "end-1c").strip() for campo, widget in self.campos_resposta.items()}
        lista_passos = self.get_lista_passos()
        
        # Validações básicas
        if tipo_questao == "traducao":
            if not respostas.get('s1') or not respostas.get('s2'):
                messagebox.showwarning("Aviso", "Preencha as traduções de S1 e S2.")
                return
        if not lista_passos:
            messagebox.showwarning("Aviso", "Adicione pelo menos um passo para demonstrar a equivalência.")
            return

        tempo_gasto = time.time() - self.start_time
        if self.timer_id:
            self.window.after_cancel(self.timer_id)
            self.timer_id = None

        # Determinar expressões para avaliação dos passos
        if tipo_questao == "traducao":
            expr_inicial = respostas.get('s1', '')
            expr_objetivo = respostas.get('s2', '') 
        else:
            expr_inicial = questao_atual.get('expressao_s1', '')
            expr_objetivo = questao_atual.get('expressao_s2', '')

        # Avaliação dos passos (interno)
        try:
            if 'return_regras' in avaliar_passos.__code__.co_varnames:
                resultado_passos, detalhes_passos, erros, historico = avaliar_passos(lista_passos, expr_inicial, expr_objetivo, return_regras=True)
            else:
                resultado_passos, detalhes_passos, erros, historico = avaliar_passos(lista_passos, expr_inicial, expr_objetivo)
        except Exception as e:
            resultado_passos = False
            detalhes_passos = []
            erros = [f"Erro na avaliação: {str(e)}"]
            historico = []

        # Organizar dados da avaliação dos passos
        avaliacao_passos = {
            'resultado': resultado_passos,
            'detalhes': detalhes_passos,
            'erros': erros,
            'historico': historico
        }

        # Avaliação da tradução (OpenRouter) - apenas para questões de tradução
        avaliacao_traducao = None
        if tipo_questao == "traducao":
            try:
                gabarito_s1 = questao_atual.get('gabarito_traducao_s1', '')
                gabarito_s2 = questao_atual.get('gabarito_traducao_s2', '')

                avaliacao_traducao = avaliar_traducao_logica(
                    questao_atual.get('enunciado', ''),
                    f"S1: {respostas.get('s1', '')} | S2: {respostas.get('s2', '')}",
                    f"S1: {gabarito_s1} | S2: {gabarito_s2}"
                )
                print(f"Resposta da API de tradução: '{avaliacao_traducao}'")
            except Exception as e:
                avaliacao_traducao = f"[ERRO ao avaliar tradução: {e}]"
                print(f"Erro na avaliação da tradução: {e}")

        # Explicação natural do Gemini
        try:
            prompt_gemini = "Você é um tutor especializado em lógica proposicional. Explique de forma didática e detalhada o resultado da avaliação.\n\n"
            
            if tipo_questao == "traducao":
                prompt_gemini += "=== QUESTÃO DE TRADUÇÃO ===\n"
                prompt_gemini += f"ENUNCIADO ORIGINAL: {questao_atual.get('enunciado', '')}\n\n"
                prompt_gemini += f"TRADUÇÃO DO ALUNO:\n"
                prompt_gemini += f"S1: {respostas.get('s1', '')}\n"
                prompt_gemini += f"S2: {respostas.get('s2', '')}\n\n"
                prompt_gemini += f"AVALIAÇÃO DA TRADUÇÃO: {avaliacao_traducao}\n\n"
                prompt_gemini += f"PASSOS DE EQUIVALÊNCIA:\n{chr(10).join(lista_passos)}\n\n"
                prompt_gemini += f"RESULTADO DOS PASSOS: {'✅ CORRETO' if resultado_passos else '❌ INCORRETO'}\n\n"
                
                if not resultado_passos and erros:
                    prompt_gemini += f"ERROS IDENTIFICADOS:\n{chr(10).join(erros)}\n\n"
                
                prompt_gemini += "INSTRUÇÕES:\n"
                prompt_gemini += "1. Avalie DETALHADAMENTE se as traduções S1 e S2 estão corretas\n"
                prompt_gemini += "2. Explique os ERROS de tradução (se houver) e como corrigi-los\n"
                prompt_gemini += "3. Avalie se os passos de equivalência estão corretos\n"
                prompt_gemini += "4. Explique os ERROS nos passos (se houver) e sugira correções\n"
                prompt_gemini += "5. Dê dicas sobre como traduzir corretamente do português para lógica proposicional\n"
                prompt_gemini += "6. Seja específico sobre quais conectivos usar (∧, ∨, →, ¬, ↔)\n\n"
            else:
                prompt_gemini += "=== QUESTÃO SIMBÓLICA ===\n"
                prompt_gemini += f"EXPRESSÕES DADAS:\n"
                prompt_gemini += f"S1: {questao_atual.get('expressao_s1', '')}\n"
                prompt_gemini += f"S2: {questao_atual.get('expressao_s2', '')}\n\n"
                prompt_gemini += f"PASSOS DO ALUNO:\n{chr(10).join(lista_passos)}\n\n"
                prompt_gemini += f"RESULTADO: {'✅ CORRETO' if resultado_passos else '❌ INCORRETO'}\n\n"
                
                if not resultado_passos and erros:
                    prompt_gemini += f"ERROS IDENTIFICADOS:\n{chr(10).join(erros)}\n\n"
                
                prompt_gemini += "INSTRUÇÕES:\n"
                prompt_gemini += "1. Avalie cada passo da demonstração de equivalência\n"
                prompt_gemini += "2. Identifique quais regras de equivalência foram aplicadas corretamente\n"
                prompt_gemini += "3. Explique DETALHADAMENTE os erros (se houver) e como corrigi-los\n"
                prompt_gemini += "4. Sugira os próximos passos corretos para completar a demonstração\n"
                prompt_gemini += "5. Mencione regras como: De Morgan, Distributiva, Comutativa, Associativa, etc.\n\n"
            
            prompt_gemini += "Seja claro, educativo e incentive o aprendizado. Use exemplos quando necessário."
            
            explicacao_gemini = obter_explicacao_avaliacao(prompt_gemini)
        except Exception as e:
            explicacao_gemini = f"[ERRO ao gerar explicação: {e}]"

        # Preparar dados para o modal de avaliação
        if tipo_questao == "traducao":
            gabarito_s1 = questao_atual.get('gabarito_traducao_s1', "Não disponível")
            gabarito_s2 = questao_atual.get('gabarito_traducao_s2', "Não disponível")
            gabarito_equivalencia = questao_atual.get('gabarito_equivalencia', "Não disponível")
            exemplo_caminho = questao_atual.get('exemplo_caminho', "Não disponível")
            resposta_aluno_str = f"S1: {respostas.get('s1', '')}\nS2: {respostas.get('s2', '')}\nPassos:\n" + "\n".join(lista_passos)
            gabarito = f"S1: {gabarito_s1}\nS2: {gabarito_s2}\nEquivalência: {gabarito_equivalencia}\nExemplo de caminho: {exemplo_caminho}"
        else:  # simbolica
            resposta_aluno_str = f"S1: {questao_atual.get('expressao_s1', '')}\nS2: {questao_atual.get('expressao_s2', '')}\nPassos:\n" + "\n".join(lista_passos)
            gabarito = f"S1: {questao_atual.get('expressao_s1', '')}\nS2: {questao_atual.get('expressao_s2', '')}\nExemplo de caminho: {questao_atual.get('exemplo_caminho', 'Não disponível')}"

        avaliacao_detalhada = {
            "resposta_aluno": resposta_aluno_str,
            "avaliador_interno": "\n".join(avaliacao_passos['historico']) if avaliacao_passos['historico'] else "Nenhum histórico disponível",
            "avaliacao_llm": str(avaliacao_traducao) if tipo_questao == "traducao" else None,
            "explicacao_natural": explicacao_gemini,
            "gabarito": gabarito
        }

        # === Lógica de Decisão ===
        traducao_correta = False
        acertou = False
        
        if tipo_questao == "traducao":
            
            traducao_correta = self._avaliar_traducao_correta(avaliacao_traducao)
            
            passos_corretos = resultado_passos

            if traducao_correta and passos_corretos:
                acertou = True
                print("Tradução e passos corretos!")
            elif traducao_correta and not passos_corretos:
                acertou = False
                print("Tradução correta, mas passos incorretos!")
            elif not traducao_correta and passos_corretos:
                acertou = False
                print("Tradução incorreta, mas passos corretos!")
            else:
                acertou = False
                print("Tradução e passos incorretos!")
        
        else:
            # Para questões simbólicas: só precisa dos passos corretos
            acertou = resultado_passos
            print(f"Questão simbólica - Passos corretos: {acertou}")

        # Registro no perfil
        id_questao = questao_atual.get('id', str(self.questao_idx))
        tempo_limite = NIVEIS_CONFIG.get(str(self.nivel), {}).get('tempo_limite_por_questao', 300)

        erros_para_registro = self.erros_tentativa_atual
        if not acertou:
            erros_para_registro = max(1, self.erros_tentativa_atual)
        
        if tipo_questao == "traducao":
            resposta_final = f"S1: {respostas.get('s1', '')}\nS2: {respostas.get('s2', '')}\nPassos:\n" + "\n".join(lista_passos)
        else:
            resposta_final = "Passos:\n" + "\n".join(lista_passos)

        try:
            registrar_questao(
                self.nivel,
                id_questao,
                tempo_gasto,
                erros_para_registro,
                self.dicas_fixas_usadas,
                self.dicas_llm_por_questao.get(id_questao, 0),
                tempo_limite,
                acertou,
                resposta_final,
                self.perfil_path
            )
        except Exception as e:
            print(f"Erro ao registrar questão: {e}")

        # Função para avançar questão
        def avancar_questao():
            self.questao_idx += 1
            self.carregar_proxima_questao()

        # Abrir modal de avaliação
        try:
             ModalAvaliacao(self.window, avaliacao_detalhada, on_close=avancar_questao)
        except Exception as e:
            print(f"Erro ao abrir modal de avaliação: {e}")
            avancar_questao() # Avança manualmente

    def _enviar_pergunta_llm(self, pergunta_aluno):
        questao_atual = self.questoes[self.questao_idx]
        id_questao = questao_atual.get("id", self.questao_idx)
        usos_nesta_questao = self.dicas_llm_por_questao.get(id_questao, 0)
        
        self.btn_dica_llm.configure(text="Aguarde...", state="disabled")
        self.window.update_idletasks()
        
        questao_tipo = questao_atual.get("tipo", "simbolica")
        if questao_tipo == "traducao":
            s1 = self.campos_resposta['s1'].get('1.0', 'end-1c').strip() if 's1' in self.campos_resposta else ""
            s2 = self.campos_resposta['s2'].get('1.0', 'end-1c').strip() if 's2' in self.campos_resposta else ""
            passos = self.get_lista_passos()
            resposta_aluno = f"S1: {s1}\nS2: {s2}\nPassos: {', '.join(passos) if passos else 'Nenhum passo ainda'}"
        else:
            passos = self.get_lista_passos()
            resposta_aluno = f"Passos: {', '.join(passos) if passos else 'Nenhum passo ainda'}"

        enunciado = questao_atual.get("enunciado", questao_atual.get("pergunta", "[Sem enunciado]"))
        pergunta_contexto = f"{enunciado}\n\n{pergunta_aluno}" if pergunta_aluno else enunciado

        try:
            dica = obter_dica_gemini(pergunta_contexto, resposta_aluno)
            self.area_chat.configure(state="normal")
            self.area_chat.insert("end", f"\n🤖 IA: {dica}\n")
            self.area_chat.see("end")
            self.area_chat.configure(state="disabled")
            
            # Atualizar contador
            self.dicas_llm_por_questao[id_questao] = usos_nesta_questao + 1
            self.atualizar_contadores_dicas()
            
        except Exception as e:
            self.area_chat.configure(state="normal")
            self.area_chat.insert("end", f"\n❌ Erro ao obter dica: {e}\n")
            self.area_chat.see("end")
            self.area_chat.configure(state="disabled")
        finally:
            self.btn_dica_llm.configure(text="🤖 Pedir Dica à IA", state="normal")

    def finalizar_nivel(self):
        """Finaliza o nível atual e mostra o modal de conclusão"""
        if self.timer_id:
            self.window.after_cancel(self.timer_id)

        # Processar conclusão do nível  
        processar_conclusao_de_nivel(self.nivel, self.perfil_path)
        
        # Fechar janela atual primeiro
        self.window.destroy()
        
        # Abrir modal de final de nível
        ModalFinalNivel(self.parent, self.nivel, self.perfil_path, self.app_instance)