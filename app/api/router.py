from fastapi import APIRouter

from app.api.v1 import auth, users, patients, specialists, appointments

api_router = APIRouter()

# As rotas de versão (v1) serão incluídas aqui conforme forem criadas
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(patients.router, prefix="/patients", tags=["patients"])
api_router.include_router(specialists.router, prefix="/specialists", tags=["specialists"])
api_router.include_router(appointments.router, prefix="/appointments", tags=["appointments"])
