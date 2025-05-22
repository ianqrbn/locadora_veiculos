import tkinter as tk
from tkinter import ttk
from cliente_create_view import ClientView


class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Locação de Veículos - v2.0")
        self.geometry("1024x768")
        self.configure(bg="#f0f0f0")

        self.criar_menu_principal()
        self.criar_area_conteudo()

    def criar_menu_principal(self):
        menubar = tk.Menu(self)

        menu_cadastros = tk.Menu(menubar, tearoff=0)
        menu_cadastros.add_command(label="Clientes", command=self.exibir_cadastro_cliente, accelerator="Ctrl+C")
        menu_cadastros.add_command(label="Veículos", accelerator="Ctrl+V")
        menu_cadastros.add_separator()
        menu_cadastros.add_command(label="Sair", command=self.quit)
        menubar.add_cascade(label="Cadastros", menu=menu_cadastros)

        menu_operacoes = tk.Menu(menubar, tearoff=0)
        menu_operacoes.add_command(label="Nova Locação", accelerator="Ctrl+L")
        menu_operacoes.add_command(label="Cadastrar Multa", accelerator="Ctrl+M")
        menubar.add_cascade(label="Operações", menu=menu_operacoes)

        menu_edicoes = tk.Menu(menubar, tearoff=0)
        menu_edicoes.add_command(label="Gerenciar Funcionários")
        menu_edicoes.add_command(label="Gerenciar Clientes")
        menu_edicoes.add_command(label="Gerenciar Locações")
        menu_edicoes.add_command(label="Gerenciar Veículos")
        menu_edicoes.add_command(label="Gerenciar Multas")
        menubar.add_cascade(label="Edições e Exclusões", menu=menu_edicoes)

        self.config(menu=menubar)

    def criar_area_conteudo(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.aba_dashboard = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_dashboard, text="Dashboard")

        self.label_bem_vindo = ttk.Label(self.aba_dashboard, text="Bem-vindo ao Sistema!")
        self.label_bem_vindo.pack(pady=20)

        self.cadastro_cliente_view = ClientView(
            self.aba_dashboard,
            on_cadastro_success=self.on_cliente_cadastrado
        )

    def exibir_cadastro_cliente(self):
        self.label_bem_vindo.pack_forget()
        if not self.cadastro_cliente_view.winfo_ismapped():
            self.cadastro_cliente_view.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.notebook.select(self.aba_dashboard)

    def on_cliente_cadastrado(self):
        self.cadastro_cliente_view.pack_forget()
        self.label_bem_vindo.pack(pady=20)



if __name__ == "__main__":
    app = MainView()
    app.mainloop()
