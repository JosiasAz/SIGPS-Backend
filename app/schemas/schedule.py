from datetime import datetime
from pydantic import BaseModel


class AppointmentCreate(BaseModel):
    patient_id: int
    specialist_id: int
    inicio: datetime
    fim: datetime


class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    specialist_id: int
    inicio: datetime
    fim: datetime
    status: str

    class Config:
        from_attributes = True