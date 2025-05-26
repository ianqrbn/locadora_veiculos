import tkinter as tk
from tkinter import ttk, messagebox


class ClientView(ttk.Frame):
    def __init__(self, parent, controller, db, on_success_callback):
        super().__init__(parent)
        self.controller = controller  # Armazena a referência ao controller
        self.db = db
        self.on_success_callback = on_success_callback  # Função a ser chamada após o sucesso

        self.criar_widgets()
        self.atualizar_lista_clientes()

    def criar_widgets(self):
        # Frame para o formulário de cadastro
        form_frame = ttk.LabelFrame(self, text="Dados do Cliente")
        form_frame.pack(fill=tk.X, pady=10, padx=10)

        ttk.Label(form_frame, text="Nome Completo:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.nome_entry = ttk.Entry(form_frame, width=40)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(form_frame, text="CPF:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.cpf_entry = ttk.Entry(form_frame, width=20)
        self.cpf_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Telefone:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.telefone_entry = ttk.Entry(form_frame, width=20)
        self.telefone_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Rua:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.rua_entry = ttk.Entry(form_frame, width=40)
        self.rua_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(form_frame, text="Número:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.numero_entry = ttk.Entry(form_frame, width=10)
        self.numero_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Bairro:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.bairro_entry = ttk.Entry(form_frame, width=30)
        self.bairro_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.EW)

        form_frame.columnconfigure(1, weight=1)  # Faz a coluna das entradas expandir

        # Frame para os botões
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10, padx=10, fill=tk.X)

        ttk.Button(btn_frame, text="Salvar Cliente", command=self.salvar_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar Campos", command=self.limpar_campos).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Fechar",
                   command=lambda: self.on_success_callback("Cadastro de cliente fechado.")).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Excluir Cliente", command=self.excluir_cliente).pack(side=tk.RIGHT, padx=5)

        # Treeview para exibir a lista de clientes
        tree_frame = ttk.LabelFrame(self, text="Clientes Cadastrados")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tree_columns = ("ID", "Nome", "CPF", "Telefone")
        self.tree = ttk.Treeview(tree_frame, columns=tree_columns, show="headings")

        for col in tree_columns:
            self.tree.heading(col, text=col)
            if col == "ID":
                self.tree.column(col, width=40, anchor=tk.CENTER)
            elif col == "CPF" or col == "Telefone":
                self.tree.column(col, width=120, anchor=tk.W)
            else:  # Nome
                self.tree.column(col, width=250, anchor=tk.W)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def atualizar_lista_clientes(self):
        # Limpa o Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            clientes = self.db.get_all_clientes()  # Espera (id, nome, cpf, telefone, ...)
            if clientes:
                for cliente in clientes:
                    # Adapte os índices conforme o retorno de get_all_clientes
                    self.tree.insert("", tk.END, values=(cliente[0], cliente[1], cliente[2], cliente[3]))
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar a lista de clientes: {e}", parent=self)
        clientes = self.db.get_all_clientes()


    def limpar_campos(self):
        self.nome_entry.delete(0, tk.END)
        self.cpf_entry.delete(0, tk.END)
        self.telefone_entry.delete(0, tk.END)
        self.rua_entry.delete(0, tk.END)
        self.numero_entry.delete(0, tk.END)
        self.bairro_entry.delete(0, tk.END)
        self.nome_entry.focus()

    def salvar_cliente(self):
        nome = self.nome_entry.get().strip()
        cpf = self.cpf_entry.get().strip()
        telefone = self.telefone_entry.get().strip()
        rua = self.rua_entry.get().strip()
        numero = self.numero_entry.get().strip()
        bairro = self.bairro_entry.get().strip()

        if not nome or not cpf:
            messagebox.showwarning("Campos Obrigatórios", "Nome e CPF são obrigatórios!", parent=self)
            return

        # Adicione aqui mais validações se necessário (ex: formato do CPF)

        # Supondo que seu db.insert_cliente espera esses argumentos
        cliente_id = self.db.insert_cliente(nome, cpf, telefone, rua, numero, bairro)

        if cliente_id:
            messagebox.showinfo("Sucesso", f"Cliente '{nome}' cadastrado com sucesso!", parent=self)
            self.limpar_campos()
            self.atualizar_lista_clientes()
            # Não chama on_success_callback aqui para manter a tela aberta,
            # a menos que queira que feche automaticamente após salvar.
            # Se quiser fechar: self.on_success_callback("Cliente cadastrado com sucesso!")
            messagebox.showinfo("Sucesso", f"Cliente cadastrado com sucesso! (ID: {cliente_id})")
            self.atualizar_lista_clientes()
            if self.on_cadastro_success:
                self.on_cadastro_success()
        else:
            messagebox.showerror("Erro de Cadastro", "Falha ao cadastrar cliente. Verifique se o CPF já existe.",
                                 parent=self)

            messagebox.showerror("Erro", "Falha ao cadastrar cliente. Verifique o console para mais detalhes (CPF duplicado?).")

    def excluir_cliente(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um cliente para excluir.")
            return

        cliente_id = self.tree.item(item)["values"][0]
        confirm = messagebox.askyesno("Confirmar Exclusão", f"Deseja excluir o cliente ID {cliente_id}?")
        if confirm:
            sucesso = self.db.delete_cliente(cliente_id)
            if sucesso:
                self.atualizar_lista_clientes()
                messagebox.showinfo("Sucesso", f"Cliente ID {cliente_id} excluído com sucesso.")
            else:
                messagebox.showerror("Erro", "Erro ao excluir cliente. Verifique dependências no banco.")
