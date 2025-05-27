from modelo.locacao import locacao

class LocacaoController:

    def cadastrar_locacao(self, cliente_selecionado,veiculo_selecionado,data_inicio,data_prev_fim,valor_diaria_str,observacoes):
        return locacao.cadastrar(self, cliente_selecionado,veiculo_selecionado,data_inicio,data_prev_fim,valor_diaria_str,observacoes)

    def excluir_locacao(self,item_selecionado,locacao_id):
        return locacao.excluir(self,item_selecionado,locacao_id)