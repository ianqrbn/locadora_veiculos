from modelo.funcionario import Funcionario

class FuncionarioController:

    def salvar_funcionario(self,nome,email,cpf,funcao,status_texto):
        return Funcionario.salvar(self,nome,email,cpf,funcao,status_texto)