from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_active_user
from app.core.permissions import is_admin, is_especialista
from app.models.user import User
from app.schemas.specialist import SpecialistResponse
from app.schemas.schedule import ScheduleCreate, ScheduleResponse
from app.services.specialist_service import specialist_service
from app.services.schedule_service import schedule_service

router = APIRouter()

@router.get("/", response_model=List[SpecialistResponse])
def get_active_specialists(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retorna todos os especialistas ativos. Qq usuário logado pode ver.
    """
    return specialist_service.get_ativos(db)

@router.patch("/{specialist_id}/approve", response_model=SpecialistResponse)
def approve_specialist(
    specialist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(is_admin),
) -> Any:
    """
    Aprova um especialista que estava pendente. Apenas admin.
    """
    return specialist_service.approve(db, specialist_id=specialist_id)

@router.post("/schedules", response_model=ScheduleResponse)
def create_schedule(
    *,
    db: Session = Depends(get_db),
    schedule_in: ScheduleCreate,
    current_user: User = Depends(is_especialista),
) -> Any:
    """
    Especialista cria seus horários de atendimento.
    """
    specialist = specialist_service.get_by_user_id(db, user_id=current_user.id)
    return schedule_service.create(db, specialist_id=specialist.id, obj_in=schedule_in)
