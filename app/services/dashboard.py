from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.database.models import Patient, Specialist, Appointment, QueueEntry


def get_dashboard(db: Session) -> dict:
    total_pacientes = db.scalar(select(func.count()).select_from(Patient)) or 0
    total_especialistas = db.scalar(select(func.count()).select_from(Specialist)) or 0
    agendamentos_ativos = db.scalar(
        select(func.count()).select_from(Appointment).where(Appointment.status == "agendado")
    ) or 0
    fila_aguardando = db.scalar(
        select(func.count()).select_from(QueueEntry).where(QueueEntry.status == "aguardando")
    ) or 0

    return {
        "total_pacientes": int(total_pacientes),
        "total_especialistas": int(total_especialistas),
        "agendamentos_ativos": int(agendamentos_ativos),
        "fila_aguardando": int(fila_aguardando),
    }