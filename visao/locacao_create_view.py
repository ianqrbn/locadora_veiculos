import tkinter as tk
from tkinter import ttk, messagebox
import datetime # Para trabalhar com datas

class RentalView(ttk.Frame):
    def __init__(self, parent, db, on_cadastro_success):
        super().__init__(parent)
        self.db = db
        self.on_cadastro_success = on_cadastro_success
        self.criar_widgets()

    def criar_widgets(self):
        form_frame = ttk.LabelFrame(self, text="Dados da Locação")
        form_frame.pack(fill=tk.X, pady=10, padx=10)

        # Campo para o ID do Cliente (simplificado para demonstração)
        ttk.Label(form_frame, text="ID Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.cliente_id_entry = ttk.Entry(form_frame, width=15)
        self.cliente_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        # Nota: Em um sistema real, aqui você teria um botão para buscar/selecionar um cliente da base de dados.

        # Campo para o ID do Veículo (simplificado para demonstração)
        ttk.Label(form_frame, text="ID Veículo:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.veiculo_id_entry = ttk.Entry(form_frame, width=15)
        self.veiculo_id_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        # Nota: Similar ao cliente, um botão para buscar/selecionar um veículo.

        ttk.Label(form_frame, text="Data de Início:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.data_inicio_entry = ttk.Entry(form_frame, width=15)
        self.data_inicio_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.data_inicio_entry.insert(0, datetime.date.today().strftime("%d/%m/%Y")) # Preenche com a data atual

        ttk.Label(form_frame, text="Data Prev. Fim:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.data_prev_fim_entry = ttk.Entry(form_frame, width=15)
        self.data_prev_fim_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Valor Diária:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.valor_diaria_entry = ttk.Entry(form_frame, width=15)
        self.valor_diaria_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Observações:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.obs_text = tk.Text(form_frame, width=30, height=4)
        self.obs_text.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)


        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10, padx=10, fill=tk.X)

        ttk.Button(btn_frame, text="Salvar Locação", command=self.cadastrar_locacao).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar_campos).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Excluir Locação", command=self.excluir_locacao).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Fechar", command=self.limpar_e_ocultar).pack(side=tk.RIGHT, padx=5)

        self.tree = ttk.Treeview(self, columns=("id", "cliente_id", "veiculo_id", "data_inicio", "data_prev_fim", "valor_diaria"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("cliente_id", text="Cliente ID")
        self.tree.heading("veiculo_id", text="Veículo ID")
        self.tree.heading("data_inicio", text="Data Início")
        self.tree.heading("data_prev_fim", text="Data Prev. Fim")
        self.tree.heading("valor_diaria", text="Valor Diária")
        self.tree.column("id", width=40)
        self.tree.column("cliente_id", width=80)
        self.tree.column("veiculo_id", width=80)
        self.tree.column("data_inicio", width=100)
        self.tree.column("data_prev_fim", width=110)
        self.tree.column("valor_diaria", width=100)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.atualizar_locacoes()


    def atualizar_locacoes(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        try:
            locacoes = self.db.get_all_locacoes()  
            for loc in locacoes:
                self.tree.insert("", tk.END, values=loc[:6])  # Exibe os primeiros 6 campos
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar locações: {e}")

    def limpar_campos(self):
        self.cliente_id_entry.delete(0, tk.END)
        self.veiculo_id_entry.delete(0, tk.END)
        self.data_inicio_entry.delete(0, tk.END)
        self.data_inicio_entry.insert(0, datetime.date.today().strftime("%d/%m/%Y")) # Reseta para data atual
        self.data_prev_fim_entry.delete(0, tk.END)
        self.valor_diaria_entry.delete(0, tk.END)
        self.obs_text.delete(1.0, tk.END) # Para Text widget, use 1.0 para o início

    def limpar_e_ocultar(self):
        self.limpar_campos()
        self.pack_forget()

    def cadastrar_locacao(self):
        dados = {
            "cliente_id": self.cliente_id_entry.get(),
            "veiculo_id": self.veiculo_id_entry.get(),
            "data_inicio": self.data_inicio_entry.get(),
            "data_prev_fim": self.data_prev_fim_entry.get(),
            "valor_diaria": self.valor_diaria_entry.get(),
            "observacoes": self.obs_text.get(1.0, tk.END).strip()
        }

        # Validação básica
        if not all([dados["cliente_id"], dados["veiculo_id"], dados["data_inicio"], dados["data_prev_fim"], dados["valor_diaria"]]):
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios (ID Cliente, ID Veículo, Datas, Valor Diária)!")
            return

        # Validação de datas (exemplo simples)
        try:
            # Tenta converter para verificar se são datas válidas
            datetime.datetime.strptime(dados["data_inicio"], "%d/%m/%Y")
            datetime.datetime.strptime(dados["data_prev_fim"], "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erro de Data", "Formato de data inválido. Use DD/MM/AAAA.")
            return

        # Validação de valor (exemplo simples)
        try:
            float(dados["valor_diaria"])
        except ValueError:
            messagebox.showerror("Erro de Valor", "O valor da diária deve ser um número.")
            return

            # Converte IDs para int, pois no BD são INTEGERS
        try:
            cliente_id = int(dados["cliente_id"])
            veiculo_id = int(dados["veiculo_id"])
            valor_diaria = float(dados["valor_diaria"])
        except ValueError:
            messagebox.showerror("Erro de Tipo", "ID Cliente, ID Veículo e Valor Diária devem ser números válidos.")
            return

        locacao_id = self.db.insert_locacao(
            cliente_id,
            veiculo_id,
            dados["data_inicio"],
            dados["data_prev_fim"],
            valor_diaria,
            dados["observacoes"]
        )

        if locacao_id:
            messagebox.showinfo("Sucesso", f"Locação cadastrada com sucesso! (ID: {locacao_id})")
            if self.on_cadastro_success:
                self.on_cadastro_success()
        else:
            messagebox.showerror("Erro",
                                 "Falha ao cadastrar locação. Verifique o console para mais detalhes (IDs de cliente/veículo existentes?).")
    def carregar_locacoes(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        locacoes = self.db.get_all_locacoes()
        for locacao in locacoes:
            self.tree.insert("", "end", values=locacao)

    def excluir_locacao(self):
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione uma locação para excluir.")
            return

        locacao_id = self.tree.item(item_selecionado)["values"][0]

        confirmacao = messagebox.askyesno("Confirmação", f"Deseja realmente excluir a locação ID {locacao_id}?")
        if confirmacao:
            sucesso = self.db.delete_locacao(locacao_id)
            if sucesso:
                self.carregar_locacoes()
                messagebox.showinfo("Sucesso", f"Locação ID {locacao_id} excluída com sucesso.")
            else:
                messagebox.showerror("Erro", "Falha ao excluir a locação. Verifique o console.")
            