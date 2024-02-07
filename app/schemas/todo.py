import datetime

from pydantic import BaseModel


class Todo(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: datetime.date
    additional_info: str
    class Config:
        orm_mode = True
        from_attributes = True


class TodoCreate(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: datetime.date
    additional_info: str | None


class TodoUpdate(BaseModel):
    id: int | None
    first_name: str | None
    last_name: str | None
    email: str | None
    phone_number: str | None
    birthday: datetime.date | None
    additional_info: str | None

