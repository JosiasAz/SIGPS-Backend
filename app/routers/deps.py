from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import decode_token, get_bearer_token
from app.database.db import get_db
from app.database.models import User
from app.core.security import ROLE_ADMIN, ROLE_GESTOR, ROLE_RECEPCAO, ROLE_VISUALIZADOR


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(get_bearer_token),
) -> User:
    payload = decode_token(token)
    user_id = payload.get("userId")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido (sem userId)")
    user = db.get(User, int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não existe")
    return user


def require_roles(*roles: str):
    def _guard(user: User = Depends(get_current_user)) -> User:
        if user.perfil not in roles:
            raise HTTPException(status_code=403, detail="Sem permissão")
        return user
    return _guard


require_admin = require_roles(ROLE_ADMIN)
require_staff = require_roles(ROLE_ADMIN, ROLE_GESTOR, ROLE_RECEPCAO)  # operação
require_view = require_roles(ROLE_ADMIN, ROLE_GESTOR, ROLE_RECEPCAO, ROLE_VISUALIZADOR)