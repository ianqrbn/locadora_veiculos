import tkinter as tk
from tkinter import ttk, messagebox
import datetime # Para trabalhar com datas

class FineView(ttk.Frame):
    def __init__(self, parent, db, on_cadastro_success):
        super().__init__(parent)
        self.db = db
        self.on_cadastro_success = on_cadastro_success
        self.criar_widgets()

    def criar_widgets(self):
        form_frame = ttk.LabelFrame(self, text="Dados da Multa")
        form_frame.pack(fill=tk.X, pady=10, padx=10)

        # Campo para o ID da Locação (opcional, ou ID do Veículo)
        ttk.Label(form_frame, text="ID Locação:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.locacao_id_entry = ttk.Entry(form_frame, width=15)
        self.locacao_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        # Nota: Em um sistema mais complexo, você poderia ter uma opção para associar a multa a uma locação OU a um veículo diretamente.

        ttk.Label(form_frame, text="Data da Multa:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.data_multa_entry = ttk.Entry(form_frame, width=15)
        self.data_multa_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.data_multa_entry.insert(0, datetime.date.today().strftime("%d/%m/%Y"))

        ttk.Label(form_frame, text="Valor:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.valor_entry = ttk.Entry(form_frame, width=15)
        self.valor_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Descrição:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.descricao_text = tk.Text(form_frame, width=30, height=4)
        self.descricao_text.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Situação:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.situacao_var = tk.StringVar(self)
        self.situacao_combobox = ttk.Combobox(form_frame, textvariable=self.situacao_var,
                                              values=["Pendente", "Paga", "Contestada"], state="readonly")
        self.situacao_combobox.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        self.situacao_combobox.set("Pendente") # Valor padrão


        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10, padx=10, fill=tk.X)

        ttk.Button(btn_frame, text="Salvar Multa", command=self.cadastrar_multa).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar_campos).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Fechar", command=self.limpar_e_ocultar).pack(side=tk.RIGHT, padx=5)

        self.tree = ttk.Treeview(self, columns=("id", "locacao_id", "data_multa", "valor", "situacao"), show="headings")
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

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.atualizar_multas()

    def atualizar_multas(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        try:
            multas = self.db.get_all_multas()  
            for loc in multas:
                self.tree.insert("", tk.END, values=loc[:5])  # Exibe os primeiros 5 campos
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar locações: {e}")

    def limpar_campos(self):
        self.locacao_id_entry.delete(0, tk.END)
        self.data_multa_entry.delete(0, tk.END)
        self.data_multa_entry.insert(0, datetime.date.today().strftime("%d/%m/%Y"))
        self.valor_entry.delete(0, tk.END)
        self.descricao_text.delete(1.0, tk.END)
        self.situacao_combobox.set("Pendente")

    def limpar_e_ocultar(self):
        self.limpar_campos()
        self.pack_forget()

    def cadastrar_multa(self):
        dados = {
            "locacao_id": self.locacao_id_entry.get(),
            "data_multa": self.data_multa_entry.get(),
            "valor": self.valor_entry.get(),
            "descricao": self.descricao_text.get(1.0, tk.END).strip(),
            "situacao": self.situacao_var.get()
        }

        # Validação básica
        if not all([dados["locacao_id"], dados["data_multa"], dados["valor"], dados["descricao"]]):
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios!")
            return

        # Validação de data
        try:
            datetime.datetime.strptime(dados["data_multa"], "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erro de Data", "Formato de data inválido. Use DD/MM/AAAA.")
            return

        # Validação de valor
        try:
            float(dados["valor"])
        except ValueError:
            messagebox.showerror("Erro de Valor", "O valor da multa deve ser um número.")
            return

        # Simula sucesso no cadastro
        messagebox.showinfo("Sucesso", "Multa cadastrada com sucesso!")
        if self.on_cadastro_success:
            self.on_cadastro_success()