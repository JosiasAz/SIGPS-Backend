from datetime import datetime
from sqlalchemy import (
    String, Integer, DateTime, ForeignKey, UniqueConstraint, Text, Enum, Float
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.db import Base

PERFIS = ("admin", "gestor", "paciente", "visualizador")


class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = (UniqueConstraint("email", name="uq_usuarios_email"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    perfil: Mapped[str] = mapped_column(Enum(*PERFIS), nullable=False, default="visualizador")

    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    atualizado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Paciente(Base):
    __tablename__ = "pacientes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    telefone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Dados para ML
    idade: Mapped[int] = mapped_column(Integer, default=0)
    renda: Mapped[float] = mapped_column(Float, default=0.0)
    gastos: Mapped[float] = mapped_column(Float, default=0.0)

    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    agendamentos = relationship("Agendamento", back_populates="paciente")
    entradas_fila = relationship("EntradaFila", back_populates="paciente")


class Especialidade(Base):
    __tablename__ = "especialidades"
    __table_args__ = (UniqueConstraint("nome", name="uq_especialidades_nome"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)

    especialistas = relationship("Especialista", back_populates="especialidade")


class Especialista(Base):
    __tablename__ = "especialistas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    formacao: Mapped[str | None] = mapped_column(String(255), nullable=True)
    registro: Mapped[str | None] = mapped_column(String(120), nullable=True)  # CRM/CRP etc
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)

    especialidade_id: Mapped[int | None] = mapped_column(ForeignKey("especialidades.id"), nullable=True)
    especialidade = relationship("Especialidade", back_populates="especialistas")

    agendamentos = relationship("Agendamento", back_populates="especialista")
    entradas_fila = relationship("EntradaFila", back_populates="especialista")


class Agendamento(Base):
    __tablename__ = "agendamentos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("pacientes.id"), nullable=False)
    especialista_id: Mapped[int] = mapped_column(ForeignKey("especialistas.id"), nullable=False)

    inicio: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fim: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    status: Mapped[str] = mapped_column(
        Enum("agendado", "concluido", "cancelado"),
        default="agendado",
        nullable=False,
    )

    paciente = relationship("Paciente", back_populates="agendamentos")
    especialista = relationship("Especialista", back_populates="agendamentos")


class EntradaFila(Base):
    __tablename__ = "entradas_fila"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("pacientes.id"), nullable=False)
    especialista_id: Mapped[int | None] = mapped_column(ForeignKey("especialistas.id"), nullable=True)

    motivo: Mapped[str | None] = mapped_column(Text, nullable=True)
    prioridade: Mapped[int] = mapped_column(Integer, default=0)  # 0..100 (quanto maior, mais urgente)
    score_ml: Mapped[float | None] = mapped_column(Float, nullable=True)

    status: Mapped[str] = mapped_column(
        Enum("aguardando", "chamado", "atendido", "cancelado"),
        default="aguardando",
        nullable=False,
    )

    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    paciente = relationship("Paciente", back_populates="entradas_fila")
    especialista = relationship("Especialista", back_populates="entradas_fila")