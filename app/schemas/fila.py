from pydantic import BaseModel


class FilaCriar(BaseModel):
    paciente_id: int
    especialista_id: int | None = None
    motivo: str | None = None
    prioridade: int = 0


class FilaAtualizarStatus(BaseModel):
    status: str  # aguardando|chamado|atendido|cancelado


class FilaResposta(BaseModel):
    id: int
    paciente_id: int
    especialista_id: int | None
    motivo: str | None
    prioridade: int
    score_ml: float | None
    status: str

    class Config:
        from_attributes = True