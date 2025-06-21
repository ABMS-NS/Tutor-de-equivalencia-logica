import customtkinter as ctk
from screens.question_screen import QuestionScreen

class GraphScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="Grafo de Aprendizado", font=("Arial", 20)).pack(pady=10)
        ctk.CTkLabel(self, text="Clique em um nó para iniciar").pack(pady=5)

        for i in range(1, 6):
            ctk.CTkButton(self, text=f"Nível {i}", command=self.open_question).pack(pady=5)

    def open_question(self):
        self.destroy()
        QuestionScreen(self.master).pack(fill="both", expand=True)