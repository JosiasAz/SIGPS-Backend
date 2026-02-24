from datetime import datetime
from pydantic import BaseModel


class AgendamentoCriar(BaseModel):
    paciente_id: int
    especialista_id: int
    inicio: datetime
    fim: datetime


class AgendamentoResposta(BaseModel):
    id: int
    paciente_id: int
    especialista_id: int
    inicio: datetime
    fim: datetime
    status: str

    class Config:
        from_attributes = True