import customtkinter as ctk
from tkinter import messagebox, filedialog, Scrollbar, Text, RIGHT, Y, END
import tkinter as tk
import os
import importlib.util
from src.config import MAIN_WINDOW, PERFIS_PATH
from src.utils import centralizar_janela
from src.perfil.perfil import criar_perfil, carregar_perfil, salvar_perfil

class MainWindow:
    def __init__(self, on_iniciar_callback):
        self.on_iniciar_callback = on_iniciar_callback
        self.perfil = None  # Perfil carregado em memória
        self.perfil_path = None  # Inicializar como None
        self.root = ctk.CTk()
        self.root.title("Tutor de Lógica")
        # Tela cheia por padrão
        self.root.state('zoomed')
        self.root.resizable(True, True)
        self.criar_interface()

    def criar_interface(self):
        """Cria a interface da tela principal"""
        # Frame principal ocupa toda a tela
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(expand=True, fill="both", padx=0, pady=0)
        
        # Título
        titulo = ctk.CTkLabel(
            main_frame,
            text="Tutor de Lógica",
            font=ctk.CTkFont(size=44, weight="bold")
        )
        titulo.pack(pady=(30, 10))
        
        # Subtítulo
        subtitulo = ctk.CTkLabel(
            main_frame,
            text="Aprenda lógica de forma interativa e personalizada",
            font=ctk.CTkFont(size=20)
        )
        subtitulo.pack(pady=(0, 30))
        
        # Container para botões centralizado
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=(0, 0))

        # Botão Iniciar
        btn_iniciar = ctk.CTkButton(
            btn_frame,
            text="Iniciar",
            font=ctk.CTkFont(size=22, weight="bold"),
            width=280,
            height=60,
            command=self.fluxo_inicial
        )
        btn_iniciar.pack(pady=(0, 12))

        # Botão Manual de Regras
        btn_manual = ctk.CTkButton(
            btn_frame,
            text="📖 Manual de Regras",
            font=ctk.CTkFont(size=18, weight="bold"),
            width=280,
            height=44,
            command=lambda: self.mostrar_manual_regras(self.root)
        )
        btn_manual.pack(pady=(0, 8))

        # === SEÇÃO DE GRÁFICOS ===
        
        # Frame para gráficos
        graficos_frame = ctk.CTkFrame(btn_frame, fg_color="transparent")
        graficos_frame.pack(pady=(10, 0))
        
        # Título da seção
        label_graficos = ctk.CTkLabel(
            graficos_frame,
            text="📊 Análise de Desempenho",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        label_graficos.pack(pady=(0, 8))

        # 1. Status dos Níveis
        btn_grafico_niveis = ctk.CTkButton(
            graficos_frame,
            text="🎯 Status dos Níveis",
            font=ctk.CTkFont(size=15),
            width=280,
            height=38,
            command=self.abrir_grafico_status_niveis
        )
        btn_grafico_niveis.pack(pady=(0, 6))

        # 2. Progresso por Nível
        btn_grafico_progresso = ctk.CTkButton(
            graficos_frame,
            text="📈 Progresso por Nível",
            font=ctk.CTkFont(size=15),
            width=280,
            height=38,
            command=self.abrir_grafico_progresso_nivel
        )
        btn_grafico_progresso.pack(pady=(0, 6))

        # 3. Resumo Geral
        btn_grafico_resumo = ctk.CTkButton(
            graficos_frame,
            text="🕸️ Resumo Geral (Radar)",
            font=ctk.CTkFont(size=15),
            width=280,
            height=38,
            command=self.abrir_grafico_resumo_geral
        )
        btn_grafico_resumo.pack(pady=(0, 6))

        # 4. Desempenho por Conceito
        btn_grafico_conceitos = ctk.CTkButton(
            graficos_frame,
            text="🧠 Desempenho por Conceito",
            font=ctk.CTkFont(size=15),
            width=280,
            height=38,
            command=self.abrir_grafico_conceitos
        )
        btn_grafico_conceitos.pack(pady=(0, 6))

        # Botão Sair
        btn_sair = ctk.CTkButton(
            btn_frame,
            text="Sair",
            font=ctk.CTkFont(size=15),
            width=120,
            height=32,
            command=self.root.destroy
        )
        btn_sair.pack(pady=(20, 0))

    # === MÉTODOS DOS GRÁFICOS (CORRIGIDOS) ===
    
    def abrir_grafico_status_niveis(self):
        """Gráfico vertical de status dos níveis"""
        if not self.perfil_path:
            messagebox.showwarning("Aviso", "Perfil não carregado! Carregue um perfil primeiro.")
            return
            
        try:
            from src.perfil.graficos import grafico_status_niveis
            grafico_status_niveis(self.perfil_path)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar gráfico: {e}")

    def abrir_grafico_progresso_nivel(self):
        """Gráfico de barras das tentativas de um nível específico"""
        if not self.perfil_path:
            messagebox.showwarning("Aviso", "Perfil não carregado! Carregue um perfil primeiro.")
            return
            
        try:
            from src.perfil.graficos import grafico_progresso_nivel
            self._escolher_nivel_para_grafico(grafico_progresso_nivel)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar gráfico: {e}")

    def abrir_grafico_resumo_geral(self):
        """Gráfico radar com resumo de todos os níveis"""
        if not self.perfil_path:
            messagebox.showwarning("Aviso", "Perfil não carregado! Carregue um perfil primeiro.")
            return
            
        try:
            dados = carregar_perfil(self.perfil_path)
            if not dados or not dados.get("niveis"):
                messagebox.showwarning("Aviso", "Nenhum dado de nível encontrado no perfil!")
                return
                
            from src.perfil.graficos import grafico_resumo_geral
            grafico_resumo_geral(self.perfil_path)  # Passar perfil_path
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar gráfico: {e}")

    def abrir_grafico_conceitos(self):
        """Gráfico radar por conceitos/tópicos"""
        if not self.perfil_path:
            messagebox.showwarning("Aviso", "Perfil não carregado! Carregue um perfil primeiro.")
            return
            
        try:
            from src.perfil.graficos import grafico_por_conceito
            grafico_por_conceito(self.perfil_path)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar gráfico: {e}")

    def _escolher_nivel_para_grafico(self, funcao_grafico):
        """Modal para escolher qual nível analisar"""
        modal = ctk.CTkToplevel(self.root)
        modal.title("Escolher Nível")
        modal.geometry("300x200")
        modal.grab_set()
        modal.focus_set()
        
        # Centralizar
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 150
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 100
        modal.geometry(f"300x200+{x}+{y}")
        
        frame = ctk.CTkFrame(modal)
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        label = ctk.CTkLabel(frame, text="Escolha o nível para análise:", font=ctk.CTkFont(size=14, weight="bold"))
        label.pack(pady=(10, 15))
        
        # Botões dos níveis - CORRIGIDO para passar perfil_path
        for nivel in [1, 2, 3]:
            btn = ctk.CTkButton(
                frame,
                text=f"Nível {nivel}",
                width=200,
                command=lambda n=nivel: [modal.destroy(), funcao_grafico(n, self.perfil_path)]
            )
            btn.pack(pady=5)

    # === RESTO DOS MÉTODOS (INALTERADOS) ===
    
    def fluxo_inicial(self):
        resposta = messagebox.askyesno("Perfil", "Você já possui um perfil salvo (arquivo JSON)?")
        if resposta:
            self.anexar_perfil()
        else:
            self.cadastrar_perfil()

    def anexar_perfil(self):
        caminho = filedialog.askopenfilename(title="Selecione o arquivo de perfil JSON", filetypes=[("Arquivos JSON", "*.json")])
        if not caminho:
            return
        try:
            self.perfil = carregar_perfil(caminho)
            
            if self.perfil is None:
                messagebox.showerror("Erro", "Arquivo de perfil inválido ou corrompido!")
                return
                
            self.perfil_path = caminho
            messagebox.showinfo("Perfil carregado", f"Bem-vindo de volta, {self.perfil.get('nome', 'Usuário')}!")
            self.on_iniciar_callback("levels_selection", self.perfil, self.perfil_path)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar perfil: {e}")

    def cadastrar_perfil(self):
        self.janela_cadastro = ctk.CTkToplevel(self.root)
        self.janela_cadastro.title("Cadastro de Perfil")
        self.janela_cadastro.geometry(f"{MAIN_WINDOW['width']}x{MAIN_WINDOW['height']}")
        self.janela_cadastro.resizable(False, False)
        centralizar_janela(self.janela_cadastro, MAIN_WINDOW['width'], MAIN_WINDOW['height'])
        self.perguntas = [
            ("Qual seu nível de familiaridade com Lógica Proposicional?", [
                "Nunca estudei lógica proposicional.",
                "Já vi o básico (conectivos, tabelas-verdade), mas não pratiquei muito.",
                "Já estudei e resolvi exercícios de lógica proposicional."
            ]),
            ("Você já traduziu frases do português para símbolos com conectivos lógicos?", [
                "Nunca tentei traduzir frases para símbolos.",
                "Já tentei, mas tenho dificuldade.",
                "Consigo traduzir frases simples sem muita dificuldade."
            ]),
            ("Você já fez demonstrações lógicas usando regras de equivalência?", [
                "Nunca fiz demonstrações desse tipo.",
                "Já vi exemplos, mas não me sinto seguro.",
                "Já resolvi exercícios de equivalência lógica com aplicação de regras."
            ])
        ]
        self.respostas = [-1] * len(self.perguntas)
        self.pergunta_atual = 0
        self._mostrar_pergunta()

    def _mostrar_pergunta(self):
        for widget in self.janela_cadastro.winfo_children():
            widget.destroy()
        frame = ctk.CTkFrame(self.janela_cadastro)
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        if self.pergunta_atual == 0:
            label_nome = ctk.CTkLabel(frame, text="Digite seu nome:", font=ctk.CTkFont(size=16, weight="bold"))
            label_nome.pack(anchor="w", pady=(10, 5))
            self.entry_nome = ctk.CTkEntry(frame, font=ctk.CTkFont(size=15))
            self.entry_nome.pack(fill="x", pady=(0, 15))
            if hasattr(self, 'nome_usuario') and self.nome_usuario:
                self.entry_nome.insert(0, self.nome_usuario)
        label = ctk.CTkLabel(frame, text=f"{self.pergunta_atual+1}. {self.perguntas[self.pergunta_atual][0]}", font=ctk.CTkFont(size=15, weight="bold"))
        label.pack(anchor="w", pady=(10, 5))
        self.var = ctk.IntVar(value=self.respostas[self.pergunta_atual])
        for i, alt in enumerate(self.perguntas[self.pergunta_atual][1]):
            radio = ctk.CTkRadioButton(frame, text=alt, variable=self.var, value=i, font=ctk.CTkFont(size=13))
            radio.pack(anchor="w", padx=30)
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=15)
        if self.pergunta_atual > 0:
            btn_anterior = ctk.CTkButton(btn_frame, text="Anterior", width=100, command=self._anterior_pergunta)
            btn_anterior.pack(side="left", padx=5)
        btn_proximo = ctk.CTkButton(btn_frame, text="Próxima" if self.pergunta_atual < len(self.perguntas)-1 else "Finalizar", width=100, command=self._proxima_pergunta)
        btn_proximo.pack(side="right", padx=5)

    def _anterior_pergunta(self):
        self.respostas[self.pergunta_atual] = self.var.get()
        self.pergunta_atual -= 1
        self._mostrar_pergunta()

    def _proxima_pergunta(self):
        self.respostas[self.pergunta_atual] = self.var.get()
        if self.var.get() == -1:
            messagebox.showwarning("Atenção", "Por favor, selecione uma alternativa!")
            return
        if self.pergunta_atual == 0:
            nome = self.entry_nome.get().strip()
            if not nome:
                messagebox.showwarning("Atenção", "Por favor, digite seu nome!")
                return
            self.nome_usuario = nome
        if self.pergunta_atual < len(self.perguntas)-1:
            self.pergunta_atual += 1
            self._mostrar_pergunta()
        else:
            nome = getattr(self, 'nome_usuario', "")
            if not nome:
                messagebox.showwarning("Atenção", "Por favor, digite seu nome!")
                self.pergunta_atual = 0
                self._mostrar_pergunta()
                return
            
            try:
                base_dir = PERFIS_PATH
                os.makedirs(base_dir, exist_ok=True)
                
                arquivos = [f for f in os.listdir(base_dir) if f.startswith(nome)]
                novo_id = len(arquivos) + 1
                nome_arquivo = f"{nome}_ID{novo_id:03d}.json"
                caminho = os.path.join(base_dir, nome_arquivo)
                
                perfil = criar_perfil(nome, self.respostas, caminho)
                salvar_perfil(perfil, caminho)
                
                self.perfil = perfil
                self.perfil_path = caminho
                self.janela_cadastro.destroy()
                messagebox.showinfo("Perfil criado", f"Perfil criado com sucesso! Bem-vindo, {nome}.")
                self.on_iniciar_callback("levels_selection", self.perfil, self.perfil_path)
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao criar perfil: {e}")

    def mostrar_manual_regras(self, parent=None):
        """Exibe uma janela/modal com o resumo das regras lógicas formatadas de regras.py."""
        caminho_regras = os.path.join(os.path.dirname(__file__), '../especialista/regras.py')
        caminho_regras = os.path.abspath(caminho_regras)
        
        spec = importlib.util.spec_from_file_location("regras_mod", caminho_regras)
        regras_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(regras_mod)
        get_regras_formatadas = regras_mod.get_regras_formatadas
        regras = get_regras_formatadas()
        
        win = ctk.CTkToplevel(parent) if parent else ctk.CTk()
        win.title("Manual de Regras Lógicas")
        win.geometry("800x850+200+50")
        win.resizable(True, True)
        frame = ctk.CTkFrame(win)
        frame.pack(expand=True, fill="both", padx=30, pady=30)
        label_titulo = ctk.CTkLabel(frame, text="Manual de Regras Lógicas", font=ctk.CTkFont(size=26, weight="bold"))
        label_titulo.pack(pady=(10, 20))
        
        text_frame = tk.Frame(frame)
        text_frame.pack(expand=True, fill="both")
        text = Text(text_frame, wrap="word", font=("Arial", 14), height=35, bg="#f8f8f8", borderwidth=0, relief="flat")
        scroll = Scrollbar(text_frame, command=text.yview)
        text.configure(yscrollcommand=scroll.set)
        text.pack(side="left", fill="both", expand=True)
        scroll.pack(side=RIGHT, fill=Y)
        
        for regra in regras:
            text.insert(END, f"{regra['nome']}\n", ("titulo",))
            text.insert(END, f"   Fórmula: {regra['formula']}\n", ("formula",))
            text.insert(END, f"   Explicação: {regra['explicacao']}\n", ("explicacao",))
            if 'exemplo' in regra:
                text.insert(END, f"   Exemplo: {regra['exemplo']}\n", ("exemplo",))
            text.insert(END, "\n")
        
        text.tag_config("titulo", font=("Arial", 15, "bold"), foreground="#1a237e")
        text.tag_config("formula", font=("Consolas", 13, "italic"), foreground="#1565c0")
        text.tag_config("explicacao", font=("Arial", 13), foreground="#333333")
        text.tag_config("exemplo", font=("Arial", 13, "italic"), foreground="#388e3c")
        text.configure(state="disabled")
        
        btn_fechar = ctk.CTkButton(frame, text="Fechar", command=win.destroy)
        btn_fechar.pack(pady=10)
        win.grab_set()
        win.focus_set()
        win.mainloop() if not parent else None

    def get_root(self):
        """Retorna a janela root"""
        return self.root
    
    def executar(self):
        """Inicia o loop principal da aplicação"""
        self.root.mainloop()