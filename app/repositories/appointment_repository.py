from sqlalchemy.orm import Session
from typing import List
from app.repositories.base_repository import BaseRepository
from app.models.appointment import Appointment

class AppointmentRepository(BaseRepository[Appointment]):
    def get_by_patient(self, db: Session, *, patient_id: int, skip: int = 0, limit: int = 100) -> List[Appointment]:
        return db.query(Appointment).filter(Appointment.patient_id == patient_id).offset(skip).limit(limit).all()

    def get_by_specialist(self, db: Session, *, specialist_id: int, skip: int = 0, limit: int = 100) -> List[Appointment]:
        return db.query(Appointment).filter(Appointment.specialist_id == specialist_id).offset(skip).limit(limit).all()

appointment_repository = AppointmentRepository(Appointment)
