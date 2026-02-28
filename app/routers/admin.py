from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database.db import obter_sessao_db
from app.database.models import Usuario, Especialista, Paciente
from app.routers.deps import exigir_admin
from app.core.security import gerar_hash_senha
from app.core.responses import standard_response
from app.schemas.auth import UserRegister, UserResponse
from app.ml.model import treinar_IA

router = APIRouter(prefix="/admin", tags=["Administração"])

@router.post("/usuarios")
def create_internal_user(dados: UserRegister, db: Session = Depends(obter_sessao_db), _=Depends(exigir_admin)):
    """Criar perfis internos (gestor, visualizador)."""
    existente = db.scalar(select(Usuario).where(Usuario.email == str(dados.email).lower()))
    if existente:
        return standard_response(False, message="Email já cadastrado", status_code=409)

    novo = Usuario(
        email=str(dados.email).lower(),
        senha_hash=gerar_hash_senha(dados.password),
        perfil=dados.role
    )
    db.add(novo)
    db.commit()
    return standard_response(True, message=f"Usuário {novo.email} criado com perfil {novo.perfil}")

@router.get("/usuarios")
def list_all_users(db: Session = Depends(obter_sessao_db), _=Depends(exigir_admin)):
    """Listar todos os usuários."""
    users = db.scalars(select(Usuario)).all()
    data = [{"id": u.id, "email": u.email, "role": u.perfil} for u in users]
    return standard_response(True, data=data)

@router.put("/usuarios/{id}")
def update_user(id: int, dados: dict = Body(...), db: Session = Depends(obter_sessao_db), _=Depends(exigir_admin)):
    """Editar usuário."""
    user = db.get(Usuario, id)
    if not user:
        return standard_response(False, message="Usuário não encontrado", status_code=404)
    
    if "role" in dados:
        user.perfil = dados["role"]
    if "password" in dados:
        user.senha_hash = gerar_hash_senha(dados["password"])
        
    db.commit()
    return standard_response(True, message="Usuário atualizado")

@router.delete("/usuarios/{id}")
def deactivate_user(id: int, db: Session = Depends(obter_sessao_db), _=Depends(exigir_admin)):
    """Desativar usuário."""
    user = db.get(Usuario, id)
    if not user:
        return standard_response(False, message="Usuário não encontrado", status_code=404)
    db.delete(user)
    db.commit()
    return standard_response(True, message="Usuário removido")

@router.post("/especialistas/vincular")
def vincular_especialista(dados: dict = Body(...), db: Session = Depends(obter_sessao_db), _=Depends(exigir_admin)):
    """Vincular especialista à clínica/consultório."""
    # Logic for linking specialist to clinic record
    return standard_response(True, message="Especialista vinculado")

@router.get("/configuracoes")
def get_config(db: Session = Depends(obter_sessao_db), _=Depends(exigir_admin)):
    """Parâmetros do sistema e do modelo de IA."""
    return standard_response(True, data={
        "especialidades_cadastradas": [],
        "ia_parametros": {
            "n_amostras_treino": 300,
            "modelo_atual": "modelo.pkl"
        }
    })

@router.post("/configuracoes/ia/treinar")
def treinar_modelo_ia(n_amostras: int = 300, db: Session = Depends(obter_sessao_db), _=Depends(exigir_admin)):
    """Acionar treinamento do modelo de priorização."""
    try:
        nome, precisao = treinar_IA(n_amostras=n_amostras)
        return standard_response(True, data={"modelo": nome, "precisao": precisao}, message="Modelo treinado com sucesso")
    except Exception as e:
        return standard_response(False, message=f"Erro ao treinar modelo: {str(e)}", status_code=500)

@router.get("/auditoria")
def get_audit(db: Session = Depends(obter_sessao_db), _=Depends(exigir_admin)):
    """Log de acessos e ações críticas."""
    return standard_response(True, data=[], message="Logs de auditoria")
