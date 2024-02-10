from datetime import datetime, timedelta
from sqlalchemy import and_, extract
from fastapi import HTTPException
from models.todo import TodoDB


class TodoRepo():
    def __init__(self, db) -> None:
        self.db = db

    def get_all(self) -> list[TodoDB]:
        return self.db.query(TodoDB).filter()

    def create(self, todo_item):
        new_item = TodoDB(**todo_item.dict())
        self.db.add(new_item)
        self.db.commit()
        self.db.refresh(new_item)
        return new_item

    def get_by_id(self, id: int):
        return self.db.query(TodoDB).filter(TodoDB.id == id).first()

    def update(self, id: int, todo_update_data):
        todo_item = self.db.query(TodoDB).filter(TodoDB.id == id).first()
        if not todo_item:
            raise None
        for key, value in todo_update_data.dict().items():
            setattr(todo_item, key, value)
        self.db.commit()
        self.db.refresh(todo_item)
        return todo_item

    def delete(self, id: int):
        todo_item = self.db.query(TodoDB).filter(TodoDB.id == id).first()
        if not todo_item:
            raise None
        self.db.delete(todo_item)
        self.db.commit()
        return True

    def search_contacts(self, first_name, last_name, email):
        query = self.db.query(TodoDB)
        if first_name:
            query = query.filter(TodoDB.first_name.contains(first_name))
        if last_name:
            query = query.filter(TodoDB.last_name.contains(last_name))
        if email:
            query = query.filter(TodoDB.email.contains(email))
        return query.all()

    def get_upcoming_birthdays(self):
        today = datetime.today()
        dates = [(today + timedelta(days=i)).date() for i in range(7)]

        return self.db.query(TodoDB).filter(
            and_(
                extract('month', TodoDB.birthday).in_([date.month for date in dates]),
                extract('day', TodoDB.birthday).in_([date.day for date in dates])
            )
        ).all()
