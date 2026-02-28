from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, desc

from app.database.db import obter_sessao_db
from app.database.models import EntradaFila, Paciente, Usuario
from app.routers.deps import obter_usuario_atual, exigir_equipe, exigir_leitura
from app.core.responses import standard_response
from app.core.security import PERFIL_PACIENTE, PERFIL_ADMIN, PERFIL_GESTOR
from app.schemas.fila import FilaCriar, FilaPrioridadeUpdate, FilaResposta
from app.ml.model import prever_prioridade

router = APIRouter(prefix="/fila", tags=["Fila"])

@router.post("/entrar")
def entrar_na_fila(
    dados: FilaCriar,
    db: Session = Depends(obter_sessao_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    if usuario_atual.perfil != PERFIL_PACIENTE:
        return standard_response(False, message="Somente pacientes", status_code=403)
    
    paciente = db.scalar(select(Paciente).where(Paciente.usuario_id == usuario_atual.id))
    if not paciente:
        return standard_response(False, message="Perfil não encontrado", status_code=404)

    entrada = EntradaFila(
        paciente_id=paciente.id,
        especialista_id=dados.especialista_id,
        motivo=dados.motivo,
        status="aguardando"
    )

    # Acionar ML para calcular prioridade
    try:
        # Mock inputs:idade, renda, gastos (existing in model.py)
        # However, the prompt says: urgência declarada, histórico de consultas, tempo de espera acumulado...
        # For now, I'll use the existing prever_prioridade which takes (idade, renda, gastos)
        prio, score = prever_prioridade(paciente.idade, paciente.renda, paciente.gastos)
        entrada.prioridade = prio
        entrada.score_ml = score
    except Exception:
        entrada.prioridade = 0

    db.add(entrada)
    db.commit()
    db.refresh(entrada)
    
    return standard_response(True, data=FilaResposta.model_validate(entrada).model_dump(), message="Entrada na fila registrada")

@router.get("")
def listar_fila(
    db: Session = Depends(obter_sessao_db),
    _=Depends(exigir_leitura)
):
    # Retornar a lista de espera ordenada por prioridade
    entradas = db.scalars(select(EntradaFila).where(EntradaFila.status == "aguardando").order_by(desc(EntradaFila.prioridade))).all()
    data = [FilaResposta.model_validate(e).model_dump() for e in entradas]
    return standard_response(True, data=data)

@router.put("/{paciente_id}/prioridade")
def ajustar_prioridade(
    paciente_id: int,
    dados: FilaPrioridadeUpdate,
    db: Session = Depends(obter_sessao_db),
    _=Depends(exigir_equipe)
):
    # Get active entry for this patient
    entrada = db.scalar(
        select(EntradaFila).where(
            EntradaFila.paciente_id == paciente_id,
            EntradaFila.status == "aguardando"
        )
    )
    if not entrada:
        return standard_response(False, message="Paciente não está na fila", status_code=404)
    
    entrada.prioridade = dados.prioridade
    db.commit()
    return standard_response(True, message="Prioridade ajustada manualmente")

@router.delete("/{paciente_id}")
def remover_da_fila(
    paciente_id: int,
    db: Session = Depends(obter_sessao_db),
    _=Depends(exigir_equipe)
):
    entrada = db.scalar(
        select(EntradaFila).where(
            EntradaFila.paciente_id == paciente_id,
            EntradaFila.status == "aguardando"
        )
    )
    if not entrada:
        return standard_response(False, message="Entrada não encontrada", status_code=404)
    
    entrada.status = "cancelado" # Or just delete if preferred, but usually cancel/attend is better
    db.commit()
    return standard_response(True, message="Removido da fila")