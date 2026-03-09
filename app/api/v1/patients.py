from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_active_user
from app.core.permissions import is_paciente
from app.models.user import User
from app.schemas.patient import PatientResponse, PatientUpdate
from app.services.patient_service import patient_service

router = APIRouter()

@router.get("/me", response_model=PatientResponse)
def read_patient_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(is_paciente),
) -> Any:
    """
    Retorna os dados do paciente logado.
    """
    return patient_service.get_by_user_id(db, user_id=current_user.id)

@router.put("/me", response_model=PatientResponse)
def update_patient_me(
    *,
    db: Session = Depends(get_db),
    patient_in: PatientUpdate,
    current_user: User = Depends(is_paciente),
) -> Any:
    """
    Atualiza os dados do paciente logado.
    """
    return patient_service.update(db, user_id=current_user.id, obj_in=patient_in)
