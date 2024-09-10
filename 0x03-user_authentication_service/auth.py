#!/usr/bin/env python3
""" Authentication module """
from uuid import uuid4
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ returns an encrypted password """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """returns a stringified uuid"""
    return str(uuid4())


class Auth:
    """ Auth class to interact with the authentication database """

    def __init__(self):
        """ initialize an Auth instance """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ register a user """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user:
            raise ValueError(f"User {email} already exists")
        hashed_pwd = _hash_password(password)
        user = self._db.add_user(email, hashed_pwd)
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """validate a user's login details"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False
