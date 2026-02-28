from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import decodificar_token, obter_token_bearer
from app.database.db import obter_sessao_db
from app.database.models import Usuario
from app.core.security import PERFIL_ADMIN, PERFIL_GESTOR, PERFIL_PACIENTE, PERFIL_VISUALIZADOR, PERFIL_ESPECIALISTA


def obter_usuario_atual(
    db: Session = Depends(obter_sessao_db),
    token: str = Depends(obter_token_bearer),
) -> Usuario:
    payload = decodificar_token(token)
    usuario_id = payload.get("sub")
    if not usuario_id:
        raise HTTPException(status_code=401, detail="Token inválido (sem sub)")
    usuario = db.get(Usuario, int(usuario_id))
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não existe")
    return usuario


def exigir_perfis(*perfis: str):
    def _guard(usuario: Usuario = Depends(obter_usuario_atual)) -> Usuario:
        if usuario.perfil not in perfis:
            raise HTTPException(status_code=403, detail="Sem permissão")
        return usuario
    return _guard


exigir_admin = exigir_perfis(PERFIL_ADMIN)
exigir_equipe = exigir_perfis(PERFIL_ADMIN, PERFIL_GESTOR)
exigir_operacao = exigir_perfis(PERFIL_ADMIN, PERFIL_GESTOR, PERFIL_PACIENTE, PERFIL_ESPECIALISTA)
exigir_leitura = exigir_perfis(PERFIL_ADMIN, PERFIL_GESTOR, PERFIL_PACIENTE, PERFIL_VISUALIZADOR, PERFIL_ESPECIALISTA)
