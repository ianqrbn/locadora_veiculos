import tkinter as tk
from tkinter import ttk
from visao.cliente_create_view import ClientView
from visao.veiculo_create_view import VehicleView
from visao.locacao_create_view import RentalView
from visao.multa_create_view import FineView
from persistencia.database import Database # Importe o módulo do banco de dados

class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Locação de Veículos - v2.0")
        self.geometry("1024x768")
        self.configure(bg="#f0f0f0")

        self.db = Database("persistencia/locadora.db")
        self.view_atual = None

        self.criar_menu_principal()
        self.criar_area_conteudo()
        self.criar_status_bar()

        # O que fazer ao fechar a janela
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """Fecha a conexão com o BD ao fechar a janela principal."""
        if self.db:
            self.db.close()
        self.destroy()

    def criar_menu_principal(self):
        menubar = tk.Menu(self)

        menu_cadastros = tk.Menu(menubar, tearoff=0)
        menu_cadastros.add_command(label="Clientes", command=self.exibir_cadastro_cliente, accelerator="Ctrl+C")
        menu_cadastros.add_command(label="Veículos", command=self.exibir_cadastro_veiculo, accelerator="Ctrl+V")
        menu_cadastros.add_separator()
        menu_cadastros.add_command(label="Sair", command=self.quit)

        menubar.add_cascade(label="Cadastros", menu=menu_cadastros)

        menu_operacoes = tk.Menu(menubar, tearoff=0)
        menu_operacoes.add_command(label="Nova Locação", command=self.exibir_cadastro_locacao, accelerator="Ctrl+L")
        menu_operacoes.add_command(label="Cadastrar Multa", command=self.exibir_cadastro_multa, accelerator="Ctrl+M")
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

    def criar_status_bar(self):
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto")
        status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor="w")
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def atualizar_status(self, mensagem):
        self.status_var.set(mensagem)

    def exibir_view_conteudo(self, view_factory, titulo_status):
        if self.view_atual:
            self.view_atual.pack_forget()

        self.label_bem_vindo.pack_forget()

        # Passa a instância do banco de dados para a view através da factory
        self.view_atual = view_factory(self.aba_dashboard, self.db)
        self.view_atual.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.atualizar_status(titulo_status)
        self.notebook.select(self.aba_dashboard)

    def exibir_cadastro_cliente(self):
        # O on_cadastro_success é o callback que a view chamará ao salvar
        self.exibir_view_conteudo(
            lambda parent, db: ClientView(parent, db, on_cadastro_success=self.on_cliente_cadastrado),
            "Janela de Clientes aberta"
        )

    def exibir_cadastro_veiculo(self):
        self.exibir_view_conteudo(
            lambda parent, db: VehicleView(parent, db, on_cadastro_success=self.on_veiculo_cadastrado),
            "Janela de Veículos aberta"
        )

    def exibir_cadastro_locacao(self):
        self.exibir_view_conteudo(
            lambda parent, db: RentalView(parent, db, on_cadastro_success=self.on_locacao_cadastrada),
            "Janela de Locação aberta"
        )

    def exibir_cadastro_multa(self):
        self.exibir_view_conteudo(
            lambda parent, db: FineView(parent, db, on_cadastro_success=self.on_multa_cadastrada),
            "Janela de Multa aberta"
        )

    def on_cliente_cadastrado(self):
        if self.view_atual:
            self.view_atual.limpar_e_ocultar()
            self.view_atual = None
        self.label_bem_vindo.pack(pady=20)
        self.atualizar_status("Cliente cadastrado com sucesso!")

    def on_veiculo_cadastrado(self):
        if self.view_atual:
            self.view_atual.limpar_e_ocultar()
            self.view_atual = None
        self.label_bem_vindo.pack(pady=20)
        self.atualizar_status("Veículo cadastrado com sucesso!")

    def on_locacao_cadastrada(self):
        if self.view_atual:
            self.view_atual.limpar_e_ocultar()
            self.view_atual = None
        self.label_bem_vindo.pack(pady=20)
        self.atualizar_status("Locação cadastrada com sucesso!")

    def on_multa_cadastrada(self):
        if self.view_atual:
            self.view_atual.limpar_e_ocultar()
            self.view_atual = None
        self.label_bem_vindo.pack(pady=20)
        self.atualizar_status("Multa cadastrada com sucesso!")

if __name__ == "__main__":
    app = MainView()
    app.mainloop()