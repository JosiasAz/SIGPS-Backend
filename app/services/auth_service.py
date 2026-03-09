from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.core import security
from app.models.user import User
from app.repositories.user_repository import user_repository

class AuthService:
    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
        user = user_repository.get_by_email(db, email=email)
        if not user:
            return None
        if not security.verify_password(password, user.password_hash):
            return None
        return user

    def login(self, db: Session, email: str, password: str) -> Optional[User]:
        user = self.authenticate(db, email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        elif not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return user

auth_service = AuthService()
