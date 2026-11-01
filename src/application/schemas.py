from pydantic import BaseModel, ConfigDict, Field
from typing import List
from src.domain.models import CanalPedidoEnum, StatusPedidoEnum

class ItemPedidoCreate(BaseModel):
    produto_id: int
    # Field garante que ninguém vai mandar um pedido com "0" ou quantidade negativa
    quantidade: int = Field(gt=0, description="A quantidade deve ser no mínimo 1")

class PedidoCreate(BaseModel):
    # Exige que a Multicanalidade (APP, TOTEM, etc) seja obrigatoriamente informada
    canal_pedido: CanalPedidoEnum
    itens: List[ItemPedidoCreate]

class PedidoResponse(BaseModel):
    id: int
    usuario_id: int
    canal_pedido: CanalPedidoEnum
    status: StatusPedidoEnum
    valor_total: float

    model_config = ConfigDict(from_attributes=True)

class PagamentoMockRequest(BaseModel):
    cartao_ficticio: str = Field(min_length=16, max_length=16, description="Digite 16 números. Termine em 0000 para forçar erro de recusa.")
    
class PagamentoMockResponse(BaseModel):
    sucesso: bool
    transacao_id: str
    mensagem: str
    pedido: PedidoResponse

class UsuarioCreate(BaseModel):
    nome: str
    cpf: str
    email: str
    senha: str
    aceite_lgpd: bool = Field(description="Obrigatório aceite para retenção de dados.")   