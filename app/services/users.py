from fastapi import HTTPException
from app.models.users import UserDB
from app.repositories.user import UserRepo
from app.schemas.user import User
from random import randint
from app.dependencies.emails import send_email

from app.schemas.user import UserActivation


class UserServices():
    def __init__(self, db) -> None:
        self.repo = UserRepo(db=db)

    def create_new(self, user: User) -> User:
        user.is_active = False
        user.otp = str(randint(100000, 999999))
        send_email("Welcome Dude,", f" your code is {user.otp}", user.username)
        new_user_from_db = self.repo.create(user)
        new_user = User.from_orm(new_user_from_db)
        return new_user

    def activate_user(self, data: UserActivation):
        user = self.get_by_username(data.Email)
        if data.otp == user.otp:
            user.is_active = True
            user = self.repo.update(user)
        return user

    def get_user_for_auth(self, username: str, password: str) -> User:
        user = self.repo.get_user_and_check_pass(username, password)
        if user is None:
            raise HTTPException(status_code=403)
        return User.from_orm(user)

    def get_by_username(self, username: str) -> User:
        user = self.repo.get_by_username(username)
        if user is None:
            raise HTTPException(status_code=403)
        return User.from_orm(user)

    def set_image(self, user: User, url: str) -> User:
        user.image = url
        user_from_db = self.repo.update(user)
        return User.from_orm(user_from_db)
