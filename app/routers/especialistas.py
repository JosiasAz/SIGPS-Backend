from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database.db import obter_sessao_db
from app.database.models import Especialista, Especialidade
from app.routers.deps import exigir_equipe, exigir_leitura
from app.schemas.especialistas import (
    EspecialistaCriar, EspecialistaAtualizar, EspecialistaResposta,
    EspecialidadeCriar, EspecialidadeResposta
)

router = APIRouter(prefix="/especialistas", tags=["Especialistas"])


@router.post("/especialidades", response_model=EspecialidadeResposta)
def criar_especialidade(
    dados: EspecialidadeCriar,
    db: Session = Depends(obter_sessao_db),
    _=Depends(exigir_equipe),
):
    e = Especialidade(nome=dados.nome.strip())
    db.add(e)
    db.commit()
    db.refresh(e)
    return e


@router.get("/especialidades", response_model=list[EspecialidadeResposta])
def listar_especialidades(
    db: Session = Depends(obter_sessao_db),
    _=Depends(exigir_leitura),
):
    return list(db.scalars(select(Especialidade)).all())


@router.post("", response_model=EspecialistaResposta)
def criar_especialista(
    dados: EspecialistaCriar,
    db: Session = Depends(obter_sessao_db),
    _=Depends(exigir_equipe),
):
    esp = Especialista(**dados.model_dump())
    db.add(esp)
    db.commit()
    db.refresh(esp)
    return esp


@router.get("", response_model=list[EspecialistaResposta])
def listar_especialistas(
    db: Session = Depends(obter_sessao_db),
    _=Depends(exigir_leitura),
):
    return list(db.scalars(select(Especialista)).all())


@router.get("/{especialista_id}", response_model=EspecialistaResposta)
def obter_especialista(
    especialista_id: int,
    db: Session = Depends(obter_sessao_db),
    _=Depends(exigir_leitura),
):
    esp = db.get(Especialista, especialista_id)
    if not esp:
        raise HTTPException(status_code=404, detail="Especialista não encontrado")
    return esp


@router.patch("/{especialista_id}", response_model=EspecialistaResposta)
def atualizar_especialista(
    especialista_id: int,
    dados: EspecialistaAtualizar,
    db: Session = Depends(obter_sessao_db),
    _=Depends(exigir_equipe),
):
    esp = db.get(Especialista, especialista_id)
    if not esp:
        raise HTTPException(status_code=404, detail="Especialista não encontrado")

    for k, v in dados.model_dump(exclude_unset=True).items():
        setattr(esp, k, v)

    db.commit()
    db.refresh(esp)
    return esp


@router.delete("/{especialista_id}")
def remover_especialista(
    especialista_id: int,
    db: Session = Depends(obter_sessao_db),
    _=Depends(exigir_equipe),
):
    esp = db.get(Especialista, especialista_id)
    if not esp:
        raise HTTPException(status_code=404, detail="Especialista não encontrado")
    db.delete(esp)
    db.commit()
    return {"ok": True}