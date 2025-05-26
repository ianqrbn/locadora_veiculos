import tkinter as tk
from tkinter import messagebox
import hashlib
import time

from persistencia.database import Database
from visao.login_view import LoginView
from visao.gerente_create_view import GerenteCreateView
from visao.main_view import MainView  # Importa a MainView revisada


def log_message(message):
    print(f"[{time.strftime('%H:%M:%S')}] CONTROLLER: {message}")


class ApplicationController:
    def __init__(self):
        log_message("Iniciando o controlador (__init__)...")
        self.db = Database()
        self.root = tk.Tk()
        # Mantém o withdraw aqui, pois as Toplevels (Login/Gerente) precisam de um pai,
        # mesmo que escondido inicialmente. A lógica de deiconify será robusta.
        self.root.withdraw()

        self.logged_in_user = None  # Para guardar os dados do usuário logado
        self.current_toplevel_view = None
        self.main_view_instance = None
        log_message("Controlador inicializado.")

    def run(self):
        log_message("Método run() iniciado.")
        self.show_initial_view()

        log_message("Entrando no mainloop() do ApplicationController...")
        self.root.mainloop()

        log_message("Mainloop() do ApplicationController finalizado.")
        if self.db and self.db.conn:
            log_message("Fechando a conexão DB do ApplicationController ao final de run().")
            self.db.close()

    def switch_toplevel_view(self, new_view_class):
        log_message(f"Chamando switch_toplevel_view para a classe: {new_view_class.__name__}")
        if self.current_toplevel_view:
            self.current_toplevel_view.destroy()

        log_message(f"Criando nova instância Toplevel de: {new_view_class.__name__}")
        self.current_toplevel_view = new_view_class(self.root, self)
        log_message("switch_toplevel_view finalizado.")

    def show_initial_view(self):
        log_message("Chamando show_initial_view...")
        if not self.db.admin_existe():
            self.switch_toplevel_view(GerenteCreateView)
        else:
            self.switch_toplevel_view(LoginView)

    def cadastrar_gerente_inicial(self, nome, email, senha, confirma_senha):
        log_message("Chamando cadastrar_gerente_inicial...")
        if not all([nome, email, senha, confirma_senha]):
            messagebox.showerror("Erro de Validação", "Todos os campos são obrigatórios.",
                                 parent=self.current_toplevel_view)
            return
        if senha != confirma_senha:
            messagebox.showerror("Erro de Validação", "As senhas não coincidem.", parent=self.current_toplevel_view)
            return

        sucesso = self.db.insert_gerente(nome, email, senha)
        if sucesso:
            messagebox.showinfo("Sucesso", "Gerente cadastrado com sucesso! Agora você pode fazer o login.",
                                parent=self.current_toplevel_view)
            self.switch_toplevel_view(LoginView)
        else:
            messagebox.showerror("Erro no Cadastro", "O e-mail informado já está em uso.",
                                 parent=self.current_toplevel_view)

    def fazer_login(self, email, senha):
        log_message(f"Chamando fazer_login para o email: {email}")
        if not email or not senha:
            messagebox.showerror("Erro de Login", "E-mail e senha são obrigatórios.", parent=self.current_toplevel_view)
            return

        gerente_data = self.db.get_gerente_by_email(email)
        log_message(f"Dados retornados do DB para o email '{email}': {gerente_data}")

        if gerente_data:
            senha_hash_armazenada = gerente_data[3]
            senha_digitada_hash = hashlib.sha256(senha.encode('utf-8')).hexdigest()

            if senha_digitada_hash == senha_hash_armazenada:
                log_message("Login validado com sucesso.")
                self.logged_in_user = gerente_data  # Armazena os dados do usuário
                log_message(
                    f"Controller: self.logged_in_user DEFINIDO COMO: {self.logged_in_user}, TIPO: {type(self.logged_in_user)}")

                # A messagebox de boas-vindas está comentada para não interromper o fluxo de teste da janela
                # messagebox.showinfo("Login Bem-sucedido", f"Bem-vindo, {gerente_data[1]}!", parent=self.current_toplevel_view)

                self.show_main_application_window()
                return
            else:
                log_message("Senha incorreta.")
                messagebox.showerror("Erro de Login", "Senha incorreta.", parent=self.current_toplevel_view)
        else:
            log_message("Nenhum gerente encontrado com este e-mail.")
            messagebox.showerror("Erro de Login", "Nenhum gerente encontrado com este e-mail.",
                                 parent=self.current_toplevel_view)

    def _center_window(self, window, width, height):
        """Centraliza uma janela no ecrã."""
        window.update_idletasks()  # Garante que as dimensões da janela sejam as mais recentes
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')
        log_message(f"Janela centralizada em: {x},{y} com tamanho {width}x{height}")

    def _configure_main_window_appearance(self):
        """Função auxiliar para configurar a aparência da janela principal após um delay."""
        log_message("Executando _configure_main_window_appearance via 'after'")
        self.root.update_idletasks()
        self.root.state('normal')
        self.root.lift()
        self.root.focus_set()
        try:
            # Tenta forçar a janela para o topo e depois reverte (específico para alguns S.O.)
            self.root.attributes('-topmost', True)
            self.root.update_idletasks()
            self.root.attributes('-topmost', False)
            log_message("Atributo -topmost aplicado e revertido.")
        except tk.TclError:
            log_message("Atributo -topmost não suportado ou falhou.")
        log_message("Janela principal deveria estar normal, no topo e com foco.")

    def show_main_application_window(self):
        log_message("show_main_application_window() chamado.")
        if self.current_toplevel_view:
            self.current_toplevel_view.destroy()
            self.current_toplevel_view = None

        window_width = 1024
        window_height = 768

        self.root.title("Sistema de Locação de Veículos Principal")
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.minsize(800, 600)

        self._center_window(self.root, window_width, window_height)  # Centraliza

        self.root.deiconify()  # Torna a janela visível
        log_message("Janela root 'deiconified'. Agendando configuração final.")

        # Agenda a configuração final da aparência da janela com um delay
        self.root.after(200, self._configure_main_window_appearance)

        log_message("Instanciando MainView (como Frame) dentro da janela root...")
        self.main_view_instance = MainView(parent_container=self.root, controller=self, db_connection=self.db)
        self.main_view_instance.pack(fill=tk.BOTH, expand=True)

        self.root.protocol("WM_DELETE_WINDOW", self.on_app_quit)
        log_message("MainView instanciada e empacotada. Janela principal configurada.")

    def on_app_quit(self):
        log_message("on_app_quit chamado.")
        if messagebox.askokcancel("Sair", "Você tem certeza que quer sair do sistema?"):
            if self.db and self.db.conn:
                self.db.close()
            if self.root:
                self.root.destroy()
