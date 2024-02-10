from typing import Optional
from fastapi import APIRouter, Depends
from schemas.todo import Todo, TodoCreate, TodoUpdate
from schemas.user import User
from dependencies.database import get_db, SessionLocal
from services.todos import TodoServices
from dependencies.auth import check_is_admin, check_is_manager, check_is_default_user


router = APIRouter()


@router.get("/")
async def list_todos(user: User = Depends(check_is_default_user), db: SessionLocal = Depends(get_db)) -> list[Todo]:
    todo_items = TodoServices(db=db).get_all_todos()
    return todo_items


@router.get("/{id}")
async def get_detail(id: int, user: User = Depends(check_is_default_user), db: SessionLocal = Depends(get_db)) -> Todo:
    todo_item = TodoServices(db=db).get_by_id(id)
    return todo_item


@router.get("/contacts/search")
async def search_contacts(
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None,
    db: SessionLocal = Depends(get_db)
) -> list[Todo]:
    return TodoServices(db=db).search_contacts(first_name, last_name, email)


@router.get("/contacts/upcoming_birthdays")
async def get_upcoming_birthdays(db: SessionLocal = Depends(get_db)):
    todo_item = TodoServices(db=db).get_upcoming_birthdays()
    return todo_item


@router.post("/")
async def create_todo(todo_item: TodoCreate, admin: User = Depends(check_is_admin), db: SessionLocal = Depends(get_db)) -> TodoCreate:
    new_item = TodoServices(db=db).create_new(todo_item)
    return new_item


@router.put("/{id}")
async def update_todo(id: int, todo_item: TodoUpdate, db: SessionLocal = Depends(get_db)) -> TodoUpdate:
    new_item = TodoServices(db=db).update(id, todo_item)
    return new_item


@router.delete("/{id}")
async def delete_todo(id: int, db: SessionLocal = Depends(get_db)) -> bool:
    TodoServices(db=db).delete(id)
    return True


