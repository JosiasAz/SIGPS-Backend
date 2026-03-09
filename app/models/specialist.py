from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.utils.enums import SpecialistStatus

class Specialist(Base):
    __tablename__ = "specialists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    nome_completo = Column(String(255), nullable=False)
    registro_profissional = Column(String(50), unique=True, nullable=False)
    especialidade = Column(String(100), nullable=False)
    bio = Column(Text)
    modality = Column(String(50), nullable=False)  # Presencial/Online
    status = Column(Enum(SpecialistStatus), default=SpecialistStatus.PENDENTE, nullable=False)

    # Relacionamentos
    user = relationship("User", back_populates="specialist")
    schedules = relationship("Schedule", back_populates="specialist")
    appointments = relationship("Appointment", back_populates="specialist")
