from tkinter import ttk, messagebox
from datetime import date, datetime

class locacao:

    def cadastrar(self, cliente_selecionado,veiculo_selecionado,data_inicio,data_prev_fim,valor_diaria_str,observacoes):
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

        if not cliente_selecionado or not veiculo_selecionado:
            messagebox.showwarning("Aviso", "Por favor, selecione um cliente e um veículo.", parent=self)
            return
        cliente_id = self.clientes_map[cliente_selecionado]
        veiculo_id = self.veiculos_map[veiculo_selecionado]

        # Obter e validar outros dados do formulário
    

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
            return locacao_id
        else:
            messagebox.showerror("Erro", "Falha ao cadastrar locação no banco de dados.", parent=self)


    def excluir(self,item_selecionado,locacao_id):
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione uma locação para excluir.")
            return
        confirmacao = messagebox.askyesno("Confirmação", f"Deseja realmente excluir a locação ID {locacao_id}?")
        if confirmacao:
            sucesso = self.db.delete_locacao(locacao_id)
            if sucesso:
                self.db.update_veiculo_status(locacao_id, 'DISPONIVEL')
                messagebox.showinfo("Sucesso", f"Locação ID {locacao_id} excluída com sucesso.")
                # TODO: atualizar a pagina
                return sucesso
            else:
                messagebox.showerror("Erro", "Falha ao excluir a locação. Verifique o console.")