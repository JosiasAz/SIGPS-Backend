from pydantic import BaseModel, EmailStr
from typing import Optional
from app.utils.enums import UserRole

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    role: UserRole

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str
    
    # Opcionais dependendo do role (pode ser ajustado)
    nome_completo: Optional[str] = None
    cpf: Optional[str] = None
    data_nascimento: Optional[str] = None
    telefone: Optional[str] = None

    # Específicos do Especialista
    registro_profissional: Optional[str] = None
    especialidade: Optional[str] = None
    modality: Optional[str] = None

# Properties to receive via API on update
class UserUpdate(BaseModel):
    password: Optional[str] = None
    is_active: Optional[bool] = None

class UserInDBBase(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

# Additional properties to return via API
class UserResponse(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str
