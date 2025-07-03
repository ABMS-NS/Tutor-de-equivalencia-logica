"""
Modal para exibir resultado final de um nível.
"""

import customtkinter as ctk
from tkinter import messagebox
from src.perfil.graficos import grafico_progresso_nivel
from src.config import ADVANCEMENT_CRITERIA
from src.perfil.perfil import carregar_perfil

class ModalFinalNivel:
    def __init__(self, parent, nivel, perfil_path, app_instance):  
        self.parent = parent
        self.nivel = nivel
        self.perfil_path = perfil_path  
        self.app_instance = app_instance
        
        self.window = ctk.CTkToplevel(parent)
        self.window.title(f"Resumo do Nível {nivel}")
        
        
        largura, altura = 700, 500
        x = int(self.window.winfo_screenwidth() / 2 - largura / 2)
        y = int(self.window.winfo_screenheight() / 2 - altura / 2)
        self.window.geometry(f"{largura}x{altura}+{x}+{y}")
        self.window.resizable(True, True)
        self.window.grab_set()
        self.window.focus_set()
        
        self.criar_interface()


    def criar_interface(self):
        """Cria a interface do modal de finalização de nível"""
        try:
            dados_perfil = carregar_perfil(self.perfil_path)
            nivel_str = str(self.nivel)
            
            if not dados_perfil or nivel_str not in dados_perfil.get("niveis", {}):
                messagebox.showerror("Erro", "Não foi possível carregar dados do nível.")
                self.window.destroy()
                return
            
            nivel_data = dados_perfil["niveis"][nivel_str]
            tentativas = nivel_data.get("tentativas_anteriores", [])
            
            if not tentativas:
                messagebox.showerror("Erro", "Nenhuma tentativa encontrada neste nível.")
                self.window.destroy()
                return
            
            
            ultima_tentativa = tentativas[-1]
            total_questoes = ultima_tentativa.get("total_questoes", 0)
            acertos = ultima_tentativa.get("acertos", 0)
            dificuldade_media = ultima_tentativa.get("dificuldade_media", 0)
            percentual = (acertos / total_questoes) * 100 if total_questoes > 0 else 0
            
           
            min_taxa = ADVANCEMENT_CRITERIA.get("min_grade", 7.0) * 10  # 7.0 -> 70%
            max_dificuldade = ADVANCEMENT_CRITERIA.get("max_difficulty", 2.0)  # 2.0
            
            liberou_proximo = (percentual >= min_taxa and dificuldade_media <= max_dificuldade)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar dados: {str(e)}")
            self.window.destroy()
            return

        # Interface
        frame = ctk.CTkFrame(self.window)
        frame.pack(expand=True, fill="both", padx=30, pady=30)

        # Título
        titulo = ctk.CTkLabel(
            frame, 
            text=f"🎯 Nível {self.nivel} Finalizado!", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        titulo.pack(pady=(10, 10))

        # Resumo dos resultados
        resumo = (
            f"📊 Questões respondidas: {total_questoes}\n"
            f"✅ Acertos: {acertos}\n"
            f"📈 Taxa de acerto: {percentual:.1f}%\n"
            f"⚖️ Dificuldade média: {dificuldade_media:.2f}\n\n"
            f"🎯 Meta: {min_taxa:.0f}% de acertos\n"
            f"⚖️ Dificuldade máxima: {max_dificuldade}"
        )
        
        label_resumo = ctk.CTkLabel(
            frame, 
            text=resumo, 
            font=ctk.CTkFont(size=16),
            justify="left"
        )
        label_resumo.pack(pady=(10, 20))

        # Mensagem de resultado
        if liberou_proximo:
            msg = f"🎉 Parabéns! Você atingiu os critérios e desbloqueou o próximo nível!"
            cor = "#2ecc71"
            emoji = "🏆"
        else:
            msg = f"📚 Continue praticando! Você ainda não atingiu todos os critérios para o próximo nível."
            cor = "#e74c3c"
            emoji = "💪"
        
        label_msg = ctk.CTkLabel(
            frame, 
            text=f"{emoji} {msg}", 
            font=ctk.CTkFont(size=16, weight="bold"), 
            text_color=cor,
            wraplength=600
        )
        label_msg.pack(pady=(0, 20))

        # Botões
        frame_botoes = ctk.CTkFrame(frame, fg_color="transparent")
        frame_botoes.pack(pady=(20, 10))

        # Botão gráfico
        btn_grafico = ctk.CTkButton(
            frame_botoes, 
            text="📊 Ver Gráfico de Progresso", 
            font=ctk.CTkFont(size=15),
            width=200,
            command=lambda: self.mostrar_grafico()
        )
        btn_grafico.pack(side="left", padx=(0, 10))

        # Botão OK
        btn_ok = ctk.CTkButton(
            frame_botoes, 
            text="✅ Continuar", 
            font=ctk.CTkFont(size=15),
            width=150,
            command=self.fechar
        )
        btn_ok.pack(side="right")

    def mostrar_grafico(self):
        """Mostra gráfico de progresso do nível"""
        try:
            grafico_progresso_nivel(self.nivel, self.perfil_path)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exibir gráfico: {str(e)}")

    def fechar(self):
        """Fecha modal e volta para seleção de níveis"""
        self.window.destroy()
        
        try:
            dados_perfil_atualizado = carregar_perfil(self.perfil_path)
            if self.app_instance:
                self.app_instance.voltar_para_levels_selection(dados_perfil_atualizado, self.perfil_path)
            else:
                print("App instance não disponível para voltar para levels_selection.")
                if self.app_instance:
                    self.app_instance.voltar_para_main_window()
        except Exception as e:
            print(f"Erro ao voltar para levels_selection: {e}")
            if self.app_instance:
                self.app_instance.voltar_para_main_window()