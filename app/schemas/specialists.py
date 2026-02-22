from pydantic import BaseModel


class SpecialtyCreate(BaseModel):
    nome: str


class SpecialtyResponse(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True


class SpecialistCreate(BaseModel):
    nome: str
    formacao: str | None = None
    registro: str | None = None
    bio: str | None = None
    especialidade_id: int | None = None


class SpecialistUpdate(BaseModel):
    nome: str | None = None
    formacao: str | None = None
    registro: str | None = None
    bio: str | None = None
    especialidade_id: int | None = None


class SpecialistResponse(BaseModel):
    id: int
    nome: str
    formacao: str | None
    registro: str | None
    bio: str | None
    especialidade_id: int | None

    class Config:
        from_attributes = True