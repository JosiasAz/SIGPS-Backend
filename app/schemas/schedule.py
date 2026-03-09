from pydantic import BaseModel
from datetime import date, time

class ScheduleBase(BaseModel):
    data: date
    hora_inicio: time

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(BaseModel):
    is_available: bool

class ScheduleResponse(ScheduleBase):
    id: int
    specialist_id: int
    is_available: bool

    class Config:
        from_attributes = True
