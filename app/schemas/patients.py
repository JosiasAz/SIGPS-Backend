from pydantic import BaseModel, EmailStr


class PatientCreate(BaseModel):
    nome: str
    email: EmailStr | None = None
    telefone: str | None = None
    observacoes: str | None = None


class PatientUpdate(BaseModel):
    nome: str | None = None
    email: EmailStr | None = None
    telefone: str | None = None
    observacoes: str | None = None


class PatientResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr | None
    telefone: str | None
    observacoes: str | None

    class Config:
        from_attributes = True