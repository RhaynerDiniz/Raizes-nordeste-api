from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# Cria o arquivo do banco local no seu PC para desenvolvimento (aiosqlite = SQLite assíncrono)
DATABASE_URL = "sqlite+aiosqlite:///./raizes_nordeste.db"

# Engine de conexão do SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True) # echo=True exibe os comandos SQL no terminal

# Fábrica (Factory) que vai criar as sessões do banco de dados para nós
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

# Essa função (Dependência) "entrega" o banco para a nossa API toda vez que houver um acesso.
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()