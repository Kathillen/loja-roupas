# Uso uma tupla para guardar os tamanhos permitidos, já que ela é imutável
TAMANHOS = ("PP", "P", "M", "G", "GG")


class Produto:
    def __init__(self, nome, preco, tamanho):
        # Valido os dados antes de criar o produto
        if not nome or not nome.strip():
            raise ValueError("Nome do produto não pode ser vazio")
        if preco <= 0:
            raise ValueError("preço deve ser maior que zero")
        if tamanho.upper() not in TAMANHOS:
            raise ValueError(f"tamanho inválido: {tamanho}")

        self.nome = nome.strip()
        self.preco = preco
        self.tamanho = tamanho

    def descricao(self):
        return f"{self.nome} {self.tamanho}: R$ {self.preco:.2f}"

    def para_dict(self):
        """Transformo os dados do produto em um dicionário, pronto para virar JSON."""
        return {
            "tipo": type(self).__name__,
            "nome": self.nome,
            "preco": self.preco,
            "tamanho": self.tamanho,
        }


class Camiseta(Produto):
    MANGAS = ("curta", "longa")

    def __init__(self, nome, preco, tamanho, manga):
        # Reaproveito as validações e os atributos da classe Produto
        super().__init__(nome, preco, tamanho)

        if manga not in self.MANGAS:
            raise ValueError(f"manga inválida: {manga}")
        self.manga = manga

    def descricao(self):
        return f"{super().descricao()} · manga {self.manga}"

    def para_dict(self):
        # Aproveito os dados do produto e acrescento a manga
        dados = super().para_dict()
        dados["tipo"] = "camiseta"
        dados["manga"] = self.manga
        return dados

class Calca(Produto):
    def __init__(self, nome, preco, tamanho, modelagem):
        # Reaproveito as validações e os atributos da classe Produto
        super().__init__(nome, preco, tamanho)
        self.modelagem = modelagem

    def descricao(self):
        return f"{super().descricao()} · {self.modelagem}"

    def para_dict(self):
        # Aproveito os dados do produto e acrescento a modelagem
        dados = super().para_dict()
        dados["modelagem"] = self.modelagem
        return dados
