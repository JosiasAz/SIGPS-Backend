from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database.db import get_db
from app.database.models import Specialist, Specialty
from app.routers.deps import require_staff, require_view
from app.schemas.specialists import (
    SpecialistCreate, SpecialistUpdate, SpecialistResponse,
    SpecialtyCreate, SpecialtyResponse
)

router = APIRouter(prefix="/specialists", tags=["Specialists"])


@router.post("/specialties", response_model=SpecialtyResponse)
def create_specialty(
    data: SpecialtyCreate,
    db: Session = Depends(get_db),
    _=Depends(require_staff),
):
    s = Specialty(nome=data.nome.strip())
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


@router.get("/specialties", response_model=list[SpecialtyResponse])
def list_specialties(
    db: Session = Depends(get_db),
    _=Depends(require_view),
):
    return list(db.scalars(select(Specialty)).all())


@router.post("", response_model=SpecialistResponse)
def create_specialist(
    data: SpecialistCreate,
    db: Session = Depends(get_db),
    _=Depends(require_staff),
):
    sp = Specialist(**data.model_dump())
    db.add(sp)
    db.commit()
    db.refresh(sp)
    return sp


@router.get("", response_model=list[SpecialistResponse])
def list_specialists(
    db: Session = Depends(get_db),
    _=Depends(require_view),
):
    return list(db.scalars(select(Specialist)).all())


@router.get("/{specialist_id}", response_model=SpecialistResponse)
def get_specialist(
    specialist_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_view),
):
    sp = db.get(Specialist, specialist_id)
    if not sp:
        raise HTTPException(status_code=404, detail="Especialista não encontrado")
    return sp


@router.patch("/{specialist_id}", response_model=SpecialistResponse)
def update_specialist(
    specialist_id: int,
    data: SpecialistUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_staff),
):
    sp = db.get(Specialist, specialist_id)
    if not sp:
        raise HTTPException(status_code=404, detail="Especialista não encontrado")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(sp, k, v)

    db.commit()
    db.refresh(sp)
    return sp


@router.delete("/{specialist_id}")
def delete_specialist(
    specialist_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_staff),
):
    sp = db.get(Specialist, specialist_id)
    if not sp:
        raise HTTPException(status_code=404, detail="Especialista não encontrado")
    db.delete(sp)
    db.commit()
    return {"ok": True}