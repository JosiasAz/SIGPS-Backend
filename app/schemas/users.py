from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    perfil: str

    class Config:
        from_attributes = True