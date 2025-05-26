import tkinter as tk
from tkinter import ttk, messagebox


class FuncionarioView(ttk.Frame):
    def __init__(self, parent, controller, db, on_success_callback):
        super().__init__(parent)
        self.controller = controller
        self.db = db
        self.on_success_callback = on_success_callback

        self.criar_widgets()
        self.atualizar_lista_funcionarios()

    def criar_widgets(self):
        # Frame para o formulário de cadastro
        form_frame = ttk.LabelFrame(self, text="Dados do Funcionário")
        form_frame.pack(fill=tk.X, pady=10, padx=10)

        ttk.Label(form_frame, text="Nome Completo:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.nome_entry = ttk.Entry(form_frame, width=40)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(form_frame, text="E-mail:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.email_entry = ttk.Entry(form_frame, width=40)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(form_frame, text="CPF:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.cpf_entry = ttk.Entry(form_frame, width=20)
        self.cpf_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Função:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.funcao_entry = ttk.Entry(form_frame, width=30)
        self.funcao_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW)

        # Para o status, podemos usar um Combobox (Ativo/Inativo)
        ttk.Label(form_frame, text="Status:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.status_var = tk.StringVar(value="Ativo")  # Valor padrão
        self.status_combo = ttk.Combobox(form_frame, textvariable=self.status_var, values=["Ativo", "Inativo"],
                                         state="readonly", width=18)
        self.status_combo.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        form_frame.columnconfigure(1, weight=1)

        # Frame para os botões
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10, padx=10, fill=tk.X)

        ttk.Button(btn_frame, text="Salvar Funcionário", command=self.salvar_funcionario).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar Campos", command=self.limpar_campos).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Fechar",
                   command=lambda: self.on_success_callback("Cadastro de funcionário fechado.")).pack(side=tk.RIGHT,
                                                                                                      padx=5)

        # Treeview para exibir a lista de funcionários
        tree_frame = ttk.LabelFrame(self, text="Funcionários Cadastrados")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tree_columns = ("ID", "Nome", "E-mail", "CPF", "Função", "Status")
        self.tree = ttk.Treeview(tree_frame, columns=tree_columns, show="headings")

        for col in tree_columns:
            self.tree.heading(col, text=col)
            if col == "ID":
                self.tree.column(col, width=40, anchor=tk.CENTER)
            elif col == "CPF":
                self.tree.column(col, width=110, anchor=tk.W)
            elif col == "E-mail" or col == "Nome":
                self.tree.column(col, width=200, anchor=tk.W)
            else:  # Função, Status
                self.tree.column(col, width=100, anchor=tk.W)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def atualizar_lista_funcionarios(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            funcionarios = self.db.get_all_funcionarios()  # Espera (id, nome, email, cpf, funcao, status)
            if funcionarios:
                for func in funcionarios:
                    # Converte o status booleano (0 ou 1) para texto ("Inativo" ou "Ativo")
                    status_texto = "Ativo" if func[5] == 1 else "Inativo"
                    # Monta a tupla de valores para a Treeview
                    valores_para_tree = func[0:5] + (status_texto,)
                    self.tree.insert("", tk.END, values=valores_para_tree)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar a lista de funcionários: {e}", parent=self)

    def limpar_campos(self):
        self.nome_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.cpf_entry.delete(0, tk.END)
        self.funcao_entry.delete(0, tk.END)
        self.status_var.set("Ativo")  # Reseta para o padrão
        self.nome_entry.focus()

    def salvar_funcionario(self):
        nome = self.nome_entry.get().strip()
        email = self.email_entry.get().strip()
        cpf = self.cpf_entry.get().strip()
        funcao = self.funcao_entry.get().strip()
        status_texto = self.status_var.get()

        # Converte o status de texto para booleano (0 ou 1)
        status_booleano = 1 if status_texto == "Ativo" else 0

        if not all([nome, email, cpf, funcao]):
            messagebox.showwarning("Campos Obrigatórios", "Nome, E-mail, CPF e Função são obrigatórios!", parent=self)
            return

        # Adicione aqui mais validações se necessário (ex: formato do CPF, e-mail)

        sucesso = self.db.insert_funcionario(nome, email, cpf, funcao, status_booleano)

        if sucesso:
            messagebox.showinfo("Sucesso", f"Funcionário '{nome}' cadastrado com sucesso!", parent=self)
            self.limpar_campos()
            self.atualizar_lista_funcionarios()
        else:
            messagebox.showerror("Erro de Cadastro",
                                 "Falha ao cadastrar funcionário. Verifique se o E-mail ou CPF já existem.",
                                 parent=self)
