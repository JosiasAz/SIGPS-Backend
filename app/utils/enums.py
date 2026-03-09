from enum import Enum

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    GESTOR = "GESTOR"
    PACIENTE = "PACIENTE"
    ESPECIALISTA = "ESPECIALISTA"

class SpecialistStatus(str, Enum):
    PENDENTE = "PENDENTE"
    ATIVO = "ATIVO"
    SUSPENSO = "SUSPENSO"
