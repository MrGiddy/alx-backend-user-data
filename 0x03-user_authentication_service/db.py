"""DB module"""
from sqlalchemy import create_engine
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
        self._engine = create_engine("sqlite:///a.db", echo=True)
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

    def add_user(self, email, hashed_password):
        """Create a user and save to database"""
        user = User(email=email, hashed_password=hashed_password)

        sesh = self._session
        sesh.add(user)
        sesh.commit()

        sesh.refresh(user)
        return user

    def find_user_by(self, **kwargs):
        """Finds a user in the database using a given keyword arg(s)"""
        valid_attrs = {}
        for k, v in kwargs.items():
            if hasattr(User, k):
                valid_attrs[k] = v
            else:
                raise InvalidRequestError

        sesh = self._session
        user = sesh.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound
        return user
