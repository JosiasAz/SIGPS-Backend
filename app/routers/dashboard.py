from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.routers.deps import require_view
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard import get_dashboard

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("", response_model=DashboardResponse)
def dashboard(
    db: Session = Depends(get_db),
    _=Depends(require_view),
):
    return get_dashboard(db)