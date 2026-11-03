from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./raizes_nordeste.db"

# Engine de conexão do SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True) # echo=True exibe os comandos SQL no terminal

# Fábrica (Factory) que cria as sessões do banco de dados 
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()