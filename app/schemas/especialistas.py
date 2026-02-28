from pydantic import BaseModel
from typing import Optional

class EspecialidadeCriar(BaseModel):
    nome: str

class EspecialidadeResposta(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True

class EspecialistaCriar(BaseModel):
    nome: str
    formacao: Optional[str] = None
    registro: Optional[str] = None
    bio: Optional[str] = None
    localizacao: Optional[str] = None
    foto_url: Optional[str] = None
    modalidade: str = "presencial"
    especialidade_id: Optional[int] = None

class EspecialistaAtualizar(BaseModel):
    nome: Optional[str] = None
    formacao: Optional[str] = None
    registro: Optional[str] = None
    bio: Optional[str] = None
    localizacao: Optional[str] = None
    foto_url: Optional[str] = None
    modalidade: Optional[str] = None
    especialidade_id: Optional[int] = None

class EspecialistaResposta(BaseModel):
    id: int
    usuario_id: Optional[int]
    nome: str
    formacao: Optional[str]
    registro: Optional[str]
    bio: Optional[str]
    localizacao: Optional[str]
    foto_url: Optional[str]
    modalidade: str
    especialidade_id: Optional[int]

    class Config:
        from_attributes = True