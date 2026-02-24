from pydantic import BaseModel


class EspecialidadeCriar(BaseModel):
    nome: str


class EspecialidadeResposta(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True


class EspecialistaCriar(BaseModel):
    nome: str
    formacao: str | None = None
    registro: str | None = None
    bio: str | None = None
    especialidade_id: int | None = None


class EspecialistaAtualizar(BaseModel):
    nome: str | None = None
    formacao: str | None = None
    registro: str | None = None
    bio: str | None = None
    especialidade_id: int | None = None


class EspecialistaResposta(BaseModel):
    id: int
    nome: str
    formacao: str | None
    registro: str | None
    bio: str | None
    especialidade_id: int | None

    class Config:
        from_attributes = True