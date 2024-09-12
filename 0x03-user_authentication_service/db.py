#!/usr/bin/env python3
"""DB module"""
from typing import Dict
from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base
from user import User


class DB():
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Create a user and save to database"""
        try:
            user = User(email=email, hashed_password=hashed_password)
            sesh = self._session
            sesh.add(user)
            sesh.commit()
        except Exception:
            sesh.rollback()
            user = None
        return user

    def find_user_by(self, **kwargs) -> User:
        """Finds a user in the database using a given keyword arg(s)"""
        fields = []
        values = []
        for k, v in kwargs.items():
            if hasattr(User, k):
                fields.append(getattr(User, k))
                values.append(v)
            else:
                raise InvalidRequestError()
        sesh = self._session
        user = sesh.query(User).filter(
            tuple_(*fields).in_([tuple(values)])).first()
        if not user:
            raise NoResultFound()
        return user

    def update_user(self, user_id, **kwargs):
        """Updates a user's details in the database"""
        user = self.find_user_by(id=user_id)
        if not user:
            return

        valid_attrs = {}
        for k, v in kwargs.items():
            if hasattr(User, k):
                valid_attrs[k] = v
            else:
                raise ValueError()

        sesh = self._session
        query = sesh.query(User).filter(User.id == user_id)
        query.update(valid_attrs)

        sesh.commit()
