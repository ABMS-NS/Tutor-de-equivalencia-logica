import customtkinter as ctk
import json
import os
from tkinter import messagebox

class TutorLogica:
    def __init__(self):
        #tema (estudar depois)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        #janela principal
        self.root = ctk.CTk()
        self.root.title("Tutor de Lógica")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        #centralizar
        self.centralizar_janela(self.root, 600, 400)
        
        self.criar_tela_principal()
        
    def centralizar_janela(self, janela, largura, altura):
        x = (janela.winfo_screenwidth() // 2) - (largura // 2)
        y = (janela.winfo_screenheight() // 2) - (altura // 2)
        janela.geometry(f"{largura}x{altura}+{x}+{y}")
    
    def criar_tela_principal(self):
        """Cria a interface da tela principal"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        #titulo
        titulo = ctk.CTkLabel(
            main_frame,
            text="Tutor de Lógica",
            font=ctk.CTkFont(size=36, weight="bold")
        )
        titulo.pack(pady=(40, 20))
        
        #letrinhas embaixo do titulo
        subtitulo = ctk.CTkLabel(
            main_frame,
            text="Aprenda lógica de forma interativa e personalizada",
            font=ctk.CTkFont(size=16)
        )
        subtitulo.pack(pady=(0, 40))
        
        #botao iniciar
        btn_iniciar = ctk.CTkButton(
            main_frame,
            text="INICIAR",
            font=ctk.CTkFont(size=20, weight="bold"),
            width=200,
            height=50,
            command=self.iniciar_tutor
        )
        btn_iniciar.pack(pady=20)
        
        #infos
        info = ctk.CTkLabel(
            main_frame,
            text="Feito por Alison, Jean, Rian e Davi",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        info.pack(pady=(20, 0))
    
    def verificar_criar_pasta_dados(self):
        """Verifica se a pasta 'dados' existe, se não, cria ela"""
        if not os.path.exists("dados"):
            os.makedirs("dados")
    
    def carregar_dados_json(self):
        """Carrega ou cria o arquivo dados.json"""
        self.verificar_criar_pasta_dados()
        
        caminho_arquivo = os.path.join("dados", "dados.json")
        
        try:
            if os.path.exists(caminho_arquivo):
                with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                    dados = json.load(arquivo)
                    return dados
            else:
                #cria a estrutura do json
                dados_iniciais = {
                    "nome": "",
                    "niveis": {
                        "1": {"dificuldade": 0, "questoes_erradas": []},
                        "2": {"dificuldade": 0, "questoes_erradas": []},
                        "3": {"dificuldade": 0, "questoes_erradas": []},
                        "4": {"dificuldade": 0, "questoes_erradas": []},
                        "5": {"dificuldade": 0, "questoes_erradas": []}
                    }
                }
                with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
                    json.dump(dados_iniciais, arquivo, indent=4, ensure_ascii=False)
                return dados_iniciais
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {str(e)}")
            return self.get_estrutura_inicial()
    
    def salvar_dados_json(self, dados):
        """Salva os dados no arquivo dados.json"""
        self.verificar_criar_pasta_dados()
        
        caminho_arquivo = os.path.join("dados", "dados.json")
        
        try:
            with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
                json.dump(dados, arquivo, indent=4, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar dados: {str(e)}")
    
    def get_estrutura_inicial(self):
        """Retorna a estrutura inicial dos dados"""
        return {
            "nome": "",
            "niveis": {
                "1": {"dificuldade": 0, "questoes_erradas": []},
                "2": {"dificuldade": 0, "questoes_erradas": []},
                "3": {"dificuldade": 0, "questoes_erradas": []},
                "4": {"dificuldade": 0, "questoes_erradas": []},
                "5": {"dificuldade": 0, "questoes_erradas": []}
            }
        }
    
    def configurar_dificuldades_por_nivel(self, dados, nivel_usuario):
        """Configura as dificuldades baseado no nível do usuário"""
        if nivel_usuario == "nunca_estudei":
            #todos os níveis com dificuldade 5 pra estarem travados
            for nivel in dados["niveis"]:
                dados["niveis"][nivel]["dificuldade"] = 5
                
        elif nivel_usuario == "ja_estudei":
            #apenas nível 1 com dificuldade 2, todos outros nível 5
            dados["niveis"]["1"]["dificuldade"] = 2
            for nivel in ["2", "3", "4", "5"]:
                dados["niveis"][nivel]["dificuldade"] = 5
                
        elif nivel_usuario == "professor":
            #nivel 1 e dois com dificuldade 2, os outros com 5
            dados["niveis"]["1"]["dificuldade"] = 2
            dados["niveis"]["2"]["dificuldade"] = 2
        
        return dados
    
    def iniciar_tutor(self):
        """Função chamada quando o botão Iniciar é clicado"""
        dados = self.carregar_dados_json()
        
        #verifica se já existe nome nos dados
        if "nome" not in dados or not dados.get("nome"):
            self.abrir_janela_nivel()
        else:
            #se já tem nome, pode continuar diretamente
            messagebox.showinfo("Bem-vindo!", f"Bem-vindo de volta, {dados['nome']}!")
            #seleção de níveis
            self.abrir_janela_selecao_niveis()
    
    def abrir_janela_nivel(self):
        """Abre a janela para seleção do nível de lógica"""
        #janela de seleção de nível
        janela_nivel = ctk.CTkToplevel(self.root)
        janela_nivel.title("Seleção de Nível")
        janela_nivel.geometry("450x350")
        janela_nivel.resizable(False, False)
        
        #centralização
        self.centralizar_janela(janela_nivel, 450, 350)
        
        # modal
        janela_nivel.grab_set()
        janela_nivel.focus_set()
        
        #frame principal da janela
        frame_nivel = ctk.CTkFrame(janela_nivel)
        frame_nivel.pack(expand=True, fill="both", padx=20, pady=20)
        
        #pergunta
        pergunta = ctk.CTkLabel(
            frame_nivel,
            text="Qual é seu nível de lógica?",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        pergunta.pack(pady=(30, 40))
        
        #variavel pra armazenar seleção
        nivel_var = ctk.StringVar(value="")
        
        #nível
        opcoes = [
            ("Nunca estudei", "nunca_estudei"),
            ("Já estudei lógica", "ja_estudei"),
            ("Sou professor de lógica", "professor")
        ]
        
        #radiobuttons
        for texto, valor in opcoes:
            radio = ctk.CTkRadioButton(
                frame_nivel,
                text=texto,
                variable=nivel_var,
                value=valor,
                font=ctk.CTkFont(size=16)
            )
            radio.pack(pady=10, anchor="w", padx=40)
        
        #confirmar
        def confirmar_nivel():
            if nivel_var.get():
                #carregar dados
                dados = self.carregar_dados_json()
                
                #config dificuldades
                dados = self.configurar_dificuldades_por_nivel(dados, nivel_var.get())
                
                #nome padrão (placeholder)
                dados["nome"] = "Usuário"
                
                #dados
                self.salvar_dados_json(dados)
                
                #fechar
                janela_nivel.destroy()
                
                #mensagem (gpt que fez)
                mensagens = {
                    "nunca_estudei": "Perfeito! Vamos começar do básico e construir uma base sólida em lógica!",
                    "ja_estudei": "Ótimo! Vamos revisar alguns conceitos e avançar para tópicos mais complexos!",
                    "professor": "Excelente! Como você já domina o assunto, vamos focar nos pontos mais avançados!"
                }
                
                messagebox.showinfo("Sucesso!", mensagens.get(nivel_var.get(), "Nível configurado com sucesso!"))
                
                #abrir janela
                self.abrir_janela_selecao_niveis()
            else:
                messagebox.showwarning("Atenção", "Por favor, selecione um nível!")
        
        btn_confirmar = ctk.CTkButton(
            frame_nivel,
            text="Confirmar",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=150,
            height=40,
            command=confirmar_nivel
        )
        btn_confirmar.pack(pady=30)
    
    def verificar_requisitos_nivel(self, nivel_desejado):
        """Verifica se o usuário atende os requisitos para acessar determinado nível"""
        dados = self.carregar_dados_json()
        
        if nivel_desejado == 1:
            return True  #nivel 1 sempre dispnivel
        
        #para níveis 2 e 3, verificar se níveis anteriores têm dificuldade <= 2
        for nivel in range(1, nivel_desejado):
            nivel_str = str(nivel)
            if nivel_str in dados["niveis"]:
                if dados["niveis"][nivel_str]["dificuldade"] > 2:
                    return False
        
        return True
    
    def abrir_janela_placeholder(self, nivel): #feito pelo GPT
        """Abre uma janela placeholder para o nível selecionado"""
        janela_placeholder = ctk.CTkToplevel(self.root)
        janela_placeholder.title(f"Nível {nivel}")
        janela_placeholder.geometry("400x300")
        janela_placeholder.resizable(False, False)
        
        # Centralizar janela
        self.centralizar_janela(janela_placeholder, 400, 300)
        
        # Tornar modal
        janela_placeholder.grab_set()
        janela_placeholder.focus_set()
        
        # Frame principal
        frame_placeholder = ctk.CTkFrame(janela_placeholder)
        frame_placeholder.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Título
        titulo = ctk.CTkLabel(
            frame_placeholder,
            text=f"Nível {nivel}",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        titulo.pack(pady=(40, 20))
        
        # Mensagem placeholder
        mensagem = ctk.CTkLabel(
            frame_placeholder,
            text="Esta janela será implementada em breve!\n\nAqui você encontrará as questões\ne exercícios deste nível.",
            font=ctk.CTkFont(size=16),
            justify="center"
        )
        mensagem.pack(pady=20)
        
        # Botão fechar
        btn_fechar = ctk.CTkButton(
            frame_placeholder,
            text="Fechar",
            width=120,
            command=janela_placeholder.destroy
        )
        btn_fechar.pack(pady=30)
    
    def abrir_janela_selecao_niveis(self):
        """Abre a janela de seleção de níveis"""
        janela_niveis = ctk.CTkToplevel(self.root)
        janela_niveis.title("Seleção de Níveis")
        janela_niveis.geometry("500x400")
        janela_niveis.resizable(False, False)
        
        # Centralizar janela
        self.centralizar_janela(janela_niveis, 500, 400)
        
        # Tornar modal
        janela_niveis.grab_set()
        janela_niveis.focus_set()
        
        # Frame principal
        frame_niveis = ctk.CTkFrame(janela_niveis)
        frame_niveis.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Título
        titulo = ctk.CTkLabel(
            frame_niveis,
            text="Escolha o Nível",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        titulo.pack(pady=(30, 40))
        
        # Subtítulo
        subtitulo = ctk.CTkLabel(
            frame_niveis,
            text="Selecione o nível que deseja estudar",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        subtitulo.pack(pady=(0, 30))
        
        # Função para lidar com clique nos botões
        def clicar_nivel(nivel):
            if self.verificar_requisitos_nivel(nivel):
                janela_niveis.destroy()
                self.abrir_janela_placeholder(nivel)
            else:
                # Janela de requisitos não atendidos
                janela_requisitos = ctk.CTkToplevel(janela_niveis)
                janela_requisitos.title("Requisitos não atendidos")
                janela_requisitos.geometry("350x200")
                janela_requisitos.resizable(False, False)
                
                # Centralizar
                self.centralizar_janela(janela_requisitos, 350, 200)
                
                # Tornar modal
                janela_requisitos.grab_set()
                janela_requisitos.focus_set()
                
                # Frame
                frame_req = ctk.CTkFrame(janela_requisitos)
                frame_req.pack(expand=True, fill="both", padx=15, pady=15)
                
                # Mensagem
                mensagem_req = ctk.CTkLabel(
                    frame_req,
                    text=f"❌ Nível {nivel} não disponível\n\nVocê precisa completar os níveis\nanteriores com dificuldade ≤ 2",
                    font=ctk.CTkFont(size=14),
                    justify="center"
                )
                mensagem_req.pack(expand=True)
                
                # Botão OK
                btn_ok = ctk.CTkButton(
                    frame_req,
                    text="OK",
                    width=80,
                    command=janela_requisitos.destroy
                )
                btn_ok.pack(pady=10)
        
        # Botões dos níveis
        for nivel in [1, 2, 3]:
            #verificação dos níveis
            disponivel = self.verificar_requisitos_nivel(nivel)
            
            btn_nivel = ctk.CTkButton(
                frame_niveis,
                text=f"Nível {nivel}",
                font=ctk.CTkFont(size=18, weight="bold"),
                width=200,
                height=50,
                command=lambda n=nivel: clicar_nivel(n),
                fg_color=None if disponivel else "gray",
                hover_color=None if not disponivel else None
            )
            btn_nivel.pack(pady=15)
            
            #indicação que não pode clicar
            if not disponivel:
                indicador = ctk.CTkLabel(
                    frame_niveis,
                    text="🔒 Requer completar níveis anteriores",
                    font=ctk.CTkFont(size=10),
                    text_color="gray"
                )
                indicador.pack(pady=(0, 10))
    
    def executar(self):
        """Inicia a aplicação"""
        self.root.mainloop()

# Executar a aplicação
if __name__ == "__main__":
    app = TutorLogica()
    app.executar()