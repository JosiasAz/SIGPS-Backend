from pydantic import BaseModel
from typing import Optional
from app.utils.enums import SpecialistStatus

class SpecialistBase(BaseModel):
    nome_completo: str
    bio: Optional[str] = None
    modality: str

class SpecialistCreate(SpecialistBase):
    registro_profissional: str
    especialidade: str

class SpecialistUpdate(BaseModel):
    nome_completo: Optional[str] = None
    bio: Optional[str] = None
    modality: Optional[str] = None

class SpecialistResponse(SpecialistBase):
    id: int
    user_id: int
    registro_profissional: str
    especialidade: str
    status: SpecialistStatus

    class Config:
        from_attributes = True
