# visao/multa_create_view.py - VERSÃO SIMPLIFICADA (APENAS CRIAÇÃO)

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from controle.multa_controller import MultaController  # Importa o novo controller


class FineView(ttk.Frame):
    def __init__(self, parent, controller, db, on_success_callback):
        super().__init__(parent)
        self.controller = controller
        self.db = db
        self.on_success_callback = on_success_callback

        self.criar_widgets()
        self.atualizar_multas()

    def criar_widgets(self):
        form_frame = ttk.LabelFrame(self, text="Dados da Multa")
        form_frame.pack(fill=tk.X, pady=10, padx=10)

        ttk.Label(form_frame, text="ID Locação:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.locacao_id_entry = ttk.Entry(form_frame, width=15)
        self.locacao_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Data da Multa:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.data_multa_entry = ttk.Entry(form_frame, width=15)
        self.data_multa_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.data_multa_entry.insert(0, date.today().strftime("%d/%m/%Y"))

        ttk.Label(form_frame, text="Valor (R$):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.valor_entry = ttk.Entry(form_frame, width=15)
        self.valor_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Descrição:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.descricao_text = tk.Text(form_frame, width=40, height=4)
        self.descricao_text.grid(row=3, column=1, rowspan=2, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(form_frame, text="Situação:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.situacao_var = tk.StringVar(value="Pendente")
        self.situacao_combobox = ttk.Combobox(form_frame, textvariable=self.situacao_var,
                                              values=["Pendente", "Paga", "Contestada"], state="readonly")
        self.situacao_combobox.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

        form_frame.columnconfigure(1, weight=1)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10, padx=10, fill=tk.X)

        ttk.Button(btn_frame, text="Salvar Multa", command=self.cadastra_multa).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar_campos).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Fechar", command=lambda: self.on_success_callback("Operação cancelada.")).pack(
            side=tk.RIGHT, padx=5)

        tree_frame = ttk.LabelFrame(self, text="Multas Cadastradas")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tree_columns = ("id", "locacao_id", "data_multa", "valor", "situacao")
        self.tree = ttk.Treeview(tree_frame, columns=tree_columns, show="headings")

        self.tree.heading("id", text="ID")
        self.tree.heading("locacao_id", text="ID Locação")
        self.tree.heading("data_multa", text="Data Multa")
        self.tree.heading("valor", text="Valor")
        self.tree.heading("situacao", text="Situação")

        self.tree.column("id", width=50, anchor=tk.CENTER)
        self.tree.column("locacao_id", width=100, anchor=tk.CENTER)
        self.tree.column("data_multa", width=100, anchor=tk.CENTER)
        self.tree.column("valor", width=100, anchor=tk.E)
        self.tree.column("situacao", width=100, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def atualizar_multas(self):
        # Limpa a árvore antes de adicionar novos itens
        for i in self.tree.get_children():
            self.tree.delete(i)

        try:
            multas = self.db.get_all_multas()
            for multa in multas:
                # Formata o valor para exibição
                valor_formatado = f"R$ {multa[3]:.2f}".replace('.', ',')
                valores_para_treeview = multa[0:3] + (valor_formatado,) + (multa[4],)
                self.tree.insert("", tk.END, values=valores_para_treeview)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar multas: {e}", parent=self)

    def limpar_campos(self):
        self.locacao_id_entry.delete(0, tk.END)
        self.data_multa_entry.delete(0, tk.END)
        self.data_multa_entry.insert(0, date.today().strftime("%d/%m/%Y"))
        self.valor_entry.delete(0, tk.END)
        self.descricao_text.delete(1.0, tk.END)
        self.situacao_combobox.set("Pendente")
        self.locacao_id_entry.focus()

    def cadastra_multa(self):
        """ Pega os dados da interface e envia para o controlador. """
        multa_id = MultaController.cadastrar_multa(
            self,  # Passa a própria instância da view para o Model poder exibir pop-ups
            locacao_id=self.locacao_id_entry.get(),
            data_multa=self.data_multa_entry.get(),
            valor_str=self.valor_entry.get(),
            descricao=self.descricao_text.get(1.0, tk.END).strip(),
            situacao=self.situacao_var.get()
        )
        # Se o cadastro foi bem-sucedido, limpa os campos e atualiza a lista
        if multa_id:
            self.limpar_campos()
            self.atualizar_multas()