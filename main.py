from fastapi import FastAPI, HTTPException            
from fastapi.exceptions import RequestValidationError 
from contextlib import asynccontextmanager
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/src")

from src.infrastructure.database import engine
from src.domain.models import Base
from src.api.v1_router import router_unificado as api_v1_router

# handers de erro
from src.infrastructure.error_handlers import custom_http_exception_handler, validation_exception_handler

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="API Raízes do Nordeste",
    version="1.0.0",
    description="Projeto Multidisciplinar UNINTER - Trilha Back-End",
    lifespan=lifespan
)

# Informando sobre os tratadores de erros
app.add_exception_handler(HTTPException, custom_http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(api_v1_router)

@app.get("/", tags=["Health"])
async def rota_principal():
    return {"status": "Online", "projeto": "Raízes do Nordeste", "versao": "1.0.0"}