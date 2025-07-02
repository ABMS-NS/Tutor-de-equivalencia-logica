"""
Teclado lógico virtual para inserir símbolos lógicos em campos de texto.
"""
import customtkinter as ctk

class TecladoLogico(ctk.CTkFrame):
    def __init__(self, parent, campo_destino, **kwargs):
        super().__init__(parent, **kwargs)
        self.campo_destino = campo_destino
        simbolos = [
            ("¬", "Negação"),
            ("∧", "Conjunção"),
            ("∨", "Disjunção"),
            ("→", "Implicação"),
            ("↔", "Bicondicional"),
            ("⊻", "Ou-exclusivo"),
            ("V", "Verdadeiro"),
            ("F", "Falso")
        ]
        for i, (simbolo, tooltip) in enumerate(simbolos):
            btn = ctk.CTkButton(
                self,
                text=simbolo,
                width=40,
                height=40,
                font=ctk.CTkFont(size=18, weight="bold"),
                command=lambda s=simbolo: self.inserir_simbolo(s)
            )
            btn.grid(row=0, column=i, padx=2, pady=2)

    def inserir_simbolo(self, simbolo):
        # Insere o símbolo na posição atual do cursor do campo de texto
        widget = self.campo_destino
        try:
            widget.insert("insert", simbolo)
        except Exception:
            pass
