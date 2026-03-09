from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_active_user
from app.core.permissions import is_gestor
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import user_service
from app.repositories.user_repository import user_repository

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """
    Cria um novo usuário.
    """
    user = user_service.create(db, obj_in=user_in)
    return user

@router.get("/", response_model=List[UserResponse])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(is_gestor),
) -> Any:
    """
    Retorna todos os usuários. Apenas usuários com permissão de Gestor/Admin podem acessar.
    """
    users = user_repository.get_multi(db, skip=skip, limit=limit)
    return users
