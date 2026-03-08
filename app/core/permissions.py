from typing import List
from fastapi import Depends, HTTPException, status
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.utils.enums import UserRole

class RoleChecker:
    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_active_user)):
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User role {user.role} does not have sufficient permissions",
            )
        return user

# Instâncias de conveniência para verificação de permissão
is_admin = RoleChecker([UserRole.ADMIN])
is_gestor = RoleChecker([UserRole.ADMIN, UserRole.GESTOR])
is_paciente = RoleChecker([UserRole.PACIENTE])
is_especialista = RoleChecker([UserRole.ESPECIALISTA]) or RoleChecker([UserRole.ADMIN])
# Para rotas que precisam de especialista OU admin/gestor
is_specialist_or_admin = RoleChecker([UserRole.ADMIN, UserRole.GESTOR, UserRole.ESPECIALISTA])
