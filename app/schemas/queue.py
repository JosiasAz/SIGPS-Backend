from pydantic import BaseModel


class QueueCreate(BaseModel):
    patient_id: int
    specialist_id: int | None = None
    motivo: str | None = None
    prioridade: int = 0


class QueueUpdateStatus(BaseModel):
    status: str  # aguardando|chamado|atendido|cancelado


class QueueResponse(BaseModel):
    id: int
    patient_id: int
    specialist_id: int | None
    motivo: str | None
    prioridade: int
    score_ml: float | None
    status: str

    class Config:
        from_attributes = True