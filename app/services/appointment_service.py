from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.appointment import Appointment
from app.schemas.appointment import AppointmentCreate
from app.repositories.appointment_repository import appointment_repository
from app.repositories.schedule_repository import schedule_repository
from app.repositories.specialist_repository import specialist_repository

class AppointmentService:
    def create(self, db: Session, patient_id: int, obj_in: AppointmentCreate) -> Appointment:
        # 1. Verificar se o Specialist existe
        specialist = specialist_repository.get(db, id=obj_in.specialist_id)
        if not specialist:
             raise HTTPException(status_code=404, detail="Especialista não encontrado")
             
        # 2. Verificar se o Schedule pertence ao Specialist e está disponível
        schedule = schedule_repository.get(db, id=obj_in.schedule_id)
        if not schedule:
             raise HTTPException(status_code=404, detail="Horário não encontrado")
             
        if schedule.specialist_id != obj_in.specialist_id:
             raise HTTPException(status_code=400, detail="Este horário não pertence a este especialista")
             
        if not schedule.is_available:
             raise HTTPException(status_code=400, detail="Este horário já não está mais disponível")

        # 3. Criar a consulta (Appointment)
        appointment_data = {
            "patient_id": patient_id,
            "specialist_id": obj_in.specialist_id,
            "schedule_id": obj_in.schedule_id,
            "status": "CONFIRMADO"
        }
        appointment = appointment_repository.create(db, obj_in=appointment_data)
        
        # 4. Alterar a disponibilidade do horário
        schedule_repository.update(db, db_obj=schedule, obj_in={"is_available": False})
        
        return appointment

    def cancel(self, db: Session, appointment_id: int, user_id: int, is_admin: bool = False) -> Appointment:
        appointment = appointment_repository.get(db, id=appointment_id)
        if not appointment:
             raise HTTPException(status_code=404, detail="Consulta não encontrada")
             
        # Verifica se o paciente ou especialista cancelando é o dono, ou admin
        if not is_admin:
            # Precisa checar se user_id pertence ao patient ou ao specialist
            pass # Simplificaremos a checagem no endpoint
            
        if appointment.status == "CANCELADO":
             raise HTTPException(status_code=400, detail="Consulta já está cancelada")
             
        # Cancela a consulta
        appointment = appointment_repository.update(db, db_obj=appointment, obj_in={"status": "CANCELADO"})
        
        # Libera o horário
        schedule = schedule_repository.get(db, id=appointment.schedule_id)
        if schedule:
            schedule_repository.update(db, db_obj=schedule, obj_in={"is_available": True})
            
        return appointment
        
    def get_by_patient(self, db: Session, patient_id: int) -> List[Appointment]:
        return appointment_repository.get_by_patient(db, patient_id=patient_id)

appointment_service = AppointmentService()
