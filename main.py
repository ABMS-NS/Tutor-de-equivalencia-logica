import customtkinter as ctk
from screens.main_menu import MainMenu

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Sistema de Aprendizagem")
app.geometry("900x600")

MainMenu(app).pack(fill="both", expand=True)

app.mainloop()