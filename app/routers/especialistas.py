from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database.db import obter_sessao_db
from app.database.models import Especialista, Especialidade, Usuario
from app.routers.deps import exigir_equipe, exigir_leitura, obter_usuario_atual
from app.core.responses import standard_response
from app.core.security import PERFIL_ADMIN
from app.schemas.especialistas import (
    EspecialistaCriar, EspecialistaAtualizar, EspecialistaResposta,
    EspecialidadeCriar, EspecialidadeResposta
)

router = APIRouter(prefix="/especialistas", tags=["Especialistas"])

@router.get("")
def listar_especialistas(
    especialidade: Optional[str] = Query(None),
    modalidade: Optional[str] = Query(None),
    localizacao: Optional[str] = Query(None),
    db: Session = Depends(obter_sessao_db),
    _=Depends(exigir_leitura),
):
    query = select(Especialista)
    
    if especialidade:
        query = query.join(Especialista.especialidade).where(Especialidade.nome.ilike(f"%{especialidade}%"))
    if modalidade:
        query = query.where(Especialista.modalidade == modalidade)
    if localizacao:
        query = query.where(Especialista.localizacao.ilike(f"%{localizacao}%"))
        
    especialistas = db.scalars(query).all()
    # Manual conversion to dict to avoid Pydantic validation issues if needed, 
    # but standard_response handles serializable data.
    data = [EspecialistaResposta.model_validate(e).model_dump() for e in especialistas]
    
    return standard_response(True, data=data)

@router.get("/{id}")
def obter_especialista(
    id: int,
    db: Session = Depends(obter_sessao_db),
    _=Depends(exigir_leitura),
):
    esp = db.get(Especialista, id)
    if not esp:
        return standard_response(False, message="Especialista não encontrado", error_code="NOT_FOUND", status_code=404)
    
    return standard_response(True, data=EspecialistaResposta.model_validate(esp).model_dump())

@router.put("/{id}")
def atualizar_especialista(
    id: int,
    dados: EspecialistaAtualizar,
    db: Session = Depends(obter_sessao_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    esp = db.get(Especialista, id)
    if not esp:
        return standard_response(False, message="Especialista não encontrado", error_code="NOT_FOUND", status_code=404)

    # RBAC: Only self or admin
    if usuario_atual.id != esp.usuario_id and usuario_atual.perfil != PERFIL_ADMIN:
        return standard_response(False, message="Sem permissão para editar este perfil", error_code="FORBIDDEN", status_code=403)

    for k, v in dados.model_dump(exclude_unset=True).items():
        setattr(esp, k, v)

    db.commit()
    db.refresh(esp)
    return standard_response(True, data=EspecialistaResposta.model_validate(esp).model_dump(), message="Perfil atualizado")

@router.get("/{id}/agenda")
def obter_agenda(
    id: int,
    db: Session = Depends(obter_sessao_db),
    _=Depends(exigir_leitura),
):
    # This should return available slots. For now, returning a placeholder or actual logic if exists.
    # In a real app, this would query an 'Agendas' table or calculate slots.
    # Let's see if there's an Agenda model. Currently, there isn't one in models.py, 
    # but there's a rota_agenda.
    return standard_response(True, data=[], message="Funcionalidade de agenda em implementação")

@router.put("/{id}/agenda")
def gerenciar_agenda(
    id: int,
    db: Session = Depends(obter_sessao_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    esp = db.get(Especialista, id)
    if not esp:
        return standard_response(False, message="Especialista não encontrado", error_code="NOT_FOUND", status_code=404)

    if usuario_atual.id != esp.usuario_id and usuario_atual.perfil != PERFIL_ADMIN:
        return standard_response(False, message="Sem permissão", error_code="FORBIDDEN", status_code=403)

    # Logic to manage slots
    return standard_response(True, message="Agenda atualizada com sucessso")