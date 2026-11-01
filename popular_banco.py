import asyncio
import sys
import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

# Configura caminhos para o script rodar liso
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/src")

from src.infrastructure.database import AsyncSessionLocal
from src.domain.models import Usuario, Produto, RoleEnum

async def seed_data():
    async with AsyncSessionLocal() as session:
        # Iniciando a transação
        async with session.begin():
            print("Limpando banco e Inserindo Dados na Lanchonete Raízes do Nordeste...")
            
            # Criando Usuário Teste (ID 1 que está hardcodado no nosso endpoint)
            user = Usuario(
                nome="João da Silva",
                cpf="11122233344",
                email="joao@uninter.com",
                senha_hash="123456_hashmock",
                role=RoleEnum.CLIENTE,
                aceite_lgpd=True
            )
            session.add(user)

            # Criando Produtos (O Menu)
            p1 = Produto(nome="Coxinha de Charque", preco=8.50, estoque_qtd=10) # Tem 10 no estoque
            p2 = Produto(nome="Suco de Cajá", preco=6.00, estoque_qtd=2)        # Tem só 2 no estoque (cuidado!)
            p3 = Produto(nome="Tapioca de Queijo", preco=12.00, estoque_qtd=5)  # Tem 5 no estoque

            session.add_all([p1, p2, p3])
            
        print("Tudo pronto! Prateleiras abastecidas!")

if __name__ == "__main__":
    asyncio.run(seed_data())