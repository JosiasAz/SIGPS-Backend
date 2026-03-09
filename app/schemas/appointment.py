from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.patient import PatientResponse
from app.schemas.specialist import SpecialistResponse
from app.schemas.schedule import ScheduleResponse

class AppointmentBase(BaseModel):
    schedule_id: int
    specialist_id: int

class AppointmentCreate(AppointmentBase):
    # patient_id será pego do token do usuário
    pass

class AppointmentUpdate(BaseModel):
    status: str

class AppointmentResponse(AppointmentBase):
    id: int
    patient_id: int
    status: str
    data_criacao: datetime

    # Dados adicionais para facilitar o frontend
    patient: Optional[PatientResponse] = None
    specialist: Optional[SpecialistResponse] = None
    schedule: Optional[ScheduleResponse] = None

    class Config:
        from_attributes = True
