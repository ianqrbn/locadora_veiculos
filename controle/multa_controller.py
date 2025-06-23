# Conteúdo para o novo arquivo controle/multa_controller.py

from modelo.multa import Multa

class MultaController:
    @staticmethod
    def cadastrar_multa(view_instance, locacao_id, data_multa, valor_str, descricao, situacao):
        """Pede ao Modelo para cadastrar a multa."""
        return Multa.cadastrar(view_instance, locacao_id, data_multa, valor_str, descricao, situacao)