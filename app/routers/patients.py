from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database.db import get_db
from app.database.models import Patient
from app.routers.deps import require_staff, require_view
from app.schemas.patients import PatientCreate, PatientUpdate, PatientResponse

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.post("", response_model=PatientResponse)
def create_patient(
    data: PatientCreate,
    db: Session = Depends(get_db),
    _=Depends(require_staff),
):
    p = Patient(**data.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


@router.get("", response_model=list[PatientResponse])
def list_patients(
    db: Session = Depends(get_db),
    _=Depends(require_view),
):
    return list(db.scalars(select(Patient)).all())


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_view),
):
    p = db.get(Patient, patient_id)
    if not p:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return p


@router.patch("/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: int,
    data: PatientUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_staff),
):
    p = db.get(Patient, patient_id)
    if not p:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(p, k, v)

    db.commit()
    db.refresh(p)
    return p


@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_staff),
):
    p = db.get(Patient, patient_id)
    if not p:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    db.delete(p)
    db.commit()
    return {"ok": True}