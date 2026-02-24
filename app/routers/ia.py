from fastapi import APIRouter, Depends, HTTPException

from app.routers.deps import exigir_admin, exigir_equipe
from app.schemas.ia import IA_PedidoTreino, IA_RespostaTreino, IA_PedidoPredicao, IA_RespostaPredicao
from app.ml.model import treinar_IA, prever_prioridade

router = APIRouter(prefix="/ia", tags=["Inteligência Artificial"])


@router.post("/treinar", response_model=IA_RespostaTreino)
def treinar(dados: IA_PedidoTreino, _=Depends(exigir_admin)):
    nome_modelo, precisao = treinar_IA(n_amostras=dados.n_amostras)
    return IA_RespostaTreino(nome_modelo_ia=nome_modelo, precisao=precisao)


@router.post("/prever", response_model=IA_RespostaPredicao)
def prever(dados: IA_PedidoPredicao, _=Depends(exigir_equipe)):
    try:
        prioridade, pontuacao = prever_prioridade(dados.idade, dados.renda, dados.gastos)
        return IA_RespostaPredicao(prioridade=prioridade, pontuacao=pontuacao)
    except FileNotFoundError:
        raise HTTPException(status_code=409, detail="Modelo não encontrado. Treine primeiro em /ia/treinar (admin).")