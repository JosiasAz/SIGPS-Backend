from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleCreate
from app.repositories.schedule_repository import schedule_repository

class ScheduleService:
    def create(self, db: Session, specialist_id: int, obj_in: ScheduleCreate) -> Schedule:
        # Check if already exists schedule for this specialist at this date/time if needed
        schedule_data = {
            "specialist_id": specialist_id,
            "data": obj_in.data,
            "hora_inicio": obj_in.hora_inicio,
            "is_available": True
        }
        return schedule_repository.create(db, obj_in=schedule_data)
        
    def cancel(self, db: Session, schedule_id: int):
        schedule = schedule_repository.get(db, id=schedule_id)
        if not schedule:
             raise HTTPException(status_code=404, detail="Horário não encontrado")
        return schedule_repository.remove(db, id=schedule_id)

schedule_service = ScheduleService()
