

from abc import ABC, abstractmethod  # importa recursos para criar classes abstratas e métodos obrigatórios


class Promocao(ABC):  # cria uma classe abstrata que define o contrato das promoções
    """Contrato: aplicar devolve o valor com desconto."""

    @abstractmethod  # obriga as classes filhas concretas a implementarem esse método
    def aplicar(self, subtotal):  # define o método que toda promoção deve possuir
        ...  # indica que a implementação será feita nas classes filhas


class SemPromocao(Promocao):  # cria uma promoção sem desconto, seguindo o contrato de Promocao
    def aplicar(self, subtotal):  # implementa o método obrigatório da classe pai
        return subtotal  # devolve o valor original, sem aplicar desconto


class Percentual(Promocao):  # cria uma promoção que aplica desconto percentual
    def __init__(self, pct):  # construtor que recebe a porcentagem de desconto
        if not 0 <= pct <= 100:  # verifica se o percentual está entre 0 e 100
            raise ValueError("percentual deve estar entre 0 e 100")  # lança um erro se o percentual for inválido
        self.pct = pct  # armazena o percentual no objeto, como this.pct = pct no JavaScript

    def aplicar(self, subtotal):  # calcula o valor após aplicar o desconto percentual
        return subtotal * (100 - self.pct) / 100  # calcula o preço final descontando a porcentagem informada


class Cupom(Promocao):  # cria uma promoção que desconta um valor fixo
    def __init__(self, valor):  # construtor que recebe o valor do cupom
        if valor < 0:  # verifica se o valor do cupom é negativo
            raise ValueError("valor do cupom não pode ser negativo")  # lança um erro se o valor for inválido
        self.valor = valor  # armazena o valor do cupom no objeto

    def aplicar(self, subtotal):  # calcula o valor após aplicar o cupom
        return max(subtotal - self.valor, 0)  # subtrai o cupom e garante que o resultado nunca seja menor que zero