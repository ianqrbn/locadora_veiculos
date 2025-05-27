from tkinter import ttk, messagebox

class Veiculo:

    def cadastar(self,marca,modelo,ano_str,placa,cor):
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
            return veiculo_id
        else:
            messagebox.showerror("Erro",
                                 "Falha ao cadastrar veículo. Verifique o console para mais detalhes (placas duplicadas?).")

    def excluir(self,selecionado):
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
                return sucesso
            else:
                messagebox.showerror("Erro", "Falha ao excluir veículo!")



