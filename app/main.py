from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.database.db import motor_db
from app.database.models import Base
from app.core.responses import standard_response

# Import routers
from app.routers.auth import router as rota_auth
from app.routers.especialistas import router as rota_especialistas
from app.routers.agendamentos import router as rota_agendamentos
from app.routers.fila import router as rota_fila
from app.routers.dashboard import router as rota_dashboard
from app.routers.admin import router as rota_admin

app = FastAPI(
    title="SIGPS Backend", 
    description="Sistema Inteligente de Gestão e Priorização na Saúde",
    version="2.0.0"
)

# Exception Handlers to match standard response pattern
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return standard_response(
        False, 
        message=str(exc.detail), 
        error_code=f"HTTP_{exc.status_code}", 
        status_code=exc.status_code
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    msg = errors[0].get("msg") if errors else "Dados inválidos"
    return standard_response(
        False, 
        message=f"Erro de validação: {msg}", 
        error_code="VALIDATION_ERROR", 
        status_code=422
    )

# Include routers
app.include_router(rota_auth)
app.include_router(rota_especialistas)
app.include_router(rota_agendamentos)
app.include_router(rota_fila)
app.include_router(rota_dashboard)
app.include_router(rota_admin)

@app.on_event("startup")
def ao_iniciar():
    # Em produção pode trocar por Alembic.
    if settings.APP_ENV.lower() in {"dev", "local"}:
        Base.metadata.create_all(bind=motor_db)

@app.get("/")
def home():
    return {"message": "SIGPS API rodando. Accesse /docs para documentação."}