from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_pacientes: int
    total_especialistas: int
    agendamentos_ativos: int
    fila_aguardando: int