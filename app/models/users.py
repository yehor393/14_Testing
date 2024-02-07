from sqlalchemy import Column, String, Boolean
from .base import BaseModel


class UserDB(BaseModel):
    __tablename__: str = "users"
    username = Column(String)
    password = Column(String)
    role = Column(String)
    salt = Column(String)
    is_active = Column(Boolean)
    otp = Column(String)
    image = Column(String)

