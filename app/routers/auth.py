from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import (
    criar_token_acesso, 
    criar_token_refresh,
    gerar_hash_senha, 
    verificar_senha, 
    TODOS_PERFIS,
    decodificar_token,
    obter_token_bearer
)
from app.core.responses import standard_response
from app.core.config import settings
from app.database.db import obter_sessao_db
from app.database.models import Usuario, RefreshToken, Paciente, Especialista
from app.schemas.auth import UserRegister, UserLogin, TokenRefreshRequest, UserResponse

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/register")
def register(dados: UserRegister, db: Session = Depends(obter_sessao_db)):
    role = dados.role.strip().lower()
    if role not in TODOS_PERFIS:
        return standard_response(False, message=f"Perfil inválido: {role}", error_code="INVALID_ROLE", status_code=422)

    # Check if email exists
    existente = db.scalar(select(Usuario).where(Usuario.email == str(dados.email).lower()))
    if existente:
        return standard_response(False, message="Email já cadastrado", error_code="EMAIL_EXISTS", status_code=409)

    novo_usuario = Usuario(
        email=str(dados.email).lower(),
        senha_hash=gerar_hash_senha(dados.password),
        perfil=role,
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    # Automatically create profile for Paciente or Especialista
    if role == "paciente":
        perfil = Paciente(usuario_id=novo_usuario.id, nome="Novo Paciente", email=novo_usuario.email)
        db.add(perfil)
    elif role == "especialista":
        perfil = Especialista(usuario_id=novo_usuario.id, nome="Novo Especialista")
        db.add(perfil)
    
    db.commit()

    return standard_response(
        True, 
        data={"id": novo_usuario.id, "email": novo_usuario.email, "role": novo_usuario.perfil},
        message="Usuário registrado com sucesso",
        status_code=201
    )

@router.post("/login")
def login(dados: UserLogin, db: Session = Depends(obter_sessao_db)):
    usuario = db.scalar(select(Usuario).where(Usuario.email == str(dados.email).lower()))
    if not usuario or not verificar_senha(dados.password, usuario.senha_hash):
        return standard_response(False, message="Credenciais inválidas", error_code="UNAUTHORIZED", status_code=401)

    access_token = criar_token_acesso(usuario.id, usuario.perfil)
    refresh_token_str = criar_token_refresh(usuario.id)

    # Store refresh token
    exp = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    db_refresh = RefreshToken(token=refresh_token_str, usuario_id=usuario.id, expira_em=exp)
    db.add(db_refresh)
    db.commit()

    return standard_response(
        True,
        data={
            "access_token": access_token,
            "refresh_token": refresh_token_str,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
    )

@router.post("/refresh")
def refresh(dados: TokenRefreshRequest, db: Session = Depends(obter_sessao_db)):
    # Verify refresh token in DB
    db_token = db.scalar(select(RefreshToken).where(RefreshToken.token == dados.refresh_token, RefreshToken.revogado == 0))
    if not db_token:
        return standard_response(False, message="Refresh token inválido ou revogado", error_code="INVALID_TOKEN", status_code=401)

    if db_token.expira_em.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        return standard_response(False, message="Refresh token expirado", error_code="TOKEN_EXPIRED", status_code=401)

    usuario = db_token.usuario
    access_token = criar_token_acesso(usuario.id, usuario.perfil)
    
    return standard_response(
        True,
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
    )

@router.post("/logout")
def logout(token: str = Depends(obter_token_bearer), db: Session = Depends(obter_sessao_db)):
    # Invalidate refresh tokens for this user
    payload = decodificar_token(token)
    user_id = int(payload.get("sub"))
    
    tokens = db.scalars(select(RefreshToken).where(RefreshToken.usuario_id == user_id, RefreshToken.revogado == 0)).all()
    for t in tokens:
        t.revogado = 1
    
    db.commit()
    return standard_response(True, message="Logout realizado com sucesso")