from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from app.database.db import obter_sessao_db
from app.database.models import Agendamento, Paciente, Especialista, Usuario
from app.routers.deps import obter_usuario_atual, exigir_leitura
from app.core.responses import standard_response
from app.core.security import PERFIL_PACIENTE, PERFIL_ESPECIALISTA, PERFIL_ADMIN, PERFIL_GESTOR
from app.schemas.agendamentos import AgendamentoManual, AgendamentoAutomatico, AgendamentoResposta, SugestaoIA

router = APIRouter(prefix="/agendamentos", tags=["Agendamentos"])

@router.post("/manual")
def agendamento_manual(
    dados: AgendamentoManual,
    db: Session = Depends(obter_sessao_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    # RBAC: only paciente can book for themselves
    if usuario_atual.perfil != PERFIL_PACIENTE:
        return standard_response(False, message="Somente pacientes podem realizar agendamentos manuais", status_code=403)
    
    paciente = db.scalar(select(Paciente).where(Paciente.usuario_id == usuario_atual.id))
    if not paciente:
        return standard_response(False, message="Perfil de paciente não encontrado", status_code=404)

    # Check for conflicts
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
        return standard_response(False, message="Horário já ocupado", error_code="CONFLICT", status_code=409)

    ag = Agendamento(
        paciente_id=paciente.id,
        especialista_id=dados.especialista_id,
        inicio=dados.inicio,
        fim=dados.fim,
        status="agendado",
        tipo="manual",
        confirmado=1
    )
    db.add(ag)
    db.commit()
    db.refresh(ag)
    
    return standard_response(True, data=AgendamentoResposta.model_validate(ag).model_dump(), message="Agendamento realizado com sucesso")

@router.post("/automatico")
def agendamento_automatico(
    dados: AgendamentoAutomatico,
    db: Session = Depends(obter_sessao_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    if usuario_atual.perfil != PERFIL_PACIENTE:
        return standard_response(False, message="Somente pacientes", status_code=403)
    
    paciente = db.scalar(select(Paciente).where(Paciente.usuario_id == usuario_atual.id))
    
    # Mock logic for IA suggestions
    # In a real system, we'd query available specialists and slots
    esp = db.scalars(select(Especialista)).first()
    if not esp:
        return standard_response(False, message="Nenhum especialista disponível", status_code=404)

    # Suggestion mock
    inicio_sugestao = datetime.now() + timedelta(days=1, hours=9)
    fim_sugestao = inicio_sugestao + timedelta(minutes=60)
    
    # Save as 'sugestao' pending confirmation
    ag = Agendamento(
        paciente_id=paciente.id,
        especialista_id=esp.id,
        inicio=inicio_sugestao,
        fim=fim_sugestao,
        status="sugestao",
        tipo="automatico",
        confirmado=0
    )
    db.add(ag)
    db.commit()
    db.refresh(ag)

    sugestao = SugestaoIA(
        sugestao_id=ag.id,
        especialista_id=esp.id,
        nome_especialista=esp.nome,
        inicio=ag.inicio,
        fim=ag.fim,
        mensagem=f"Sugestão baseada em {dados.opcao}: {esp.nome} no dia {ag.inicio.strftime('%d/%m às %H:%M')}"
    )

    return standard_response(True, data=sugestao.model_dump())

@router.post("/confirmar/{sugestao_id}")
def confirmar_agendamento(
    sugestao_id: int,
    db: Session = Depends(obter_sessao_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    ag = db.get(Agendamento, sugestao_id)
    if not ag or ag.status != "sugestao":
        return standard_response(False, message="Sugestão não encontrada ou já processada", status_code=404)
    
    paciente = db.scalar(select(Paciente).where(Paciente.usuario_id == usuario_atual.id))
    if ag.paciente_id != paciente.id:
        return standard_response(False, message="Ação não permitida", status_code=403)
    
    ag.status = "agendado"
    ag.confirmado = 1
    db.commit()
    
    return standard_response(True, data=AgendamentoResposta.model_validate(ag).model_dump(), message="Agendamento confirmado")

@router.get("")
def listar_agendamentos(
    db: Session = Depends(obter_sessao_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    query = select(Agendamento)
    
    if usuario_atual.perfil == PERFIL_PACIENTE:
        paciente = db.scalar(select(Paciente).where(Paciente.usuario_id == usuario_atual.id))
        query = query.where(Agendamento.paciente_id == paciente.id)
    elif usuario_atual.perfil == PERFIL_ESPECIALISTA:
        esp = db.scalar(select(Especialista).where(Especialista.usuario_id == usuario_atual.id))
        query = query.where(Agendamento.especialista_id == esp.id)
    elif usuario_atual.perfil not in (PERFIL_ADMIN, PERFIL_GESTOR, "visualizador"):
        return standard_response(False, message="Sem permissão", status_code=403)
    
    agendamentos = db.scalars(query).all()
    data = [AgendamentoResposta.model_validate(a).model_dump() for a in agendamentos]
    
    return standard_response(True, data=data)

@router.put("/{id}")
def editar_agendamento(
    id: int,
    dados: AgendamentoManual, # Reuse manual schema for edit
    db: Session = Depends(obter_sessao_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    ag = db.get(Agendamento, id)
    if not ag:
        return standard_response(False, message="Agendamento não encontrado", status_code=404)
    
    # Specialists can edit/confirm their own
    # Gestor/Admin can edit any
    can_edit = False
    if usuario_atual.perfil in (PERFIL_ADMIN, PERFIL_GESTOR):
        can_edit = True
    elif usuario_atual.perfil == PERFIL_ESPECIALISTA:
        esp = db.scalar(select(Especialista).where(Especialista.usuario_id == usuario_atual.id))
        if ag.especialista_id == esp.id:
            can_edit = True
            
    if not can_edit:
        return standard_response(False, message="Sem permissão", status_code=403)
    
    ag.inicio = dados.inicio
    ag.fim = dados.fim
    db.commit()
    
    return standard_response(True, message="Agendamento atualizado")

@router.delete("/{id}")
def cancelar_agendamento(
    id: int,
    db: Session = Depends(obter_sessao_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    ag = db.get(Agendamento, id)
    if not ag:
        return standard_response(False, message="Agendamento não encontrado", status_code=404)
    
    can_cancel = False
    if usuario_atual.perfil in (PERFIL_ADMIN, PERFIL_GESTOR):
        can_cancel = True
    elif usuario_atual.perfil == PERFIL_PACIENTE:
        paciente = db.scalar(select(Paciente).where(Paciente.usuario_id == usuario_atual.id))
        if ag.paciente_id == paciente.id:
            # Optionally check deadline here
            can_cancel = True
            
    if not can_cancel:
        return standard_response(False, message="Sem permissão", status_code=403)
    
    ag.status = "cancelado"
    db.commit()
    
    return standard_response(True, message="Agendamento cancelado")
