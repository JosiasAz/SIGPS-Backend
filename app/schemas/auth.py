from pydantic import BaseModel, EmailStr, Field


class CadastroUsuario(BaseModel):
    email: EmailStr
    senha: str = Field(min_length=6, max_length=72)
    perfil: str = "visualizador"


class LoginUsuario(BaseModel):
    email: EmailStr
    senha: str = Field(min_length=1, max_length=72)


class RespostaLogin(BaseModel):
    token_acesso: str
    tipo_token: str = "bearer"
    expira_em: str