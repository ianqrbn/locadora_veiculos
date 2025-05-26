# visao/login_view.py
import tkinter as tk
from tkinter import ttk, messagebox


class LoginView(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.title("Login do Sistema")
        self.geometry("400x300")
        self.resizable(False, False)

        # self.transient(parent) # <-- REMOVA OU COMENTE ESTA LINHA

        self.grab_set()

        # ... o resto do arquivo continua exatamente igual ...
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill="both")
        ttk.Label(main_frame, text="Acesso ao Sistema", font=("Arial", 16, "bold")).pack(pady=(0, 20))
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill="x", pady=10)
        ttk.Label(form_frame, text="E-mail:").grid(row=0, column=0, sticky="w", pady=2)
        self.entry_email = ttk.Entry(form_frame)
        self.entry_email.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        ttk.Label(form_frame, text="Senha:").grid(row=2, column=0, sticky="w", pady=2)
        self.entry_senha = ttk.Entry(form_frame, show="*")
        self.entry_senha.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        form_frame.columnconfigure(0, weight=1)
        btn_login = ttk.Button(main_frame, text="Entrar", command=self.fazer_login)
        btn_login.pack(pady=20)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.controller.root.destroy()

    def fazer_login(self):
        email = self.entry_email.get()
        senha = self.entry_senha.get()
        self.controller.fazer_login(email, senha)