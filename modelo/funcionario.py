from tkinter import ttk, messagebox

class Funcionario:

    def salvar(self,nome,email,cpf,funcao,status_texto):

        status_booleano = 1 if status_texto == "Ativo" else 0

        if not all([nome, email, cpf, funcao]):
            messagebox.showwarning("Campos Obrigatórios", "Nome, E-mail, CPF e Função são obrigatórios!", parent=self)
            return

        # Adicione aqui mais validações se necessário (ex: formato do CPF, e-mail)

        sucesso = self.db.insert_funcionario(nome, email, cpf, funcao, status_booleano)

        if sucesso:
            messagebox.showinfo("Sucesso", f"Funcionário '{nome}' cadastrado com sucesso!", parent=self)
        else:
            messagebox.showerror("Erro de Cadastro",
                                 "Falha ao cadastrar funcionário. Verifique se o E-mail ou CPF já existem.",
                                 parent=self)
