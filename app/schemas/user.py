from pydantic import BaseModel, EmailStr
import enum


class Email(BaseModel):
    email: EmailStr


class RolesEnum(str, enum.Enum):
    USER = "user"
    MANAGER = "manager"
    ADMIN = "ADMIN"


class User(BaseModel):
    username: EmailStr
    password: str
    role: RolesEnum
    is_active: bool | None
    otp: str | None
    image: str

    class Config:
        orm_mode = True
        from_attributes = True


class UserActivation(BaseModel):
    Email: EmailStr
    otp: str
