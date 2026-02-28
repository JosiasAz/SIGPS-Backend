from pydantic import BaseModel
from typing import Optional

class FilaCriar(BaseModel):
    especialista_id: Optional[int] = None
    motivo: Optional[str] = None
    urgencia_declarada: Optional[int] = 0 # 1-10

class FilaPrioridadeUpdate(BaseModel):
    prioridade: int

class FilaResposta(BaseModel):
    id: int
    paciente_id: int
    especialista_id: Optional[int]
    motivo: Optional[str]
    prioridade: int
    score_ml: Optional[float]
    status: str

    class Config:
        from_attributes = True