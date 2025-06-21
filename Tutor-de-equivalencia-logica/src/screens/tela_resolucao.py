import customtkinter as ctk
from screens.tela_avaliacao import EvaluatorScreen

class QuestionScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="Questão:", font=("Arial", 16)).pack(pady=10)
        ctk.CTkTextbox(self, height=100).pack(padx=20)

        ctk.CTkLabel(self, text="Sua Resposta:").pack(pady=5)
        self.entry = ctk.CTkTextbox(self, height=100)
        self.entry.pack(padx=20, pady=5)

        frame = ctk.CTkFrame(self)
        frame.pack(pady=10)
        ctk.CTkButton(frame, text="Perguntar ao LLM").grid(row=0, column=0, padx=5)
        ctk.CTkButton(frame, text="Dicas").grid(row=0, column=1, padx=5)
        ctk.CTkLabel(frame, text="Dificuldade: 2").grid(row=0, column=2, padx=5)

        ctk.CTkButton(self, text="Enviar", command=self.go_to_evaluator).pack(pady=20)

    def go_to_evaluator(self):
        self.destroy()
        EvaluatorScreen(self.master).pack(fill="both", expand=True)