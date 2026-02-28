from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

class AgendamentoManual(BaseModel):
    especialista_id: int
    inicio: datetime
    fim: datetime

class AgendamentoAutomatico(BaseModel):
    opcao: str # "mesmo_profissional", "mais_proximo", "filtrar_modalidade", "lista_opcoes", "ia_decide"
    preferencias: Optional[dict] = None

class AgendamentoResposta(BaseModel):
    id: int
    paciente_id: int
    especialista_id: int
    inicio: datetime
    fim: datetime
    status: str
    tipo: str
    confirmado: bool

    class Config:
        from_attributes = True

class SugestaoIA(BaseModel):
    sugestao_id: int
    especialista_id: int
    nome_especialista: str
    inicio: datetime
    fim: datetime
    mensagem: str
