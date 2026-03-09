from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    specialist_id = Column(Integer, ForeignKey("specialists.id"), nullable=False)
    schedule_id = Column(Integer, ForeignKey("schedules.id"), unique=True, nullable=False)
    status = Column(String(50), default="CONFIRMADO", nullable=False) # CONFIRMADO, CANCELADO, REALIZADO
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    patient = relationship("Patient", back_populates="appointments")
    specialist = relationship("Specialist", back_populates="appointments")
    schedule = relationship("Schedule", back_populates="appointment")
