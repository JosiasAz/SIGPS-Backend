from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.database.models import Paciente, Especialista, Agendamento, EntradaFila


def obter_dados_dashboard(db: Session) -> dict:
    total_pacientes = db.scalar(select(func.count()).select_from(Paciente)) or 0
    total_especialistas = db.scalar(select(func.count()).select_from(Especialista)) or 0
    agendamentos_ativos = db.scalar(
        select(func.count()).select_from(Agendamento).where(Agendamento.status == "agendado")
    ) or 0
    fila_aguardando = db.scalar(
        select(func.count()).select_from(EntradaFila).where(EntradaFila.status == "aguardando")
    ) or 0

    return {
        "total_pacientes": int(total_pacientes),
        "total_especialistas": int(total_especialistas),
        "agendamentos_ativos": int(agendamentos_ativos),
        "fila_aguardando": int(fila_aguardando),
    }