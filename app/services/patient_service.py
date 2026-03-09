from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.patient import Patient
from app.schemas.patient import PatientUpdate
from app.repositories.patient_repository import patient_repository

class PatientService:
    def get_by_user_id(self, db: Session, user_id: int) -> Patient:
        patient = patient_repository.get_by_user_id(db, user_id=user_id)
        if not patient:
            raise HTTPException(status_code=404, detail="Paciente não encontrado")
        return patient

    def update(self, db: Session, user_id: int, obj_in: PatientUpdate) -> Patient:
        patient = self.get_by_user_id(db, user_id)
        return patient_repository.update(db, db_obj=patient, obj_in=obj_in)

patient_service = PatientService()
