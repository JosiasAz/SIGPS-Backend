from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.patient import Patient

class PatientRepository(BaseRepository[Patient]):
    def get_by_cpf(self, db: Session, *, cpf: str) -> Optional[Patient]:
        return db.query(Patient).filter(Patient.cpf == cpf).first()
        
    def get_by_user_id(self, db: Session, *, user_id: int) -> Optional[Patient]:
        return db.query(Patient).filter(Patient.user_id == user_id).first()

patient_repository = PatientRepository(Patient)
