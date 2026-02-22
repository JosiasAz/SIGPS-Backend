from datetime import datetime
from sqlalchemy import (
    String, Integer, DateTime, ForeignKey, UniqueConstraint, Text, Enum, Float
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.db import Base

PERFIS = ("admin", "gestor", "recepcao", "visualizador")


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email", name="uq_users_email"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    perfil: Mapped[str] = mapped_column(Enum(*PERFIS), nullable=False, default="visualizador")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    telefone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    appointments = relationship("Appointment", back_populates="patient")
    queue_entries = relationship("QueueEntry", back_populates="patient")


class Specialty(Base):
    __tablename__ = "specialties"
    __table_args__ = (UniqueConstraint("nome", name="uq_specialties_nome"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)

    specialists = relationship("Specialist", back_populates="specialty")


class Specialist(Base):
    __tablename__ = "specialists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    formacao: Mapped[str | None] = mapped_column(String(255), nullable=True)
    registro: Mapped[str | None] = mapped_column(String(120), nullable=True)  # CRM/CRP etc
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)

    especialidade_id: Mapped[int | None] = mapped_column(ForeignKey("specialties.id"), nullable=True)
    specialty = relationship("Specialty", back_populates="specialists")

    appointments = relationship("Appointment", back_populates="specialist")
    queue_entries = relationship("QueueEntry", back_populates="specialist")


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)
    specialist_id: Mapped[int] = mapped_column(ForeignKey("specialists.id"), nullable=False)

    inicio: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fim: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    status: Mapped[str] = mapped_column(
        Enum("agendado", "concluido", "cancelado"),
        default="agendado",
        nullable=False,
    )

    patient = relationship("Patient", back_populates="appointments")
    specialist = relationship("Specialist", back_populates="appointments")


class QueueEntry(Base):
    __tablename__ = "queue_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)
    specialist_id: Mapped[int | None] = mapped_column(ForeignKey("specialists.id"), nullable=True)

    motivo: Mapped[str | None] = mapped_column(Text, nullable=True)
    prioridade: Mapped[int] = mapped_column(Integer, default=0)  # 0..100 (quanto maior, mais urgente)
    score_ml: Mapped[float | None] = mapped_column(Float, nullable=True)

    status: Mapped[str] = mapped_column(
        Enum("aguardando", "chamado", "atendido", "cancelado"),
        default="aguardando",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="queue_entries")
    specialist = relationship("Specialist", back_populates="queue_entries")