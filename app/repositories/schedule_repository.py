from typing import List
from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.schedule import Schedule
from datetime import date

class ScheduleRepository(BaseRepository[Schedule]):
    def get_by_specialist_and_date(self, db: Session, *, specialist_id: int, target_date: date) -> List[Schedule]:
        return db.query(Schedule).filter(
            Schedule.specialist_id == specialist_id,
            Schedule.data == target_date,
            Schedule.is_available == True
        ).all()

schedule_repository = ScheduleRepository(Schedule)
