from fastapi import FastAPI
from app.core.config import settings
from app.database.db import engine
from app.database.models import Base

from app.routers.health import router as health_router
from app.routers.auth import router as auth_router
from app.routers.patients import router as patients_router
from app.routers.specialists import router as specialists_router
from app.routers.schedule import router as schedule_router
from app.routers.queue import router as queue_router
from app.routers.dashboard import router as dashboard_router
from app.routers.ml import router as ml_router

app = FastAPI(title="SIGPS Backend", version="1.0.0")

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(patients_router)
app.include_router(specialists_router)
app.include_router(schedule_router)
app.include_router(queue_router)
app.include_router(dashboard_router)
app.include_router(ml_router)


@app.on_event("startup")
def on_startup():
    # Para TCC/dev: cria tabelas automaticamente (funciona “de primeira”)
    # Em produção você pode trocar por Alembic.
    if settings.APP_ENV.lower() in {"dev", "local"}:
        Base.metadata.create_all(bind=engine)