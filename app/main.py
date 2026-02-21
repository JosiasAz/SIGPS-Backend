from fastapi import FastAPI
from app.routers.health import router as health_router
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.ml import router as ml_router

app = FastAPI(title="SIGPS API")

app.include_router(health_router)
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(ml_router, prefix="/ml", tags=["ML"])
