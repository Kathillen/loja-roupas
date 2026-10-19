from .calculos import frete, total_carrinho  # importa as funções que calculam o frete e o subtotal do carrinho
from .produto import Produto  # importa a classe Produto para verificar se o item é um produto válido
from .promocao import Promocao, SemPromocao  # importa o contrato de promoção e a classe que não aplica desconto


class CarrinhoFinalizadoError(Exception):  # cria um erro personalizado para situações em que o carrinho já foi finalizado
    """Levantada ao mexer num carrinho já finalizado."""


class Carrinho:  # cria a classe que representa o carrinho de compras
    def __init__(self, promocao=None):  # construtor; recebe uma promoção opcional, como um constructor no JavaScript
        self._itens = []  # cria uma lista vazia para guardar pares de produto e quantidade
        self._finalizado = False  # indica que o carrinho começa aberto, ainda não foi finalizado

        promocao = promocao or SemPromocao()  # se nenhuma promoção for informada, usa SemPromocao como padrão

        if not isinstance(promocao, Promocao):  # verifica se a promoção segue o contrato da classe Promocao
            raise TypeError("a promoção precisa seguir o contrato Promocao")  # lança um erro se o objeto não for uma promoção válida

        self.promocao = promocao  # guarda a promoção escolhida no carrinho

    def adicionar(self, produto, quantidade=1):  # método para adicionar um produto ao carrinho; a quantidade padrão é 1
        if self._finalizado:  # verifica se o carrinho já foi finalizado
            raise CarrinhoFinalizadoError("carrinho finalizado não recebe peças")  # impede adicionar produtos depois da finalização

        if not isinstance(produto, Produto):  # verifica se o objeto recebido pertence à classe Produto ou a uma classe filha
            raise TypeError("só é possível adicionar um Produto")  # lança um erro se não for um produto válido

        if quantidade <= 0:  # verifica se a quantidade informada é zero ou negativa
            raise ValueError("quantidade deve ser positiva")  # impede adicionar quantidades inválidas

        self._itens.append((produto, quantidade))  # adiciona uma tupla com o produto e sua quantidade à lista do carrinho

    @property  # transforma o método abaixo em uma propriedade, permitindo acessar carrinho.itens sem usar parênteses
    def itens(self):
        return list(self._itens)  # retorna uma cópia da lista para evitar que alterem diretamente a lista interna

    @property  # permite acessar a quantidade_de_pecas como um atributo calculado
    def quantidade_de_pecas(self):
        return sum(quantidade for _, quantidade in self._itens)  # soma as quantidades de todos os produtos do carrinho; _ ignora o produto

    @property  # permite acessar o subtotal como um atributo, sem chamar subtotal()
    def subtotal(self):
        return total_carrinho([(p.preco, q) for p, q in self._itens])  # cria pares de preço e quantidade e calcula o subtotal sem frete ou desconto

    @property  # permite acessar o total como um atributo calculado
    def total(self):
        com_desconto = self.promocao.aplicar(self.subtotal)  # chama a promoção escolhida para calcular o valor com desconto; isso é polimorfismo
        return com_desconto + frete(com_desconto)  # soma o valor com desconto ao frete calculado sobre esse valor

    def finalizar(self):
        if not self._itens:
            raise ValueError("não é possível finalizar um carrinho vazio")
    
        self._finalizado = True