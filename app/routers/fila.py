from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database.db import obter_sessao_db
from app.database.models import EntradaFila, Paciente, Especialista
from app.routers.deps import exigir_operacao, exigir_leitura, exigir_equipe
from app.schemas.fila import FilaCriar, FilaAtualizarStatus, FilaResposta
from app.services.fila import obter_fila_ordenada
from app.ml.model import prever_prioridade

router = APIRouter(prefix="/fila", tags=["Fila"])


@router.post("", response_model=FilaResposta)
def adicionar_na_fila(
    dados: FilaCriar,
    db: Session = Depends(obter_sessao_db),
    _=Depends(exigir_operacao),
):
    paciente = db.get(Paciente, dados.paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    if dados.especialista_id is not None and not db.get(Especialista, dados.especialista_id):
        raise HTTPException(status_code=404, detail="Especialista não encontrado")

    ent = EntradaFila(**dados.model_dump(), status="aguardando")
    
    # IA automática: calcula prioridade com base nos dados do paciente
    try:
        prio_ia, score_ia = prever_prioridade(paciente.idade, paciente.renda, paciente.gastos)
        ent.prioridade = prio_ia
        ent.score_ml = score_ia
    except Exception:
        # Se a ML falhar (ex: não treinada), mantém a prioridade padrão do request
        pass

    db.add(ent)
    db.commit()
    db.refresh(ent)
    return ent


@router.get("", response_model=list[FilaResposta])
def listar_fila(
    db: Session = Depends(obter_sessao_db),
    _=Depends(exigir_leitura),
):
    return list(db.scalars(select(EntradaFila)).all())


@router.get("/ordenada", response_model=list[FilaResposta])
def obter_fila_ordenada_rota(
    db: Session = Depends(obter_sessao_db),
    _=Depends(exigir_leitura),
):
    return obter_fila_ordenada(db)


@router.patch("/{entrada_id}/status", response_model=FilaResposta)
def atualizar_status_fila(
    entrada_id: int,
    dados: FilaAtualizarStatus,
    db: Session = Depends(obter_sessao_db),
    _=Depends(exigir_equipe),
):
    ent = db.get(EntradaFila, entrada_id)
    if not ent:
        raise HTTPException(status_code=404, detail="Entrada da fila não encontrada")

    permitidos = {"aguardando", "chamado", "atendido", "cancelado"}
    if dados.status not in permitidos:
        raise HTTPException(status_code=422, detail="Status inválido")

    ent.status = dados.status
    db.commit()
    db.refresh(ent)
    return ent