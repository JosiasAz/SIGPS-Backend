from sqlalchemy import Column, Integer, Date, Time, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    specialist_id = Column(Integer, ForeignKey("specialists.id"), nullable=False)
    data = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)

    # Relacionamentos
    specialist = relationship("Specialist", back_populates="schedules")
    appointment = relationship("Appointment", back_populates="schedule", uselist=False)
