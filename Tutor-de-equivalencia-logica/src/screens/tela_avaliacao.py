import customtkinter as ctk

class EvaluatorScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="Avaliador", font=("Arial", 20)).pack(pady=10)

        frame = ctk.CTkFrame(self)
        frame.pack(pady=10)

        ctk.CTkLabel(frame, text="Resposta do Aluno").grid(row=0, column=0, padx=10)
        ctk.CTkTextbox(frame, width=300, height=150).grid(row=1, column=0, padx=10)

        ctk.CTkLabel(frame, text="Avaliação LLM").grid(row=0, column=1, padx=10)
        ctk.CTkTextbox(frame, width=300, height=150).grid(row=1, column=1, padx=10)

        ctk.CTkLabel(self, text="Nota Final: 8.5").pack(pady=10)

        ctk.CTkButton(self, text="Fechar", command=self.master.destroy).pack(pady=10)