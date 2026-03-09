from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_active_user
from app.core.permissions import is_paciente
from app.models.user import User
from app.schemas.appointment import AppointmentCreate, AppointmentResponse
from app.services.appointment_service import appointment_service
from app.services.patient_service import patient_service
from app.utils.enums import UserRole

router = APIRouter()

@router.post("/", response_model=AppointmentResponse)
def create_appointment(
    *,
    db: Session = Depends(get_db),
    appointment_in: AppointmentCreate,
    current_user: User = Depends(is_paciente),
) -> Any:
    """
    Paciente realiza o agendamento (Gatilha a lógica de reserva e retira a disponibilidade).
    """
    patient = patient_service.get_by_user_id(db, user_id=current_user.id)
    return appointment_service.create(db, patient_id=patient.id, obj_in=appointment_in)

@router.patch("/{appointment_id}/cancel", response_model=AppointmentResponse)
def cancel_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Cancela a consulta e libera o horário novamente.
    """
    is_admin = current_user.role in [UserRole.ADMIN, UserRole.GESTOR]
    return appointment_service.cancel(db, appointment_id=appointment_id, user_id=current_user.id, is_admin=is_admin)

@router.get("/me", response_model=List[AppointmentResponse])
def read_my_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(is_paciente),
) -> Any:
    """
    Retorna as consultas do paciente logado.
    """
    patient = patient_service.get_by_user_id(db, user_id=current_user.id)
    return appointment_service.get_by_patient(db, patient_id=patient.id)
