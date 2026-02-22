from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password, ALL_ROLES
from app.database.db import get_db
from app.database.models import User
from app.schemas.auth import RegisterRequest, LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    perfil = data.perfil.strip().lower()
    if perfil not in ALL_ROLES:
        raise HTTPException(status_code=422, detail=f"Perfil inválido: {perfil}")

    user = User(
        email=str(data.email).lower(),
        password_hash=hash_password(data.senha),
        perfil=perfil,
    )
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email já cadastrado")

    return {"id": user.id, "email": user.email, "perfil": user.perfil}


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == str(data.email).lower()))
    if not user or not verify_password(data.senha, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    tok = create_access_token(user.id, user.perfil)
    return LoginResponse(
        access_token=tok["token"],
        expires_at=tok["expires_at"].isoformat(),
    )