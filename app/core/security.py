from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer = HTTPBearer(auto_error=False)

# Perfis do SIGPS
PERFIL_ESPECIALISTA = "especialista"
PERFIL_ADMIN = "admin"
PERFIL_GESTOR = "gestor"
PERFIL_PACIENTE = "paciente"
PERFIL_VISUALIZADOR = "visualizador"

TODOS_PERFIS = {PERFIL_ADMIN, PERFIL_GESTOR, PERFIL_PACIENTE, PERFIL_VISUALIZADOR, PERFIL_ESPECIALISTA}


def gerar_hash_senha(senha_pura: str) -> str:
    return pwd_context.hash(senha_pura)


def verificar_senha(senha_pura: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha_pura, senha_hash)


def criar_token_acesso(usuario_id: int, perfil: str, expires_delta: Optional[timedelta] = None) -> str:
    now = datetime.now(timezone.utc)
    if expires_delta:
        exp = now + expires_delta
    else:
        exp = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(usuario_id),
        "perfil": perfil,
        "type": "access",
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def criar_token_refresh(usuario_id: int) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    payload = {
        "sub": str(usuario_id),
        "type": "refresh",
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def decodificar_token(token: str) -> Dict[str, Any]:
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


def obter_token_bearer(
    creds: Optional[HTTPAuthorizationCredentials] = Depends(bearer),
) -> str:
    if not creds or not creds.credentials:
        raise HTTPException(status_code=401, detail="Token ausente")
    return creds.credentials