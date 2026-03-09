from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.utils.enums import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean(), default=True)

    # Relacionamentos
    patient = relationship("Patient", back_populates="user", uselist=False)
    specialist = relationship("Specialist", back_populates="user", uselist=False)
