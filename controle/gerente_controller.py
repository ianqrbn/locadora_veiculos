# controle/gerente_controller.py
import hashlib
from visao.gerente_create_view import GerenteCreateView
from visao.login_view import LoginView
from visao.funcionario_create_view import FuncionarioView


class GerenteController:
    def __init__(self, main_app, db):
        self.main_app = main_app
        self.db = db
        self.login_view = None
        self.gerente_create_view = None
        self.funcionario_view = None

    def iniciar(self):
        """Ponto de partida. Verifica se o gerente existe e abre a tela correta."""
        if not self.db.check_gerente_exists():
            self.abrir_cadastro_gerente_inicial()
        else:
            self.abrir_login()

    def abrir_cadastro_gerente_inicial(self):
        self.main_app.withdraw()  # Esconde a janela principal
        self.gerente_create_view = GerenteCreateView(self.main_app, self)

    def cadastrar_gerente_inicial(self, nome, email, senha, confirma_senha):
        if not nome or not email or not senha:
            self.gerente_create_view.show_error("Todos os campos são obrigatórios.")
            return
        if senha != confirma_senha:
            self.gerente_create_view.show_error("As senhas não coincidem.")
            return

        success = self.db.insert_gerente(nome, email, senha)
        if success:
            self.gerente_create_view.show_success_and_close()
            self.abrir_login()
        else:
            self.gerente_create_view.show_error("O e-mail informado já está em uso.")

    def abrir_login(self):
        self.main_app.withdraw()
        self.login_view = LoginView(self.main_app, self)

    def fazer_login(self, email, senha):
        gerente_data = self.db.get_gerente_by_email(email)
        if gerente_data:
            id_gerente, nome, email_db, senha_hash = gerente_data
            senha_fornecida_hash = hashlib.sha256(senha.encode('utf-8')).hexdigest()
            if senha_fornecida_hash == senha_hash:
                self.login_view.close_and_show_main()
                self.main_app.deiconify()
                self.main_app.setup_gerente_interface()
                return

        self.login_view.show_error("E-mail ou senha inválidos.")

    # --- Métodos para Gerenciamento de Funcionários ---

    def abrir_gerenciamento_funcionarios(self):
        if self.funcionario_view and self.funcionario_view.winfo_exists():
            self.funcionario_view.destroy()
        self.funcionario_view = FuncionarioView(self.main_app.get_content_area(), self)
        self.funcionario_view.pack(expand=True, fill="both")
        self.main_app.set_status("Gerenciamento de Funcionários")

    def listar_funcionarios(self):
        return self.db.get_all_funcionarios()

    def salvar_funcionario(self, dados):
        if not dados['nome'] or not dados['email'] or not dados['cpf']:
            self.funcionario_view.show_error("Nome, E-mail e CPF são obrigatórios.")
            return

        if dados['id']:  # Edição
            success = self.db.update_funcionario(dados['id'], dados['nome'], dados['email'], dados['cpf'],
                                                 dados['funcao'], dados['status'])
        else:  # Cadastro
            success = self.db.insert_funcionario(dados['nome'], dados['email'], dados['cpf'], dados['funcao'],
                                                 dados['status'])

        if success:
            self.funcionario_view.show_message("Sucesso", "Funcionário salvo com sucesso!")
            self.funcionario_view.carregar_funcionarios()
            self.funcionario_view.limpar_campos()
        else:
            self.funcionario_view.show_error("Erro ao salvar. Verifique se o E-mail ou CPF já estão cadastrados.")

    def excluir_funcionario(self, id_funcionario):
        self.db.delete_funcionario(id_funcionario)
        self.funcionario_view.show_message("Sucesso", "Funcionário excluído com sucesso!")
        self.funcionario_view.carregar_funcionarios()
        self.funcionario_view.limpar_campos()