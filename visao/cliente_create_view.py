import tkinter as tk
from tkinter import ttk, messagebox

class ClientView(ttk.Frame):
    def __init__(self, parent, db, on_cadastro_success):
        super().__init__(parent)
        self.db = db
        self.on_cadastro_success = on_cadastro_success
        self.criar_widgets()

    def criar_widgets(self):
        form_frame = ttk.LabelFrame(self, text="Dados do Cliente")
        form_frame.pack(fill=tk.X, pady=10, padx=10)

        ttk.Label(form_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.nome_entry = ttk.Entry(form_frame, width=40)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="CPF:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.cpf_entry = ttk.Entry(form_frame, width=15)
        self.cpf_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Telefone:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.telefone_entry = ttk.Entry(form_frame, width=15)
        self.telefone_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Rua:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.rua_entry = ttk.Entry(form_frame, width=40)
        self.rua_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Número:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.numero_entry = ttk.Entry(form_frame, width=15)
        self.numero_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Bairro:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.bairro_entry = ttk.Entry(form_frame, width=40)
        self.bairro_entry.grid(row=5, column=1, padx=5, pady=5)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10, padx=10, fill=tk.X)

        ttk.Button(btn_frame, text="Salvar", command=self.cadastrar_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar_campos).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Excluir Cliente", command=self.excluir_cliente).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Fechar", command=self.limpar_e_ocultar).pack(side=tk.RIGHT, padx=5)

        self.tree = ttk.Treeview(self, columns=("ID", "Nome", "CPF", "Telefone"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("CPF", text="CPF")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.column("ID", width=40, anchor=tk.CENTER)
        self.tree.column("Nome", width=150)
        self.tree.column("CPF", width=100)
        self.tree.column("Telefone", width=100)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.atualizar_lista_clientes()

    def atualizar_lista_clientes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        clientes = self.db.get_all_clientes()
        for cliente in clientes:
            cliente_id, nome, cpf, telefone, *_ = cliente
            self.tree.insert("", tk.END, values=(cliente_id, nome, cpf, telefone))

    def limpar_campos(self):
        self.nome_entry.delete(0, tk.END)
        self.cpf_entry.delete(0, tk.END)
        self.telefone_entry.delete(0, tk.END)
        self.rua_entry.delete(0, tk.END)
        self.numero_entry.delete(0, tk.END)
        self.bairro_entry.delete(0, tk.END)

    def limpar_e_ocultar(self):
        self.limpar_campos()
        self.pack_forget()

    def cadastrar_cliente(self):
        nome = self.nome_entry.get()
        cpf = self.cpf_entry.get()
        telefone = self.telefone_entry.get()
        rua = self.rua_entry.get()
        numero = self.numero_entry.get()
        bairro = self.bairro_entry.get()

        if not all([nome, cpf, telefone, rua, numero, bairro]):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        cliente_id = self.db.insert_cliente(nome, cpf, telefone, rua, numero, bairro)

        if cliente_id:
            messagebox.showinfo("Sucesso", f"Cliente cadastrado com sucesso! (ID: {cliente_id})")
            self.atualizar_lista_clientes()
            if self.on_cadastro_success:
                self.on_cadastro_success()
        else:
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
