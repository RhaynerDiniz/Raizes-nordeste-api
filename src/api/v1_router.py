from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import JWTError, jwt

from src.infrastructure.database import get_db
from src.infrastructure.security import (
    verify_password, get_password_hash, create_access_token, 
    oauth2_scheme, SECRET_KEY, ALGORITHM
)
from src.domain.models import Usuario, RoleEnum
from src.application.schemas import (
    PedidoCreate, PedidoResponse, 
    PagamentoMockRequest, PagamentoMockResponse,
    UsuarioCreate
)
from src.application.services import criar_pedido_service, processar_pagamento_mock_service

router = APIRouter(prefix="/api/v1", tags=["Pedidos e Caixa"])
auth_router = APIRouter(prefix="/api/v1", tags=["Autenticação e LGPD"]) 

async def get_usuario_logado(token: str = Depends(oauth2_scheme)):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token Inválido")
        return int(user_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="Sua sessão expirou. Faça login novamente.", headers={"WWW-Authenticate": "Bearer"})


@auth_router.post("/usuarios/cadastrar", status_code=201)
async def cadastrar_usuario(user_dto: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    if not user_dto.aceite_lgpd:
        raise HTTPException(status_code=422, detail="Para se cadastrar é obrigatório o aceite da LGPD (Consentimento Mínimo).")
        
    usuario_novo = Usuario(
        nome=user_dto.nome,
        cpf=user_dto.cpf,
        email=user_dto.email,
        senha_hash=get_password_hash(user_dto.senha), # SENHA BCRYPT 
        role=RoleEnum.CLIENTE,
        aceite_lgpd=user_dto.aceite_lgpd
    )
    db.add(usuario_novo)
    await db.commit()
    return {"message": f"Usuário {usuario_novo.nome} criado! Senha está irreconhecível no Banco de Dados."}

@auth_router.post("/auth/token")
async def login_para_obter_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    stmt = select(Usuario).where(Usuario.email == form_data.username) # Swagger usa campo "username"
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.senha_hash):
        raise HTTPException(status_code=401, detail="Acesso Negado: E-mail ou Senha incorretos.")

    token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/pedidos", response_model=PedidoResponse, status_code=201)
async def endpoint_criar_pedido(
    pedido: PedidoCreate, 
    db: AsyncSession = Depends(get_db),
    
    usuario_id: int = Depends(get_usuario_logado) 
):
    return await criar_pedido_service(db=db, pedido_dto=pedido, usuario_id=usuario_id)

@router.post("/pedidos/{pedido_id}/pagar", response_model=PagamentoMockResponse)
async def endpoint_pagar_pedido(
    pedido_id: int, 
    pagamento: PagamentoMockRequest, 
    db: AsyncSession = Depends(get_db),
    usuario_id: int = Depends(get_usuario_logado) #
):
    return await processar_pagamento_mock_service(db=db, pedido_id=pedido_id, cartao_mock=pagamento.cartao_ficticio)

from fastapi import APIRouter
router_unificado = APIRouter()
router_unificado.include_router(auth_router)
router_unificado.include_router(router)