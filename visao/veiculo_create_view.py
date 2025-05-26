import tkinter as tk
from tkinter import ttk, messagebox


class VehicleView(ttk.Frame):
    # --- __INIT__ CORRIGIDO para aceitar 'controller' ---
    def __init__(self, parent, controller, db, on_success_callback):
        super().__init__(parent)
        self.controller = controller  # Armazena a referência ao controller
        self.db = db
        self.on_success_callback = on_success_callback

        self.criar_widgets()
        self.atualizar_lista_veiculos()

    def criar_widgets(self):
        form_frame = ttk.LabelFrame(self, text="Dados do Veículo")
        form_frame.pack(fill=tk.X, pady=10, padx=10)

        ttk.Label(form_frame, text="Marca:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.marca_entry = ttk.Entry(form_frame, width=40)
        self.marca_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(form_frame, text="Modelo:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.modelo_entry = ttk.Entry(form_frame, width=40)
        self.modelo_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(form_frame, text="Ano:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.ano_entry = ttk.Entry(form_frame, width=15)
        self.ano_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Placa:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.placa_entry = ttk.Entry(form_frame, width=15)
        self.placa_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Cor:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.cor_entry = ttk.Entry(form_frame, width=15)
        self.cor_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        form_frame.columnconfigure(1, weight=1)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10, padx=10, fill=tk.X)

        ttk.Button(btn_frame, text="Salvar Veículo", command=self.cadastrar_veiculo).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar Campos", command=self.limpar_campos).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Excluir Veículo", command=self.excluir_veiculo).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Fechar",
                   command=lambda: self.on_success_callback("Cadastro de veículo fechado.")).pack(side=tk.RIGHT, padx=5)

        tree_frame = ttk.LabelFrame(self, text="Veículos Cadastrados")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


        tree_columns = ("ID", "Marca", "Modelo", "Ano", "Placa", "Cor", "Status")
        self.tree = ttk.Treeview(tree_frame, columns=tree_columns, show="headings")

        for col in tree_columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.W, width=110)
        self.tree.column("ID", width=40, anchor=tk.CENTER)
        self.tree.column("Ano", width=60, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def atualizar_lista_veiculos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            veiculos = self.db.get_all_veiculos()  # Espera (id, marca, modelo, ano, placa, cor, status)
            if veiculos:
                for veiculo_data in veiculos:
                    self.tree.insert("", tk.END, values=veiculo_data)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar a lista de veículos: {e}", parent=self)

    def limpar_campos(self):
        self.marca_entry.delete(0, tk.END)
        self.modelo_entry.delete(0, tk.END)
        self.ano_entry.delete(0, tk.END)
        self.placa_entry.delete(0, tk.END)
        self.cor_entry.delete(0, tk.END)
        self.marca_entry.focus()

    def cadastrar_veiculo(self):
        marca = self.marca_entry.get().strip()
        modelo = self.modelo_entry.get().strip()
        ano_str = self.ano_entry.get().strip()
        placa = self.placa_entry.get().strip().upper()
        cor = self.cor_entry.get().strip()

        if not all([marca, modelo, ano_str, placa, cor]):
            messagebox.showwarning("Campos Vazios", "Todos os campos são obrigatórios!", parent=self)
            return

        try:
            ano = int(ano_str)
        except ValueError:
            messagebox.showerror("Erro de Formato", "O ano deve ser um número válido (ex: 2023).", parent=self)
            return

        # O método insert_veiculo no database.py já não espera 'chassi'
        veiculo_id = self.db.insert_veiculo(marca, modelo, ano, placa, cor)

        if veiculo_id:
            messagebox.showinfo("Sucesso", f"Veículo '{marca} {modelo}' cadastrado com sucesso!", parent=self)
            self.limpar_campos()
            self.atualizar_lista_veiculos()
        else:
            messagebox.showerror("Erro",
                                 "Falha ao cadastrar veículo. Verifique o console para mais detalhes (placas duplicadas?).")

    def carregar_veiculos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        veiculos = self.db.get_all_veiculos()
        for veiculo in veiculos:
            self.tree.insert("", "end", values=veiculo)


    def excluir_veiculo(self):

        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um veículo para excluir!")
            return

        item = self.tree.item(selecionado[0])
        veiculo_id = item["values"][0]

        confirmacao = messagebox.askyesno("Confirmação", "Deseja realmente excluir este veículo?")
        if confirmacao:
            sucesso = self.db.delete_veiculo(veiculo_id)
            if sucesso:
                messagebox.showinfo("Sucesso", "Veículo excluído com sucesso!")
                self.carregar_veiculos()
            else:
                messagebox.showerror("Erro", "Falha ao excluir veículo!")


            messagebox.showerror("Erro de Cadastro", "Falha ao cadastrar veículo. Verifique se a placa já existe.",
                                 parent=self)
