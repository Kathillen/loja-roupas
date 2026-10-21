
"""Etapa 14: as regras do catálogo, sem saber de HTTP nem de banco (Aula 10)."""
from loja.produto import Calca, Camiseta, Produto


# Crio exceções específicas para identificar os erros do catálogo
class ProdutoNaoEncontrado(Exception):
    pass  # Uso pass porque a classe serve apenas para representar esse erro


class ProdutoJaExiste(Exception):
    pass


class DadosInvalidos(Exception):
    pass


def criar_produto(dados):
    """Dicionário -> objeto do domínio. Erros de validação viram DadosInvalidos."""

    try:
        # Uso get() para obter o tipo e definir "Produto" como padrão se não existir
        # JavaScript: dados.tipo ?? "Produto"
        tipo = dados.get("tipo", "Produto")

        # Crio o objeto da classe correspondente ao tipo informado
        if tipo == "Camiseta":
            return Camiseta(
                dados["nome"], dados["preco"], dados["tamanho"],
                dados.get("manga")
            )

        if tipo == "Calca":
            # Verifico se a modelagem foi informada, pois ela é obrigatória para calças
            if not dados.get("modelagem"):
                raise ValueError("calça precisa de modelagem")

            return Calca(
                dados["nome"], dados["preco"], dados["tamanho"],
                dados["modelagem"]
            )

        if tipo == "Produto":
            return Produto(dados["nome"], dados["preco"], dados["tamanho"])

        # Uso raise para interromper a execução quando o tipo não é reconhecido
        raise ValueError(f"tipo inválido: {tipo}")

    # Capturo erros de validação e chaves obrigatórias ausentes no dicionário
    except (ValueError, KeyError) as erro:
        # Transformo os erros em DadosInvalidos para padronizar as falhas do catálogo
        # from erro mantém a exceção original como causa do novo erro
        # JavaScript: throw new Error("...", { cause: erro })
        raise DadosInvalidos(str(erro)) from erro


def com_id(produto_id, produto):
    # Uno o ID aos dados do produto para devolver tudo em um único dicionário
    # ** desempacota as chaves de para_dict() dentro do novo dicionário
    # JavaScript: { id: produto_id, ...produto.para_dict() }
    return {"id": produto_id, **produto.para_dict()}


class ServicoCatalogo:
    """Recebe o repositório pronto: não sabe se o banco é SQLite, MySQL ou memória."""

    def __init__(self, repositorio):
        # Recebo o repositório pronto e guardo para usar nos outros métodos
        self.repositorio = repositorio

    def listar(self, tamanho=None, preco_max=None):
        # Listo os produtos com os filtros informados e adiciono o ID a cada um
        # A compreensão de lista percorre os pares (ID, produto) retornados pelo repositório
        # JavaScript: array.map(([id, produto]) => comId(id, produto))
        return [
            com_id(i, p)
            for i, p in self.repositorio.listar(tamanho, preco_max)
        ]

    def produto(self, produto_id):
        # Busco o produto pelo ID no repositório
        produto = self.repositorio.buscar(produto_id)

        # Se não encontrar, lanço uma exceção específica para esse caso
        if produto is None:
            raise ProdutoNaoEncontrado(
                f"produto {produto_id} não encontrado"
            )

        return produto

    def buscar(self, produto_id):
        # Busco o produto e devolvo seus dados junto com o ID
        return com_id(produto_id, self.produto(produto_id))

    def cadastrar(self, dados):
        # Valido os dados e transformo o dicionário em um objeto de produto
        produto = criar_produto(dados)

        # Impedo o cadastro se já existir outro produto com o mesmo nome
        if self.repositorio.existe_nome(produto.nome):
            raise ProdutoJaExiste(
                f"já existe um produto chamado {produto.nome}"
            )

        # Salvo o produto e devolvo os dados com o ID gerado pelo banco
        return com_id(self.repositorio.adicionar(produto), produto)

    def atualizar(self, produto_id, dados):
        # Verifico primeiro se o produto existe para evitar atualizar um ID inválido
        self.produto(produto_id)

        # Transformo os novos dados em um objeto e valido suas regras
        produto = criar_produto(dados)

        # Verifico se o nome já pertence a outro produto, ignorando o próprio ID
        if self.repositorio.existe_nome(
            produto.nome, exceto_id=produto_id
        ):
            raise ProdutoJaExiste(
                f"já existe um produto chamado {produto.nome}"
            )

        # Atualizo o produto no repositório e devolvo os dados atualizados
        self.repositorio.atualizar(produto_id, produto)
        return com_id(produto_id, produto)

    def remover(self, produto_id):
        # Tento remover o produto e verifico se a operação foi realizada
        if not self.repositorio.remover(produto_id):
            # Lanço um erro se o repositório informar que o produto não existe
            raise ProdutoNaoEncontrado(
                f"produto {produto_id} não encontrado"
            )
