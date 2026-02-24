from pydantic import BaseModel


class IA_PedidoTreino(BaseModel):
    n_amostras: int = 300


class IA_RespostaTreino(BaseModel):
    nome_modelo_ia: str
    precisao: float


class IA_PedidoPredicao(BaseModel):
    idade: int
    renda: float
    gastos: float


class IA_RespostaPredicao(BaseModel):
    prioridade: int
    pontuacao: float