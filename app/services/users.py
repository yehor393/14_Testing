from fastapi import HTTPException
from app.models.users import UserDB
from app.repositories.user import UserRepo
from app.schemas.user import User
from random import randint
from app.dependencies.emails import send_email
from app.schemas.user import UserActivation


class UserServices():
    def __init__(self, db) -> None:
        """
        The __init__ function is called when the class is instantiated.
        It sets up the database connection and creates a UserRepo object to handle user data.
        
        :param self: Represent the instance of the class
        :param db: Pass the database connection to the userrepo class
        :return: None
        :doc-author: Trelent
        """
        self.repo = UserRepo(db=db)

    def create_new(self, user: User) -> User:
        """
        The create_new function creates a new user in the database.
            Args:
                self (UserRepo): The UserRepo object that is calling this function.
                user (User): A User object to be created in the database.
        
        :param self: Represent the instance of the class
        :param user: User: Pass the user object to the function
        :return: A new user
        :doc-author: Trelent
        """
        user.is_active = False
        user.otp = str(randint(100000, 999999))
        send_email("Welcome Dude,", f" your code is {user.otp}", user.username)
        new_user_from_db = self.repo.create(user)
        new_user = User.from_orm(new_user_from_db)
        return new_user

    def activate_user(self, data: UserActivation):
        """
        The activate_user function is used to activate a user.
            post:
              description: Activate a user by providing the OTP sent to their email address.
              requestBody:  # This is where you define the payload of your request body, if any. If there's no payload, omit this section entirely!
        
        :param self: Represent the instance of the class
        :param data: UserActivation: Pass the data to the function
        :return: The user object
        :doc-author: Trelent
        """
        user = self.get_by_username(data.Email)
        if data.otp == user.otp:
            user.is_active = True
            user = self.repo.update(user)
        return user

    def get_user_for_auth(self, username: str, password: str) -> User:
        """
        The get_user_for_auth function is used to authenticate a user.
        It takes in the username and password of the user, and returns a User object if authentication was successful.
        If authentication fails, it raises an HTTPException with status code 403.
        
        :param self: Represent the instance of a class
        :param username: str: Get the username from the request body,
        :param password: str: Check the password against the user's hashed password
        :return: A user object
        :doc-author: Trelent
        """
        user = self.repo.get_user_and_check_pass(username, password)
        if user is None:
            raise HTTPException(status_code=403)
        return User.from_orm(user)

    def get_by_username(self, username: str) -> User:
        """
        The get_by_username function takes in a username and returns the user object associated with that username.
        If no such user exists, it raises an HTTPException.
        
        :param self: Represent the instance of the class
        :param username: str: Specify the type of data that is expected to be passed into the function
        :return: A user object
        :doc-author: Trelent
        """
        user = self.repo.get_by_username(username)
        if user is None:
            raise HTTPException(status_code=403)
        return User.from_orm(user)

    def set_image(self, user: User, url: str) -> User:
        """
        The set_image function takes in a user and an image url.
        It then sets the user's image to the given url, updates it in the database,
        and returns a User object with all of its attributes.
        
        :param self: Represent the instance of a class
        :param user: User: Pass in the user object to be updated
        :param url: str: Set the image url for a user
        :return: A user object
        :doc-author: Trelent
        """
        user.image = url
        user_from_db = self.repo.update(user)
        return User.from_orm(user_from_db)
