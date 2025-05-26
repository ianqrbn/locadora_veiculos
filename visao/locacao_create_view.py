import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime


class RentalView(ttk.Frame):
    def __init__(self, parent, controller, db, on_success_callback):
        super().__init__(parent)
        self.controller = controller
        self.db = db
        self.on_success_callback = on_success_callback

        # Dicionários para mapear o texto da Combobox para o ID do banco de dados
        self.clientes_map = {}
        self.veiculos_map = {}
        self.criar_widgets()
        self.load_combobox_data()
        self.atualizar_locacoes()

    def criar_widgets(self):
        # Frame principal para o formulário
        form_frame = ttk.LabelFrame(self, text="Dados da Locação")
        form_frame.pack(fill=tk.X, pady=10, padx=10)

        # --- Seleção de Cliente ---
        ttk.Label(form_frame, text="Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.combo_cliente = ttk.Combobox(form_frame, state="readonly", width=40)
        self.combo_cliente.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        # --- Seleção de Veículo Disponível ---
        ttk.Label(form_frame, text="Veículo Disponível:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.combo_veiculo = ttk.Combobox(form_frame, state="readonly", width=40)
        self.combo_veiculo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        # --- Outros campos do formulário ---
        ttk.Label(form_frame, text="Data de Início:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.data_inicio_entry = ttk.Entry(form_frame, width=15)
        self.data_inicio_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.data_inicio_entry.insert(0, date.today().strftime("%d/%m/%Y"))

        ttk.Label(form_frame, text="Data Prev. Fim:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.data_prev_fim_entry = ttk.Entry(form_frame, width=15)
        self.data_prev_fim_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Valor Diária (R$):").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.valor_diaria_entry = ttk.Entry(form_frame, width=15)
        self.valor_diaria_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Observações:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.obs_text = tk.Text(form_frame, width=40, height=4)
        self.obs_text.grid(row=5, column=1, rowspan=2, padx=5, pady=5, sticky=tk.EW)

        form_frame.columnconfigure(1, weight=1)  # Permite que a coluna das entradas expanda

        # --- Botões de Ação ---
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10, padx=10, fill=tk.X)
        ttk.Button(btn_frame, text="Salvar Locação", command=self.cadastrar_locacao).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar_campos).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Excluir Locação", command=self.excluir_locacao).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Fechar", command=lambda: self.on_success_callback("Operação cancelada.")).pack(
            side=tk.RIGHT, padx=5)

        # --- Treeview para listar locações existentes ---
        tree_frame = ttk.LabelFrame(self, text="Locações Ativas")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tree_columns = ("id", "cliente", "placa", "inicio", "fim", "diaria", "status")
        self.tree = ttk.Treeview(tree_frame, columns=tree_columns, show="headings")

        # Define os cabeçalhos
        self.tree.heading("id", text="ID")
        self.tree.heading("cliente", text="Cliente")
        self.tree.heading("placa", text="Veículo (Placa)")
        self.tree.heading("inicio", text="Data Início")
        self.tree.heading("fim", text="Data Prev. Fim")
        self.tree.heading("diaria", text="Valor Diária")
        self.tree.heading("status", text="Status")

        # Define a largura das colunas
        self.tree.column("id", width=40, anchor=tk.CENTER)
        self.tree.column("cliente", width=200, anchor=tk.W)
        self.tree.column("placa", width=100, anchor=tk.W)
        self.tree.column("inicio", width=100, anchor=tk.CENTER)
        self.tree.column("fim", width=100, anchor=tk.CENTER)
        self.tree.column("diaria", width=80, anchor=tk.E)
        self.tree.column("status", width=80, anchor=tk.W)

        # Adiciona uma barra de rolagem
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def load_combobox_data(self):
        """Carrega dados dos clientes e veículos disponíveis para as caixas de seleção."""
        try:
            # Carrega clientes
            self.clientes_map.clear()
            clientes = self.db.get_all_clientes()
            cliente_display_list = []
            for c in clientes:  # c é (id, nome, cpf)
                display_text = f"{c[1]} (CPF: {c[2]})"
                self.clientes_map[display_text] = c[0]
                cliente_display_list.append(display_text)
            self.combo_cliente['values'] = cliente_display_list

            # Carrega veículos disponíveis
            self.veiculos_map.clear()
            veiculos = self.db.get_available_veiculos()
            veiculo_display_list = []
            for v in veiculos:  # v é (id, marca, modelo, placa)
                display_text = f"{v[1]} {v[2]} (Placa: {v[3]})"
                self.veiculos_map[display_text] = v[0]
                veiculo_display_list.append(display_text)
            self.combo_veiculo['values'] = veiculo_display_list
        except Exception as e:
            messagebox.showerror("Erro de Carregamento", f"Erro ao carregar dados para os formulários: {e}",
                                 parent=self)

    def atualizar_locacoes(self):
        """Limpa e recarrega a lista de locações na Treeview."""
        for i in self.tree.get_children():
            self.tree.delete(i)
        try:
            locacoes = self.db.get_all_locacoes()
            if locacoes:
                for loc in locacoes:
                    # Formata o valor da diária como moeda
                    valor_formatado = f"R$ {loc[5]:.2f}".replace('.', ',')
                    # Cria a tupla de valores para inserir na Treeview
                    valores_para_treeview = loc[0:5] + (valor_formatado,) + (loc[6],)
                    self.tree.insert("", tk.END, values=valores_para_treeview)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar locações: {e}", parent=self)

    def limpar_campos(self):
        """Limpa todos os campos de entrada do formulário."""
        self.combo_cliente.set('')
        self.combo_veiculo.set('')
        self.data_inicio_entry.delete(0, tk.END)
        self.data_inicio_entry.insert(0, date.today().strftime("%d/%m/%Y"))
        self.data_prev_fim_entry.delete(0, tk.END)
        self.valor_diaria_entry.delete(0, tk.END)
        self.obs_text.delete(1.0, tk.END)
        self.combo_cliente.focus()

    def cadastrar_locacao(self):
        """Valida e salva a locação com todos os dados vinculados."""
        # Obter ID do Funcionário
        try:
            funcionario_id = self.controller.logged_in_user[0]
        except (AttributeError, TypeError, IndexError):
            messagebox.showerror("Erro Crítico",
                                 "Não foi possível identificar o funcionário logado. Faça login novamente.",
                                 parent=self)
            return

        # Obter IDs do Cliente e Veículo
        cliente_selecionado = self.combo_cliente.get()
        veiculo_selecionado = self.combo_veiculo.get()

        if not cliente_selecionado or not veiculo_selecionado:
            messagebox.showwarning("Aviso", "Por favor, selecione um cliente e um veículo.", parent=self)
            return
        cliente_id = self.clientes_map[cliente_selecionado]
        veiculo_id = self.veiculos_map[veiculo_selecionado]

        # Obter e validar outros dados do formulário
        data_inicio = self.data_inicio_entry.get()
        data_prev_fim = self.data_prev_fim_entry.get()
        valor_diaria_str = self.valor_diaria_entry.get().replace(',', '.')  # Aceita vírgula
        observacoes = self.obs_text.get("1.0", tk.END).strip()

        if not all([data_inicio, data_prev_fim, valor_diaria_str]):
            messagebox.showwarning("Aviso", "Preencha as datas e o valor da diária!", parent=self)
            return

        try:
            # Validação de datas
            datetime.strptime(data_inicio, "%d/%m/%Y")
            datetime.strptime(data_prev_fim, "%d/%m/%Y")
            # Validação do valor
            valor_diaria = float(valor_diaria_str)
        except ValueError:
            messagebox.showerror("Erro de Formato", "Verifique o formato da data (DD/MM/AAAA) ou do valor monetário.",
                                 parent=self)
            return

        # Salvar no Banco de Dados
        locacao_id = self.db.insert_locacao(
            cliente_id=cliente_id,
            veiculo_id=veiculo_id,
            funcionario_id=funcionario_id,
            data_inicio=data_inicio,
            data_prev_fim=data_prev_fim,
            valor_diaria=valor_diaria,
            observacoes=observacoes
        )

        if locacao_id:
            # Atualiza o status do veículo para 'ALUGADO'
            self.db.update_veiculo_status(veiculo_id, 'ALUGADO')

            messagebox.showinfo("Sucesso", f"Locação ID {locacao_id} cadastrada com sucesso!", parent=self)

            # Limpa e atualiza a tela
            self.limpar_campos()
            self.load_combobox_data()
            self.atualizar_locacoes()
        else:
            messagebox.showerror("Erro", "Falha ao cadastrar locação no banco de dados.", parent=self)
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
                self.db.update_veiculo_status(locacao_id, 'DISPONIVEL')
                messagebox.showinfo("Sucesso", f"Locação ID {locacao_id} excluída com sucesso.")
                # TODO: atualizar a pagina

            else:
                messagebox.showerror("Erro", "Falha ao excluir a locação. Verifique o console.")

