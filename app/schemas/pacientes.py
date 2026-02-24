from pydantic import BaseModel, EmailStr


class PacienteCriar(BaseModel):
    nome: str
    email: EmailStr | None = None
    telefone: str | None = None
    observacoes: str | None = None
    idade: int = 0
    renda: float = 0.0
    gastos: float = 0.0


class PacienteAtualizar(BaseModel):
    nome: str | None = None
    email: EmailStr | None = None
    telefone: str | None = None
    observacoes: str | None = None
    idade: int | None = None
    renda: float | None = None
    gastos: float | None = None


class PacienteResposta(BaseModel):
    id: int
    nome: str
    email: EmailStr | None
    telefone: str | None
    observacoes: str | None
    idade: int
    renda: float
    gastos: float

    class Config:
        from_attributes = True