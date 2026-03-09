from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.specialist import Specialist
from app.schemas.specialist import SpecialistUpdate
from app.repositories.specialist_repository import specialist_repository
from app.repositories.user_repository import user_repository
from app.utils.enums import SpecialistStatus

class SpecialistService:
    def get_by_user_id(self, db: Session, user_id: int) -> Specialist:
        specialist = specialist_repository.get_by_user_id(db, user_id=user_id)
        if not specialist:
            raise HTTPException(status_code=404, detail="Especialista não encontrado")
        return specialist

    def update(self, db: Session, user_id: int, obj_in: SpecialistUpdate) -> Specialist:
        specialist = self.get_by_user_id(db, user_id)
        return specialist_repository.update(db, db_obj=specialist, obj_in=obj_in)

    def get_ativos(self, db: Session) -> List[Specialist]:
        return specialist_repository.get_by_status(db, status=SpecialistStatus.ATIVO)

    def approve(self, db: Session, specialist_id: int) -> Specialist:
        specialist = specialist_repository.get(db, id=specialist_id)
        if not specialist:
            raise HTTPException(status_code=404, detail="Especialista não encontrado")
            
        # Atualiza status do especialista para ATIVO
        specialist_update_data = {"status": SpecialistStatus.ATIVO}
        specialist = specialist_repository.update(db, db_obj=specialist, obj_in=specialist_update_data)
        
        # Ativa o User correspondente no login
        user = user_repository.get(db, id=specialist.user_id)
        if user:
            user_repository.update(db, db_obj=user, obj_in={"is_active": True})
            
        return specialist

specialist_service = SpecialistService()
