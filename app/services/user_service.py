from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.repositories.user_repository import user_repository
from app.core.security import get_password_hash
from app.utils.enums import UserRole, SpecialistStatus
from app.repositories.patient_repository import patient_repository
from app.repositories.specialist_repository import specialist_repository

class UserService:
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        user = user_repository.get_by_email(db, email=obj_in.email)
        if user:
            raise HTTPException(
                status_code=400,
                detail="The user with this username already exists in the system.",
            )

        # Creates the basic user
        user_create_data = {
            "email": obj_in.email,
            "password_hash": get_password_hash(obj_in.password),
            "role": obj_in.role,
            "is_active": True
        }
        
        # Especialistas entram inativos e dependentes de aprovação pelo admin
        if obj_in.role == UserRole.ESPECIALISTA:
            user_create_data["is_active"] = False

        db_user = user_repository.create(db, obj_in=user_create_data)

        # Trata o preenchimento de dependentes (Paciente / Especialista) baseados na role
        if obj_in.role == UserRole.PACIENTE:
            if not obj_in.cpf or not obj_in.nome_completo or not obj_in.data_nascimento:
                 raise HTTPException(status_code=400, detail="Para pacientes, nome_completo, cpf e data_nascimento são obrigatórios.")
            patient_data = {
                "user_id": db_user.id,
                "nome_completo": obj_in.nome_completo,
                "cpf": obj_in.cpf,
                "data_nascimento": obj_in.data_nascimento,
                "telefone": obj_in.telefone
            }
            patient_repository.create(db, obj_in=patient_data)

        elif obj_in.role == UserRole.ESPECIALISTA:
            if not obj_in.registro_profissional or not obj_in.nome_completo or not obj_in.especialidade or not obj_in.modality:
                raise HTTPException(status_code=400, detail="Para especialistas, registro_profissional, nome_completo, especialidade e modality são obrigatórios.")
            specialist_data = {
                "user_id": db_user.id,
                "nome_completo": obj_in.nome_completo,
                "registro_profissional": obj_in.registro_profissional,
                "especialidade": obj_in.especialidade,
                "bio": getattr(obj_in, "bio", ""),
                "modality": obj_in.modality,
                "status": SpecialistStatus.PENDENTE
            }
            specialist_repository.create(db, obj_in=specialist_data)

        return db_user

user_service = UserService()
