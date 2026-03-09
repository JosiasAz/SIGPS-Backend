from pydantic import BaseModel
from typing import Optional
from datetime import date

class PatientBase(BaseModel):
    nome_completo: str
    telefone: Optional[str] = None

class PatientCreate(PatientBase):
    cpf: str
    data_nascimento: date

class PatientUpdate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int
    user_id: int
    cpf: str
    data_nascimento: date

    class Config:
        from_attributes = True
