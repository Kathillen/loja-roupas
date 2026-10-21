
from sqlalchemy.pool import StaticPool
from sqlmodel import Field, SQLModel, create_engine

# Defino o caminho do arquivo onde os dados do banco serão salvos
URL_BANCO = "sqlite:///loja.db"


class ProdutoRegistro(SQLModel, table=True):
    """Represento um produto no formato em que o banco armazena."""

    __tablename__ = "produto"  # Defino o nome da tabela no banco

    # Uso Field para definir as configurações das colunas no banco
    id: int | None = Field(default=None, primary_key=True)
    tipo: str
    nome: str = Field(unique=True)
    preco: float
    tamanho: str
    manga: str | None = None       # Deixo opcional porque só a camiseta usa
    modelagem: str | None = None   # Deixo opcional porque só a calça usa


def criar_engine(url=URL_BANCO):
    # Verifico se a URL começa com "sqlite" usando o método nativo startswith()
    # JavaScript: url.startsWith("sqlite")
    argumentos = {"check_same_thread": False} if url.startswith("sqlite") else {}

    # Crio a conexão com o banco usando o SQLModel
    # JavaScript: precisaria de uma biblioteca específica para conectar ao banco
    return create_engine(url, connect_args=argumentos)


def engine_em_memoria():
    """Crio um banco temporário que existe apenas na memória."""

    # Uso StaticPool para manter a mesma conexão com o banco em memória
    # durante os testes
    return create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )


def criar_tabelas(engine):
    # Crio as tabelas definidas no SQLModel caso ainda não existam
    # Equivalente SQL: CREATE TABLE IF NOT EXISTS
    SQLModel.metadata.create_all(engine)
