import tkinter as tk
from tkinter import ttk, messagebox


class Cliente:
    
    @staticmethod
    def salvar(self,nome,cpf,telefone,rua,numero,bairro):

        if not nome or not cpf:
            messagebox.showwarning("Campos Obrigatórios", "Nome e CPF são obrigatórios!", parent=self)
            return

            # Adicione aqui mais validações se necessário (ex: formato do CPF)

            # Supondo que seu db.insert_cliente espera esses argumentos
        cliente_id = self.db.insert_cliente(nome, cpf, telefone, rua, numero, bairro)

        if cliente_id:
            messagebox.showinfo("Sucesso", f"Cliente '{nome}' cadastrado com sucesso!", parent=self)
            return cliente_id
        else:
            messagebox.showerror("Erro de Cadastro", "Falha ao cadastrar cliente. Verifique se o CPF já existe.",
                                 parent=self)

            messagebox.showerror("Erro", "Falha ao cadastrar cliente. Verifique o console para mais detalhes (CPF duplicado?).")
    @staticmethod
    def excluir(self,item):
        if not item:
            messagebox.showwarning("Aviso", "Selecione um cliente para excluir.")
            return

        cliente_id = self.tree.item(item)["values"][0]
        confirm = messagebox.askyesno("Confirmar Exclusão", f"Deseja excluir o cliente ID {cliente_id}?")
        if confirm:
            sucesso = self.db.delete_cliente(cliente_id)
            
            if sucesso:
                messagebox.showinfo("Sucesso", f"Cliente ID {cliente_id} excluído com sucesso.")
            else:
                messagebox.showerror("Erro", "Erro ao excluir cliente. Verifique dependências no banco.")
        return sucesso