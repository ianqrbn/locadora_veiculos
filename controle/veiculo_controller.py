from modelo.veiculo import Veiculo

class VeiculoController:
    
    def cadastrar_veiculo(self,marca,modelo,ano_str,placa,cor):
        return Veiculo.cadastar(self,marca,modelo,ano_str,placa,cor)
    
    def excluir_veiculo(self, selecionado):
        return Veiculo.excluir(self,selecionado)