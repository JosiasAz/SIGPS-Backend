from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database.db import obter_sessao_db
from app.database.models import Paciente
from app.routers.deps import exigir_equipe, exigir_leitura
from app.schemas.pacientes import PacienteCriar, PacienteAtualizar, PacienteResposta

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


@router.post("", response_model=PacienteResposta)
def criar_paciente(
    dados: PacienteCriar,
    db: Session = Depends(obter_sessao_db),
    _=Depends(exigir_equipe),
):
    p = Paciente(**dados.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


@router.get("", response_model=list[PacienteResposta])
def listar_pacientes(
    db: Session = Depends(obter_sessao_db),
    _=Depends(exigir_leitura),
):
    return list(db.scalars(select(Paciente)).all())


@router.get("/{paciente_id}", response_model=PacienteResposta)
def obter_paciente(
    paciente_id: int,
    db: Session = Depends(obter_sessao_db),
    _=Depends(exigir_leitura),
):
    p = db.get(Paciente, paciente_id)
    if not p:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return p


@router.patch("/{paciente_id}", response_model=PacienteResposta)
def atualizar_paciente(
    paciente_id: int,
    dados: PacienteAtualizar,
    db: Session = Depends(obter_sessao_db),
    _=Depends(exigir_equipe),
):
    p = db.get(Paciente, paciente_id)
    if not p:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    for k, v in dados.model_dump(exclude_unset=True).items():
        setattr(p, k, v)

    db.commit()
    db.refresh(p)
    return p


@router.delete("/{paciente_id}")
def remover_paciente(
    paciente_id: int,
    db: Session = Depends(obter_sessao_db),
    _=Depends(exigir_equipe),
):
    p = db.get(Paciente, paciente_id)
    if not p:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    db.delete(p)
    db.commit()
    return {"ok": True}
