from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from app.database.db import get_db
from app.database.models import Appointment, Patient, Specialist
from app.routers.deps import require_staff, require_view
from app.schemas.schedule import AppointmentCreate, AppointmentResponse

router = APIRouter(prefix="/schedule", tags=["Schedule"])


@router.post("/appointments", response_model=AppointmentResponse)
def create_appointment(
    data: AppointmentCreate,
    db: Session = Depends(get_db),
    _=Depends(require_staff),
):
    if not db.get(Patient, data.patient_id):
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    if not db.get(Specialist, data.specialist_id):
        raise HTTPException(status_code=404, detail="Especialista não encontrado")
    if data.fim <= data.inicio:
        raise HTTPException(status_code=422, detail="fim deve ser depois de inicio")

    # conflito simples: mesmo especialista com overlap
    overlap = db.scalar(
        select(Appointment).where(
            and_(
                Appointment.specialist_id == data.specialist_id,
                Appointment.status == "agendado",
                Appointment.inicio < data.fim,
                Appointment.fim > data.inicio,
            )
        )
    )
    if overlap:
        raise HTTPException(status_code=409, detail="Conflito de agenda para esse especialista")

    a = Appointment(**data.model_dump(), status="agendado")
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


@router.get("/appointments", response_model=list[AppointmentResponse])
def list_appointments(
    db: Session = Depends(get_db),
    _=Depends(require_view),
):
    return list(db.scalars(select(Appointment)).all())


@router.post("/appointments/{appointment_id}/cancel")
def cancel_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_staff),
):
    a = db.get(Appointment, appointment_id)
    if not a:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    a.status = "cancelado"
    db.commit()
    return {"ok": True}