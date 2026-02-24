from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import criar_token_acesso, gerar_hash_senha, verificar_senha, TODOS_PERFIS
from app.database.db import obter_sessao_db
from app.database.models import Usuario
from app.schemas.auth import CadastroUsuario, LoginUsuario, RespostaLogin

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/registrar")
def registrar(dados: CadastroUsuario, db: Session = Depends(obter_sessao_db)):
    perfil = dados.perfil.strip().lower()
    if perfil not in TODOS_PERFIS:
        raise HTTPException(status_code=422, detail=f"Perfil inválido: {perfil}")

    usuario = Usuario(
        email=str(dados.email).lower(),
        senha_hash=gerar_hash_senha(dados.senha),
        perfil=perfil,
    )
    db.add(usuario)
    try:
        db.commit()
        db.refresh(usuario)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email já cadastrado")

    return {"id": usuario.id, "email": usuario.email, "perfil": usuario.perfil}


@router.post("/login", response_model=RespostaLogin)
def entrar(dados: LoginUsuario, db: Session = Depends(obter_sessao_db)):
    usuario = db.scalar(select(Usuario).where(Usuario.email == str(dados.email).lower()))
    if not usuario or not verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    tok = criar_token_acesso(usuario.id, usuario.perfil)
    return RespostaLogin(
        token_acesso=tok["token"],
        expira_em=tok["expires_at"].isoformat(),
    )