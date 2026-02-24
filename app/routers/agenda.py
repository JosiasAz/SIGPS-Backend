from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from app.database.db import obter_sessao_db
from app.database.models import Agendamento, Paciente, Especialista
from app.routers.deps import exigir_equipe, exigir_leitura
from app.schemas.agenda import AgendamentoCriar, AgendamentoResposta

router = APIRouter(prefix="/agenda", tags=["Agenda"])


@router.post("/agendamentos", response_model=AgendamentoResposta)
def criar_agendamento(
    dados: AgendamentoCriar,
    db: Session = Depends(obter_sessao_db),
    _=Depends(exigir_equipe),
):
    if not db.get(Paciente, dados.paciente_id):
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    if not db.get(Especialista, dados.especialista_id):
        raise HTTPException(status_code=404, detail="Especialista não encontrado")
    if dados.fim <= dados.inicio:
        raise HTTPException(status_code=422, detail="fim deve ser depois de início")

    # conflito simples: mesmo especialista com overlap
    conflito = db.scalar(
        select(Agendamento).where(
            and_(
                Agendamento.especialista_id == dados.especialista_id,
                Agendamento.status == "agendado",
                Agendamento.inicio < dados.fim,
                Agendamento.fim > dados.inicio,
            )
        )
    )
    if conflito:
        raise HTTPException(status_code=409, detail="Conflito de agenda para esse especialista")

    ag = Agendamento(**dados.model_dump(), status="agendado")
    db.add(ag)
    db.commit()
    db.refresh(ag)
    return ag


@router.get("/agendamentos", response_model=list[AgendamentoResposta])
def listar_agendamentos(
    db: Session = Depends(obter_sessao_db),
    _=Depends(exigir_leitura),
):
    return list(db.scalars(select(Agendamento)).all())


@router.post("/agendamentos/{agendamento_id}/cancelar")
def cancelar_agendamento(
    agendamento_id: int,
    db: Session = Depends(obter_sessao_db),
    _=Depends(exigir_equipe),
):
    ag = db.get(Agendamento, agendamento_id)
    if not ag:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    ag.status = "cancelado"
    db.commit()
    return {"ok": True}