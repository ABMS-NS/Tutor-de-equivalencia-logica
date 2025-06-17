import customtkinter as ctk
from screens.graph_screen import GraphScreen


class MainMenu(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="LOGITUT", font=("Arial", 32)).pack(pady=30)
        ctk.CTkButton(self, text="Começar", command=self.go_to_graph).pack(pady=10)
        ctk.CTkButton(self, text="Carregar", command=self.go_to_graph).pack(pady=10)
        ctk.CTkLabel(self, text="Créditos", font=("Arial", 12)).pack(pady=20)

    def go_to_graph(self):
        self.destroy()
        GraphScreen(self.master).pack(fill="both", expand=True)