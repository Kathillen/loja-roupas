
from sqlmodel import Session, select

from loja.banco import ProdutoRegistro
from loja.produto import Calca, Camiseta, Produto

# Guardo os campos que podem ser atualizados
CAMPOS = ("tipo", "nome", "preco", "tamanho", "manga", "modelagem")


def para_dominio(registro):
    # Converto o registro para a classe correspondente ao tipo salvo
    if registro.tipo == "camiseta":
        return Camiseta(registro.nome, registro.preco, registro.tamanho, registro.manga)

    if registro.tipo == "calca":
        return Calca(registro.nome, registro.preco, registro.tamanho, registro.modelagem)

    return Produto(registro.nome, registro.preco, registro.tamanho)
def para_registro(produto):
    # Transformo os dados do produto em um dicionário para criar o registro
    # ** desempacota o dicionário em argumentos nomeados
    # JavaScript: { ...produto.para_dict() } cria uma cópia do objeto
    return ProdutoRegistro(**produto.para_dict())


class RepositorioProdutos:

    def __init__(self, sessao: Session):
        self.sessao = sessao  # Guardo a sessão do banco para usar nos métodos

    def adicionar(self, produto):
        registro = para_registro(produto)
        self.sessao.add(registro)
        self.sessao.commit()           # Confirmo a gravação no banco
        self.sessao.refresh(registro)  # Atualizo o objeto com os dados gerados pelo banco
        return registro.id

    def buscar(self, produto_id):
        registro = self.sessao.get(ProdutoRegistro, produto_id)

        # Retorno None se não encontrar o produto
        # JavaScript: registro === null ? null : paraDominio(registro)
        return None if registro is None else para_dominio(registro)

    def existe_nome(self, nome, exceto_id=None):
        # Busco um produto que tenha o nome informado
        consulta = select(ProdutoRegistro).where(ProdutoRegistro.nome == nome)
        registro = self.sessao.exec(consulta).first()

        # Verifico se existe um produto com esse nome, ignorando o ID informado
        return registro is not None and registro.id != exceto_id

    def listar(self, tamanho=None, preco_max=None):
        consulta = select(ProdutoRegistro)

        # Aplico os filtros somente quando os parâmetros são informados
        if tamanho is not None:
            consulta = consulta.where(ProdutoRegistro.tamanho == tamanho)
        if preco_max is not None:
            consulta = consulta.where(ProdutoRegistro.preco <= preco_max)

        # Ordeno os resultados pelo ID e converto os registros em objetos
        consulta = consulta.order_by(ProdutoRegistro.id)
        return [(r.id, para_dominio(r)) for r in self.sessao.exec(consulta)]

    def atualizar(self, produto_id, produto):
        registro = self.sessao.get(ProdutoRegistro, produto_id)

        # Retorno False se o produto não existir
        if registro is None:
            return False

        novo = para_registro(produto)

        # Copio os valores do novo registro para o registro existente
        for campo in CAMPOS:
            # getattr() lê um atributo e setattr() altera esse atributo
            # JavaScript: registro[campo] = novo[campo]
            setattr(registro, campo, getattr(novo, campo))

        self.sessao.add(registro)
        self.sessao.commit()
        return True

    def remover(self, produto_id):
        registro = self.sessao.get(ProdutoRegistro, produto_id)

        # Interrompo a remoção se o produto não existir
        if registro is None:
            return False

        self.sessao.delete(registro)
        self.sessao.commit()  # Confirmo a exclusão no banco
        return True
