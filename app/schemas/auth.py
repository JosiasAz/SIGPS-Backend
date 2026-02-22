from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    senha: str = Field(min_length=6, max_length=72)
    perfil: str = "visualizador"


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str = Field(min_length=1, max_length=72)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: str