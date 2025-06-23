import tkinter as tk
from tkinter import ttk
# Supondo que suas views de cadastro sejam Frames e estejam prontas para serem usadas
from visao.cliente_create_view import ClientView
from visao.veiculo_create_view import VehicleView
from visao.locacao_create_view import RentalView
from visao.funcionario_create_view import FuncionarioView
from visao.multa_create_view import FineView


# Não precisa mais importar Database aqui, será passada pelo controller

# Altera de tk.Tk para ttk.Frame
class MainView(ttk.Frame):
    def __init__(self, parent_container, controller, db_connection):
        super().__init__(parent_container)

        self.controller = controller
        self.db = db_connection  # Usa a conexão do banco de dados passada pelo controller

        self.view_atual = None  # Para controlar a view de cadastro exibida na aba

        # Configurações do Frame principal (opcional, pode usar estilos ttk)
        # self.configure(bg="#f0f0f0") # ttk.Frame usa estilos, não bg diretamente

        self.criar_menu_principal()
        self.criar_area_conteudo()
        self.criar_status_bar()

        # O fechamento da janela raiz (e do DB) será gerenciado pelo ApplicationController

    def criar_menu_principal(self):
        # O menu é adicionado à janela de nível superior (a janela raiz do controller)
        top_level_window = self.winfo_toplevel()
        menubar = tk.Menu(top_level_window)

        menu_cadastros = tk.Menu(menubar, tearoff=0)
        menu_cadastros.add_command(label="Clientes", command=self.exibir_cadastro_cliente, accelerator="Ctrl+C")
        menu_cadastros.add_command(label="Veículos", command=self.exibir_cadastro_veiculo, accelerator="Ctrl+V")
        menu_cadastros.add_command(label="Funcionários", command=self.exibir_cadastro_funcionario, accelerator="Ctrl+F")
        menu_cadastros.add_separator()
        # O comando Sair agora destrói a janela raiz, o que acionará o on_app_quit do controller
        menu_cadastros.add_command(label="Sair", command=top_level_window.destroy)
        menubar.add_cascade(label="Cadastros", menu=menu_cadastros)

        menu_operacoes = tk.Menu(menubar, tearoff=0)
        menu_operacoes.add_command(label="Nova Locação", command=self.exibir_cadastro_locacao, accelerator="Ctrl+L")
        menu_operacoes.add_command(label="Cadastrar Multa", command=self.exibir_cadastro_multa, accelerator="Ctrl+M")
        menubar.add_cascade(label="Operações", menu=menu_operacoes)

        menu_edicoes = tk.Menu(menubar, tearoff=0)
        # TODO: Implementar as funcionalidades e associar comandos
        menu_edicoes.add_command(label="Gerenciar Funcionários",
                                 command=lambda: self.atualizar_status("Gerenciar Funcionários - A implementar"))
        menu_edicoes.add_command(label="Gerenciar Clientes",
                                 command=lambda: self.atualizar_status("Gerenciar Clientes - A implementar"))
        menu_edicoes.add_command(label="Gerenciar Locações",
                                 command=lambda: self.atualizar_status("Gerenciar Locações - A implementar"))
        menu_edicoes.add_command(label="Gerenciar Veículos",
                                 command=lambda: self.atualizar_status("Gerenciar Veículos - A implementar"))
        menu_edicoes.add_command(label="Gerenciar Multas",
                                 command=lambda: self.atualizar_status("Gerenciar Multas - A implementar"))
        menubar.add_cascade(label="Edições e Exclusões", menu=menu_edicoes)

        top_level_window.config(menu=menubar)

    def criar_area_conteudo(self):
        # O Notebook é criado dentro deste Frame (MainView)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # A aba dashboard é um Frame dentro do Notebook
        self.aba_dashboard = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_dashboard, text="Dashboard")

        # Conteúdo inicial do dashboard
        self.label_bem_vindo = ttk.Label(self.aba_dashboard, text="Bem-vindo ao Sistema de Locação!",
                                         font=("Arial", 16))
        self.label_bem_vindo.pack(pady=20, padx=20, anchor="center")

        # Frame para conter as views de cadastro dentro da aba_dashboard
        self.cadastro_view_container = ttk.Frame(self.aba_dashboard)
        # Não empacotar ainda, será gerenciado por exibir_view_conteudo

    def criar_status_bar(self):
        # A status bar é criada dentro deste Frame (MainView)
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto")
        status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor="w")
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def atualizar_status(self, mensagem):
        self.status_var.set(mensagem)

    def exibir_view_conteudo(self, view_class, titulo_status, *args_para_view):
        """
        Exibe uma view de cadastro (que deve ser uma classe de Frame) na área de conteúdo.
        view_class: A classe da view a ser instanciada (ex: ClientView).
        titulo_status: Mensagem para a barra de status.
        *args_para_view: Argumentos adicionais para o construtor da view_class (além do parent, controller e db).
        """
        # Limpa a view anterior, se houver
        if self.view_atual:
            self.view_atual.destroy()
            self.view_atual = None

        # Esconde o label de bem-vindo
        self.label_bem_vindo.pack_forget()

        # Garante que o container da view de cadastro está visível (se não estiver, empacota)
        if not self.cadastro_view_container.winfo_ismapped():
            self.cadastro_view_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # --- LINHA CORRIGIDA ---
        # Cria a nova view dentro do container, passando o controller e o db
        self.view_atual = view_class(self.cadastro_view_container, self.controller, self.db, *args_para_view)
        # --- FIM DA CORREÇÃO ---

        self.view_atual.pack(fill=tk.BOTH, expand=True)

        self.atualizar_status(titulo_status)
        self.notebook.select(self.aba_dashboard)  # Garante que a aba do dashboard esteja selecionada

    def _retornar_ao_dashboard(self, mensagem_status="Operação Concluída."):
        """Método auxiliar para limpar a view de cadastro e mostrar o dashboard."""
        if self.view_atual:
            self.view_atual.destroy()
            self.view_atual = None

        # Esconde o container das views de cadastro se estiver vazio
        if not self.cadastro_view_container.winfo_children():
            self.cadastro_view_container.pack_forget()

        self.label_bem_vindo.pack(pady=20, padx=20, anchor="center")  # Mostra o label de bem-vindo
        self.atualizar_status(mensagem_status)
        self.notebook.select(self.aba_dashboard)

    # --- Comandos do Menu ---
    def exibir_cadastro_cliente(self):
        # Garanta que ClientView está importado e que seu __init__ espera (parent, controller, db, callback)
        self.exibir_view_conteudo(ClientView, "Cadastro de Clientes", self._retornar_ao_dashboard)

    def exibir_cadastro_veiculo(self):
        # Garanta que VehicleView está importado e que seu __init__ espera (parent, controller, db, callback)
        self.exibir_view_conteudo(VehicleView, "Cadastro de Veículos", self._retornar_ao_dashboard)

    def exibir_cadastro_locacao(self):
        # Garanta que RentalView está importado e que seu __init__ espera (parent, controller, db, callback)
        self.exibir_view_conteudo(RentalView, "Nova Locação", self._retornar_ao_dashboard)


    def exibir_cadastro_funcionario(self):
        self.exibir_view_conteudo(FuncionarioView, "Cadastro de Funcionários", self._retornar_ao_dashboard)


    def exibir_cadastro_multa(self):
        # Garanta que FineView está importado
        # A linha abaixo chama a tela de cadastro
        self.exibir_view_conteudo(FineView, "Cadastro de Multa", self._retornar_ao_dashboard)
# O bloco if __name__ == "__main__": foi removido daqui.
# A MainView será instanciada pelo ApplicationController.
