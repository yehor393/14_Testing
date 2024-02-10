import datetime
import jwt

from typing import Annotated
from fastapi import HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from app.dependencies.database import get_db, SessionLocal

from app.services.users import UserServices
from app.schemas.user import User, RolesEnum

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

secret_key = "secret_key"


class Token(BaseModel):
    access_token: str | bytes
    token_type: str = "bearer"


def create_access_token(username: str, role: str):
    """
    The create_access_token function creates a JWT token for the user.
        The token is created with the following data:
            - sub (subject): username of the user, which is used to identify them in our database.
            - role: role of the user, which determines what they can do on our website.
            - exp (expiration time): expiration time of 1 day from now.
    
    :param username: str: Specify the username of the user that is logging in
    :param role: str: Specify the role of the user
    :return: A token
    :doc-author: Trelent
    """
    token_data = {
        "sub": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    token = jwt.encode(token_data, secret_key, algorithm="HS256")

    return token


def decode_jwt_token(token):
    """
    The decode_jwt_token function takes a token as an argument and decodes it using the jwt.decode function.
    The decode_jwt_token function returns the decoded payload.
    
    :param token: Decode the token
    :return: The decoded payload from the token
    :doc-author: Trelent
    """
    decoded_payload = jwt.decode(token, secret_key, algorithms=["HS256"])
    return decoded_payload


async def get_current_user(token: str = Depends(oauth2_scheme), db: SessionLocal = Depends(get_db)):
    """
    The get_current_user function is a dependency that can be injected into any endpoint.
    It will decode the JWT token and return the user object if it exists.
    
    :param token: str: Get the token from the request header
    :param db: SessionLocal: Pass the database session to the function
    :return: The user object
    :doc-author: Trelent
    """
    token = decode_jwt_token(token)
    user_service = UserServices(db)
    username = token.get("sub")
    user = user_service.get_by_username(username)
    return user


async def check_is_default_user(user: User = Depends(get_current_user)) -> User:
    """
    The check_is_default_user function is a dependency that can be used to check if the user has the role of USER, MANAGER or ADMIN.
    It also checks if the user is active. If both conditions are met, it returns the current user object.
    
    :param user: User: Get the user object from the database
    :return: A user object if the role is user, manager or admin and if the user is active
    :doc-author: Trelent
    """
    if user.role in [RolesEnum.USER, RolesEnum.MANAGER, RolesEnum.ADMIN] and user.is_active:
        return user
    raise HTTPException(status_code=403)


async def check_is_manager(user: User = Depends(get_current_user)) -> User:
    """
    The check_is_manager function is a dependency that checks if the user has the role of manager or admin.
    If they do, then it returns their User object. If not, it raises an HTTPException with status code 403.
    
    :param user: User: Pass the user object to the function
    :return: A user object if the user is a manager or admin and has an active account
    :doc-author: Trelent
    """
    if user.role in [RolesEnum.MANAGER, RolesEnum.ADMIN] and user.is_active:
        return user
    raise HTTPException(status_code=403)


async def check_is_admin(user: User = Depends(get_current_user)) -> User:
    """
    The check_is_admin function is a dependency that can be used to check if the user has admin privileges.
    It will raise an HTTPException with status code 403 (Forbidden) if the user does not have admin privileges.
    
    :param user: User: Get the user from the database
    :return: The user object if the role is admin and the user is active
    :doc-author: Trelent
    """
    if user.role == RolesEnum.ADMIN and user.is_active:
        return user
    raise HTTPException(status_code=403)


DefaultUser = Annotated[User, Depends(check_is_default_user)]
AdminUser = Annotated[User, Depends(check_is_admin)]
Manager = Annotated[User, Depends(check_is_manager)]
