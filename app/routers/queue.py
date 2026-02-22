from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database.db import get_db
from app.database.models import QueueEntry, Patient, Specialist
from app.routers.deps import require_staff, require_view
from app.schemas.queue import QueueCreate, QueueUpdateStatus, QueueResponse
from app.services.queue import get_queue_ordered

router = APIRouter(prefix="/queue", tags=["Queue"])


@router.post("", response_model=QueueResponse)
def add_to_queue(
    data: QueueCreate,
    db: Session = Depends(get_db),
    _=Depends(require_staff),
):
    if not db.get(Patient, data.patient_id):
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    if data.specialist_id is not None and not db.get(Specialist, data.specialist_id):
        raise HTTPException(status_code=404, detail="Especialista não encontrado")

    e = QueueEntry(**data.model_dump(), status="aguardando")
    db.add(e)
    db.commit()
    db.refresh(e)
    return e


@router.get("", response_model=list[QueueResponse])
def list_queue(
    db: Session = Depends(get_db),
    _=Depends(require_view),
):
    return list(db.scalars(select(QueueEntry)).all())


@router.get("/ordered", response_model=list[QueueResponse])
def queue_ordered(
    db: Session = Depends(get_db),
    _=Depends(require_view),
):
    return get_queue_ordered(db)


@router.patch("/{entry_id}/status", response_model=QueueResponse)
def update_queue_status(
    entry_id: int,
    data: QueueUpdateStatus,
    db: Session = Depends(get_db),
    _=Depends(require_staff),
):
    e = db.get(QueueEntry, entry_id)
    if not e:
        raise HTTPException(status_code=404, detail="Entrada da fila não encontrada")

    allowed = {"aguardando", "chamado", "atendido", "cancelado"}
    if data.status not in allowed:
        raise HTTPException(status_code=422, detail="Status inválido")

    e.status = data.status
    db.commit()
    db.refresh(e)
    return e