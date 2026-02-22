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
ROLE_ADMIN = "admin"
ROLE_GESTOR = "gestor"
ROLE_RECEPCAO = "recepcao"
ROLE_VISUALIZADOR = "visualizador"

ALL_ROLES = {ROLE_ADMIN, ROLE_GESTOR, ROLE_RECEPCAO, ROLE_VISUALIZADOR}


def hash_password(raw: str) -> str:
    return pwd_context.hash(raw)


def verify_password(raw: str, hashed: str) -> bool:
    return pwd_context.verify(raw, hashed)


def create_access_token(user_id: int, perfil: str) -> Dict[str, Any]:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "userId": user_id,
        "perfil": perfil,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
    return {"token": token, "expires_at": exp}


def decode_token(token: str) -> Dict[str, Any]:
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


def get_bearer_token(
    creds: Optional[HTTPAuthorizationCredentials] = Depends(bearer),
) -> str:
    if not creds or not creds.credentials:
        raise HTTPException(status_code=401, detail="Token ausente")
    return creds.credentials