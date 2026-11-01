import enum
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

Base = declarative_base()

# ============ ENUMS (Domínio Restrito) ============
class RoleEnum(str, enum.Enum):
    CLIENTE = "CLIENTE"
    ATENDENTE = "ATENDENTE"
    COZINHA = "COZINHA"
    GERENTE = "GERENTE"
    ADMIN = "ADMIN"

class CanalPedidoEnum(str, enum.Enum):
    APP = "APP"
    TOTEM = "TOTEM"
    BALCAO = "BALCAO"
    PICKUP = "PICKUP"
    WEB = "WEB"

class StatusPedidoEnum(str, enum.Enum):
    AGUARDANDO_PAGAMENTO = "AGUARDANDO_PAGAMENTO"
    EM_PREPARO = "EM_PREPARO"
    PRONTO = "PRONTO"
    ENTREGUE = "ENTREGUE"
    CANCELADO = "CANCELADO"


# ============ TABELAS DO BANCO DE DADOS ============
class Usuario(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(100))
    cpf: Mapped[str] = mapped_column(String(14), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    senha_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[RoleEnum] = mapped_column(SQLEnum(RoleEnum), default=RoleEnum.CLIENTE)
    # Requisito explícito de LGPD (Auditoria de aceite):
    aceite_lgpd: Mapped[bool] = mapped_column(Boolean, default=False)

class Produto(Base):
    __tablename__ = "produtos"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    preco: Mapped[float] = mapped_column(Float)
    estoque_qtd: Mapped[int] = mapped_column(Integer, default=0)

class Pedido(Base):
    __tablename__ = "pedidos"
    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    # Requisito MVP Fluxo A (Multicanalidade Obrigatória):
    canal_pedido: Mapped[CanalPedidoEnum] = mapped_column(SQLEnum(CanalPedidoEnum))
    status: Mapped[StatusPedidoEnum] = mapped_column(SQLEnum(StatusPedidoEnum), default=StatusPedidoEnum.AGUARDANDO_PAGAMENTO)
    valor_total: Mapped[float] = mapped_column(Float, default=0.0)
    
    itens = relationship("ItemPedido", back_populates="pedido", lazy="selectin")

class ItemPedido(Base):
    __tablename__ = "itens_pedido"
    id: Mapped[int] = mapped_column(primary_key=True)
    pedido_id: Mapped[int] = mapped_column(ForeignKey("pedidos.id"))
    produto_id: Mapped[int] = mapped_column(ForeignKey("produtos.id"))
    quantidade: Mapped[int] = mapped_column(Integer)
    preco_unitario: Mapped[float] = mapped_column(Float)

    pedido = relationship("Pedido", back_populates="itens")