from sqlalchemy import Column, String, Date
from .base import BaseModel


class TodoDB(BaseModel):
    __tablename__: str = "todos"

    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    birthday = Column(Date)
    additional_info = Column(String, nullable=True)
