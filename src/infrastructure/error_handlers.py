from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from datetime import datetime

# Este captura erros nossos de regra de negócio (O seu Error 409, Error 404, etc)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": f"Erro na Requisição HTTP ({exc.status_code})",
            "message": exc.detail,
            "details": "Verifique a regra de negócios descrita na message.",
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path
        }
    )

# Este captura quando um Hack ou App manda JSONs tortos ou errados 
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Erro de Validação Semântica (422)",
            "message": "Os dados enviados no JSON ou URL não seguem os contratos do sistema.",
            "details": exc.errors(),
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path
        }
    )