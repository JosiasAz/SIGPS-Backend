from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.specialist import Specialist
from app.utils.enums import SpecialistStatus

class SpecialistRepository(BaseRepository[Specialist]):
    def get_by_registro(self, db: Session, *, registro_profissional: str) -> Optional[Specialist]:
        return db.query(Specialist).filter(Specialist.registro_profissional == registro_profissional).first()

    def get_by_user_id(self, db: Session, *, user_id: int) -> Optional[Specialist]:
        return db.query(Specialist).filter(Specialist.user_id == user_id).first()

    def get_by_status(self, db: Session, *, status: SpecialistStatus, skip: int = 0, limit: int = 100) -> List[Specialist]:
        return db.query(Specialist).filter(Specialist.status == status).offset(skip).limit(limit).all()

specialist_repository = SpecialistRepository(Specialist)
