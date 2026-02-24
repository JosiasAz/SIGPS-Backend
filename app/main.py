from fastapi import FastAPI
from app.core.config import settings
from app.database.db import motor_db
from app.database.models import Base

from app.routers.saude import router as rota_saude
from app.routers.auth import router as rota_auth
from app.routers.pacientes import router as rota_pacientes
from app.routers.especialistas import router as rota_especialistas
from app.routers.agenda import router as rota_agenda
from app.routers.fila import router as rota_fila
from app.routers.painel import router as rota_painel
from app.routers.ia import router as rota_ia

app = FastAPI(title="SIGPS Backend", version="1.0.0")

app.include_router(rota_saude)
app.include_router(rota_auth)
app.include_router(rota_pacientes)
app.include_router(rota_especialistas)
app.include_router(rota_agenda)
app.include_router(rota_fila)
app.include_router(rota_painel)
app.include_router(rota_ia)


@app.on_event("startup")
def ao_iniciar():
    # Em produção você pode trocar por Alembic.
    if settings.APP_ENV.lower() in {"dev", "local"}:
        Base.metadata.create_all(bind=motor_db)