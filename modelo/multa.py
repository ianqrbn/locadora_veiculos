# Conteúdo para o novo arquivo modelo/multa.py

from tkinter import messagebox
from datetime import datetime

class Multa:
    @staticmethod
    def cadastrar(view_instance, locacao_id, data_multa, valor_str, descricao, situacao):
        """ Valida os dados e chama o método do DB para inserir a multa. """
        if not all([locacao_id, data_multa, valor_str, descricao]):
            messagebox.showwarning("Campos Obrigatórios", "Todos os campos, exceto Situação, são obrigatórios!", parent=view_instance)
            return None

        try:
            # Valida o formato da data
            datetime.strptime(data_multa, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erro de Formato", "O formato da data deve ser DD/MM/AAAA.", parent=view_instance)
            return None

        try:
            # Valida e converte o valor monetário
            valor = float(valor_str.replace(',', '.'))
        except ValueError:
            messagebox.showerror("Erro de Formato", "O valor da multa deve ser um número válido.", parent=view_instance)
            return None

        # Chama o método do banco de dados para inserir
        multa_id = view_instance.db.insert_multa(locacao_id, data_multa, valor, descricao, situacao)

        if multa_id:
            messagebox.showinfo("Sucesso", f"Multa ID {multa_id} cadastrada com sucesso!", parent=view_instance)
            return multa_id
        else:
            messagebox.showerror("Erro", "Falha ao cadastrar multa no banco de dados.", parent=view_instance)
            return None