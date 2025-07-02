import customtkinter as ctk
from tkinter import messagebox

class ModalAvaliacao(ctk.CTkToplevel):
    def __init__(self, parent, avaliacao_detalhada: dict, on_close=None):
        super().__init__(parent)
        self.on_close = on_close 
        self.title("Avaliação Detalhada da Resposta")
        # Janela maior e centralizada
        largura, altura = 800, 650
        x = int(self.winfo_screenwidth() / 2 - largura / 2)
        y = int(self.winfo_screenheight() / 2 - altura / 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")
        self.resizable(True, True)
        self.grab_set()
        self.focus_set()
        # Frame principal para centralizar conteúdo
        frame = ctk.CTkFrame(self)
        frame.pack(expand=True, fill="both", padx=30, pady=30)
        # Título
        ctk.CTkLabel(frame, text="Avaliação Detalhada", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(15, 15))
        # Resposta do aluno
        ctk.CTkLabel(frame, text="Sua resposta:", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=10)
        box1 = ctk.CTkTextbox(frame, height=60, font=ctk.CTkFont(size=14), state="normal", wrap="word")
        box1.pack(fill="x", padx=10, pady=(0, 10))
        box1.insert("1.0", avaliacao_detalhada.get("resposta_aluno", ""))
        box1.configure(state="disabled")
        # Avaliador interno
        ctk.CTkLabel(frame, text="Avaliação do sistema:", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=10)
        box2 = ctk.CTkTextbox(frame, height=60, font=ctk.CTkFont(size=14), state="normal", wrap="word")
        box2.pack(fill="x", padx=10, pady=(0, 10))
        box2.insert("1.0", avaliacao_detalhada.get("avaliador_interno", ""))
        box2.configure(state="disabled")
        # Avaliação LLM (tradução)
        if avaliacao_detalhada.get("avaliacao_llm"):
            ctk.CTkLabel(frame, text="Avaliação da LLM (tradução):", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=10)
            box3 = ctk.CTkTextbox(frame, height=60, font=ctk.CTkFont(size=14), state="normal", wrap="word")
            box3.pack(fill="x", padx=10, pady=(0, 10))
            box3.insert("1.0", avaliacao_detalhada.get("avaliacao_llm", ""))
            box3.configure(state="disabled")
        # Explicação natural
        if avaliacao_detalhada.get("explicacao_natural"):
            ctk.CTkLabel(frame, text="Explicação natural:", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=10)
            box4 = ctk.CTkTextbox(frame, height=80, font=ctk.CTkFont(size=14), state="normal", wrap="word")
            box4.pack(fill="x", padx=10, pady=(0, 10))
            box4.insert("1.0", avaliacao_detalhada.get("explicacao_natural", ""))
            box4.configure(state="disabled")
        # Gabarito
        ctk.CTkLabel(frame, text="Gabarito da questão:", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=10)
        box5 = ctk.CTkTextbox(frame, height=60, font=ctk.CTkFont(size=14), state="normal", wrap="word")
        box5.pack(fill="x", padx=10, pady=(0, 10))
        box5.insert("1.0", avaliacao_detalhada.get("gabarito", ""))
        box5.configure(state="disabled")
        # Botão fechar centralizado
        ctk.CTkButton(frame, text="Fechar", command=self._fechar).pack(pady=15)
        self.protocol("WM_DELETE_WINDOW", self._fechar)

    def _fechar(self):
        self.destroy()
        if self.on_close:
            self.on_close()
