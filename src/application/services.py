import uuid # identificadores únicos

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from src.domain.models import Pedido, ItemPedido, Produto, StatusPedidoEnum
from src.application.schemas import PedidoCreate

async def criar_pedido_service(db: AsyncSession, pedido_dto: PedidoCreate, usuario_id: int):
    async with db.begin():
        valor_total = 0.0
        itens_bd = []

        for item_dto in pedido_dto.itens:
            # Busca o produto. O .with_for_update() bloqueia essa linha no banco 
            # temporariamente para 2 atendentes não comprarem o mesmo produto ao mesmo tempo!
            stmt = select(Produto).where(Produto.id == item_dto.produto_id).with_for_update()
            resultado = await db.execute(stmt)
            produto = resultado.scalar_one_or_none()

            if not produto:
                raise HTTPException(status_code=404, detail=f"Produto código {item_dto.produto_id} não cadastrado.")
            
            # Validando estoque antes do pedido
            if produto.estoque_qtd < item_dto.quantidade:
                raise HTTPException(
                    status_code=409, 
                    detail=f"Temos apenas {produto.estoque_qtd} und. de '{produto.nome}'. Você pediu {item_dto.quantidade}."
                )

            # Retira a unidade do estoque 
            produto.estoque_qtd -= item_dto.quantidade
            
            # soma no bolso da Lanchonete
            valor_total += produto.preco * item_dto.quantidade
            
            # Guarda o item da Nota 
            itens_bd.append(
                ItemPedido(produto_id=produto.id, quantidade=item_dto.quantidade, preco_unitario=produto.preco)
            )

        # Grava a Capa do Pedido
        novo_pedido = Pedido(
            usuario_id=usuario_id,
            canal_pedido=pedido_dto.canal_pedido,
            status=StatusPedidoEnum.AGUARDANDO_PAGAMENTO,
            valor_total=valor_total,
            itens=itens_bd
        )
        db.add(novo_pedido)
        
    await db.refresh(novo_pedido)
    return novo_pedido

async def processar_pagamento_mock_service(db: AsyncSession, pedido_id: int, cartao_mock: str):
    async with db.begin():
        # Busca o Pedido travando para evitar pagamento duplicado ao mesmo tempo 
        stmt = select(Pedido).where(Pedido.id == pedido_id).with_for_update()
        resultado = await db.execute(stmt)
        pedido = resultado.scalar_one_or_none()

        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido não encontrado no banco de dados.")

        # Só paga se estiver Aguardando Pagamento!
        if pedido.status != StatusPedidoEnum.AGUARDANDO_PAGAMENTO:
            raise HTTPException(
                status_code=400, 
                detail=f"Pedido no status '{pedido.status.value}' não permite cobrança agora."
            )

        # SIMULADOR DE GATEWAY (MOCK) 
        transacao_fake = str(uuid.uuid4()) 
        
        if cartao_mock.endswith("0000"):
            raise HTTPException(
                status_code=400,
                detail="Operadora recusou o cartão. Transação não autorizada. Status inalterado."
            )
        
        # Pagamento Autorizado. Muda o status na máquina para EM PREPARO
        pedido.status = StatusPedidoEnum.EM_PREPARO
        db.add(pedido) # Atualiza no banco
        
        return {
            "sucesso": True,
            "transacao_id": transacao_fake,
            "mensagem": "Pagamento recebido. A cozinha foi acionada!",
            "pedido": pedido
        }