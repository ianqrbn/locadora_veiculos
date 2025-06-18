# visao/gerente_create_view.py
import tkinter as tk
from tkinter import ttk


class GerenteCreateView(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.title("Cadastro Inicial do Gerente")
        self.geometry("450x400")
        self.resizable(False, False)

        # self.transient(parent) # <-- REMOVA OU COMENTE ESTA LINHA

        self.grab_set()

        # ... o resto do arquivo continua exatamente igual ...
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill="both")
        ttk.Label(main_frame, text="Bem-vindo! Cadastre o Gerente.", font=("Arial", 14, "bold")).pack(pady=(0, 10))
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill="x", pady=10)
        ttk.Label(form_frame, text="Nome Completo:").grid(row=0, column=0, sticky="w", pady=2)
        self.entry_nome = ttk.Entry(form_frame)
        self.entry_nome.grid(row=1, column=0, sticky="ew", pady=(0, 5))
        ttk.Label(form_frame, text="E-mail:").grid(row=2, column=0, sticky="w", pady=2)
        self.entry_email = ttk.Entry(form_frame)
        self.entry_email.grid(row=3, column=0, sticky="ew", pady=(0, 5))
        ttk.Label(form_frame, text="Senha:").grid(row=4, column=0, sticky="w", pady=2)
        self.entry_senha = ttk.Entry(form_frame, show="*")
        self.entry_senha.grid(row=5, column=0, sticky="ew", pady=(0, 5))
        ttk.Label(form_frame, text="Confirmar Senha:").grid(row=6, column=0, sticky="w", pady=2)
        self.entry_confirma_senha = ttk.Entry(form_frame, show="*")
        self.entry_confirma_senha.grid(row=7, column=0, sticky="ew", pady=(0, 5))
        form_frame.columnconfigure(0, weight=1)
        btn_cadastrar = ttk.Button(main_frame, text="Cadastrar", command=self.cadastrar)
        btn_cadastrar.pack(pady=20)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.controller.root.destroy()

    def cadastrar(self):
        nome = self.entry_nome.get()
        email = self.entry_email.get()
        senha = self.entry_senha.get()
        confirma_senha = self.entry_confirma_senha.get()
        self.controller.cadastrar_gerente_inicial(nome, email, senha, confirma_senha)