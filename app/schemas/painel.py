from pydantic import BaseModel

class DashboardResposta(BaseModel):
    total_pacientes: int
    total_especialistas: int
    agendamentos_ativos: int
    fila_aguardando: int