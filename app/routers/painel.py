from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import obter_sessao_db
from app.routers.deps import exigir_leitura
from app.schemas.painel import DashboardResposta
from app.services.painel import obter_dados_dashboard

router = APIRouter(prefix="/painel", tags=["Painel"])


@router.get("", response_model=DashboardResposta)
def obter_dashboard(
    db: Session = Depends(obter_sessao_db),
    _=Depends(exigir_leitura),
):
    return obter_dados_dashboard(db)