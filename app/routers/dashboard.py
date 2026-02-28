from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.database.db import obter_sessao_db
from app.routers.deps import exigir_leitura
from app.core.responses import standard_response
from app.database.models import Agendamento, EntradaFila

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/kpis")
def get_kpis(db: Session = Depends(obter_sessao_db), _=Depends(exigir_leitura)):
    # Calculate mock or real KPIs
    total_agendamentos = db.scalar(select(func.count(Agendamento.id)))
    na_fila = db.scalar(select(func.count(EntradaFila.id)).where(EntradaFila.status == "aguardando"))
    
    data = {
        "taxa_ocupacao": 0.85, # mock
        "tempo_medio_espera_minutos": 12, # mock
        "total_agendamentos": total_agendamentos,
        "pacientes_na_fila": na_fila
    }
    return standard_response(True, data=data)

@router.get("/agendamentos")
def get_dashboard_agendamentos(db: Session = Depends(obter_sessao_db), _=Depends(exigir_leitura)):
    # Visão consolidada
    # In a real app, group by date or specialty
    return standard_response(True, data=[], message="Visão consolidada em implementação")

@router.get("/fila")
def get_dashboard_fila(db: Session = Depends(obter_sessao_db), _=Depends(exigir_leitura)):
    # Status atual da lista de espera
    return standard_response(True, data=[], message="Status da fila detalhado em implementação")
