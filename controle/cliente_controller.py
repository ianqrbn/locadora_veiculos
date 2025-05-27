from modelo.cliente import Cliente
    
class ClienteController:
    @staticmethod
    def salvar_cliente(self,nome,cpf,telefone,rua,numero,bairro):
        return Cliente.salvar(self,nome,cpf,telefone,rua,numero,bairro)
    
    @staticmethod
    def excluir_cliente(self,item):
        return Cliente.excluir(self,item)