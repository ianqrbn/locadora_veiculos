import tkinter as tk
from tkinter import ttk, messagebox


class VehicleView(ttk.Frame):
    def __init__(self, parent, db, on_cadastro_success):
        super().__init__(parent)
        self.db = db
        self.on_cadastro_success = on_cadastro_success
        self.criar_widgets()

    def criar_widgets(self):
        form_frame = ttk.LabelFrame(self, text="Dados do Veículo")
        form_frame.pack(fill=tk.X, pady=10, padx=10)

        ttk.Label(form_frame, text="Marca:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.marca_entry = ttk.Entry(form_frame, width=40)
        self.marca_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Modelo:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.modelo_entry = ttk.Entry(form_frame, width=40)
        self.modelo_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Ano:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.ano_entry = ttk.Entry(form_frame, width=15)
        self.ano_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Placa:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.placa_entry = ttk.Entry(form_frame, width=15)
        self.placa_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Cor:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.cor_entry = ttk.Entry(form_frame, width=15)
        self.cor_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10, padx=10, fill=tk.X)

        ttk.Button(btn_frame, text="Salvar", command=self.cadastrar_veiculo).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar_campos).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Fechar", command=self.limpar_e_ocultar).pack(side=tk.RIGHT, padx=5)

        # --- Treeview para exibir a lista de veículos ---
        self.tree = ttk.Treeview(self, columns=("ID", "Marca", "Modelo", "Ano", "Placa", "Cor"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Marca", text="Marca")
        self.tree.heading("Modelo", text="Modelo")
        self.tree.heading("Ano", text="Ano")
        self.tree.heading("Placa", text="Placa")
        self.tree.heading("Cor", text="Cor")
        self.tree.column("ID", width=40, anchor=tk.CENTER)
        self.tree.column("Marca", width=120)
        self.tree.column("Modelo", width=120)
        self.tree.column("Ano", width=60, anchor=tk.CENTER)
        self.tree.column("Placa", width=100)
        self.tree.column("Cor", width=80)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.atualizar_lista_veiculos()


    def atualizar_lista_veiculos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        veiculos = self.db.get_all_veiculos()
        for veiculo in veiculos:
            veiculo_id, marca, modelo, ano, placa, cor, *_ = veiculo
            self.tree.insert("", tk.END, values=(veiculo_id, marca, modelo, ano, placa, cor))

    def limpar_campos(self):
        self.marca_entry.delete(0, tk.END)
        self.modelo_entry.delete(0, tk.END)
        self.ano_entry.delete(0, tk.END)
        self.placa_entry.delete(0, tk.END)
        self.cor_entry.delete(0, tk.END)

    def limpar_e_ocultar(self):
        self.limpar_campos()
        self.pack_forget()

    def cadastrar_veiculo(self):
        dados = {
            "marca": self.marca_entry.get(),
            "modelo": self.modelo_entry.get(),
            "ano": self.ano_entry.get(),
            "placa": self.placa_entry.get(),
            "cor": self.cor_entry.get()
        }

        if not all(dados.values()):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        veiculo_id = self.db.insert_veiculo(dados["marca"], dados["modelo"], dados["ano"], dados["placa"], dados["cor"])

        if veiculo_id:
            messagebox.showinfo("Sucesso", f"Veículo cadastrado com sucesso! (ID: {veiculo_id})")
            if self.on_cadastro_success:
                self.on_cadastro_success()
        else:
            messagebox.showerror("Erro",
                                 "Falha ao cadastrar veículo. Verifique o console para mais detalhes (placas duplicadas?).")