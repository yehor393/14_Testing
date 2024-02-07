import datetime
import jwt

from typing import Annotated
from fastapi import HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from dependencies.database import get_db, SessionLocal

from services.users import UserServices
from schemas.user import User, RolesEnum

# Маркери для авторизації та отримання даних користувача
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

secret_key = "secret_key"


class Token(BaseModel):
    access_token: str | bytes
    token_type: str = "bearer"


def create_access_token(username: str, role: str):
    token_data = {
        "sub": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    token = jwt.encode(token_data, secret_key, algorithm="HS256")

    return token


def decode_jwt_token(token):
    decoded_payload = jwt.decode(token, secret_key, algorithms=["HS256"])
    return decoded_payload


async def get_current_user(token: str = Depends(oauth2_scheme), db: SessionLocal = Depends(get_db)):
    token = decode_jwt_token(token)
    user_service = UserServices(db)
    username = token.get("sub")
    user = user_service.get_by_username(username)
    return user


async def check_is_default_user(user: User = Depends(get_current_user)) -> User:
    if user.role in [RolesEnum.USER, RolesEnum.MANAGER, RolesEnum.ADMIN] and user.is_active:
        return user
    raise HTTPException(status_code=403)


async def check_is_manager(user: User = Depends(get_current_user)) -> User:
    if user.role in [RolesEnum.MANAGER, RolesEnum.ADMIN] and user.is_active:
        return user
    raise HTTPException(status_code=403)


async def check_is_admin(user: User = Depends(get_current_user)) -> User:
    if user.role == RolesEnum.ADMIN and user.is_active:
        return user
    raise HTTPException(status_code=403)


DefaultUser = Annotated[User, Depends(check_is_default_user)]
AdminUser = Annotated[User, Depends(check_is_admin)]
Manager = Annotated[User, Depends(check_is_manager)]
