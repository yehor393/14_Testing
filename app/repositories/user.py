from fastapi import HTTPException
from app.models.users import UserDB
import hashlib
import os


class UserRepo():
    def __init__(self, db) -> None:
        self.db = db

    def create(self, user):
        """
        The create function creates a new user in the database.
            It takes a User object as an argument and returns the newly created user.
            
        
        :param self: Represent the instance of the class
        :param user: Create a new user
        :return: A new user object
        :doc-author: Trelent
        """
        password, salt = self.hash_password(user.password)
        new_user = UserDB(**user.dict())
        new_user.password = password
        new_user.salt = salt
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def update(self, user):
        """
        The update function is used to update a user's information in the database.
        It takes in a User object and updates the corresponding entry in the database.
        
        
        :param self: Represent the instance of the class
        :param user: Update the user in the database
        :return: The create function, which returns the user
        :doc-author: Trelent
        """
        self.db.query(UserDB).filter(UserDB.username == user.username).delete()
        return self.create(user)

    def get_by_username(self, username):
        """
        The get_by_username function is used to retrieve a user from the database by their username.
            
        
        :param self: Represent the instance of the class
        :param username: Filter the query to find a user with that username
        :return: The first result of the query
        :doc-author: Trelent
        """
        return self.db.query(UserDB).filter(UserDB.username == username).first()

    def get_user_and_check_pass(self, username, password):
        """
        The get_user_and_check_pass function takes in a username and password,
            hashes the password with the salt from the database, and compares it to
            what is stored in the database. If they match, then we return that user.
        
        
        :param self: Represent the instance of the class
        :param username: Query the database for a user with that username
        :param password: Check if the password entered by the user is correct
        :return: A user object if the username and password match
        :doc-author: Trelent
        """
        user = self.db.query(UserDB).filter(UserDB.username == username).first()
        password_from_db = user.password
        user_salt = user.salt
        hashed_pass, _ = self.hash_password(password=password, salt=user_salt)
        if hashed_pass == password_from_db:
            return user
        else:
            return None

    def generate_salt(self):
        """
        The generate_salt function generates a random string of characters to be used as the salt for hashing passwords.
        The function uses the os module's urandom function to generate a 16 byte string, which is then converted into hexadecimal format and returned.
        
        :param self: Represent the instance of the class
        :return: A random string of 16 bytes
        :doc-author: Trelent
        """
        return os.urandom(16)

    def hash_password(self, password, salt=None) -> tuple[str]:
        """
        The hash_password function takes a password and an optional salt as input.
        If no salt is provided, it generates one using the generate_salt function.
        It then concatenates the password with the salt and hashes them together using SHA256.
        The hashed password is returned along with its corresponding hex-encoded salt.
        
        :param self: Refer to the current instance of a class
        :param password: Get the password from the user
        :param salt: Generate a random salt
        :return: A tuple of the hashed password and salt
        :doc-author: Trelent
        """
        if salt is None:
            salt = self.generate_salt()
        else:
            salt = bytes.fromhex(salt)
        salted_password = password.encode() + salt
        hashed_password = hashlib.sha256(salted_password).hexdigest()
        return str(hashed_password), str(salt.hex())
