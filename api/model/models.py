"""This module define all models (persistent objects - PO) of application. Each model
is a subclass of the Base class (base declarative) from app.model.database module.
The declarative extension in SQLAlchemy allows to define tables and models in one go,
that is in the same class.
"""

from datetime import datetime

from sqlalchemy import inspect
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from api.database import Base


class Model:
    """The Model class declare the serialize() method that is
    supposed to serializes the model data. The Model's subclasses
    can provide a implementation of this method."""

    def serialize(self) -> dict:
        """Serialize the object attributes values into a dictionary."""

        return {}

    def remove_session(self):
        """Removes an object from the session its current session."""

        session = inspect(self).session
        if session:
            session.expunge(self)


class User(Base, Model):
    """ User's model class.

    Column:
        id (integer, primary key)
        name (string, unique)
        email (string, unique)
        password (string)

    Attributes:
        name (str): User's name
        email (str): User's email
        password (str): User's password
    """

    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(36), nullable=False)
    username = Column(String(36), unique=True, nullable=False, index=True)
    email = Column(String(), unique=True, nullable=False)
    phone = Column(String(15), unique=True, nullable=True)
    password = Column(String(), nullable=False)
    verified_account = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    def __init__(self, name: str = None, username: str = None, email: str = None, phone: str = None,
                 password: str = '123456', verified_account: bool = False, active: bool = True,
                 created_at: datetime = datetime.now(), updated_at: datetime = datetime.now(),
                 deleted_at: datetime = datetime.now()) -> None:
        self.name = name
        self.username = username
        self.email = email
        self.phone = phone
        self.password = password
        self.verified_account = verified_account
        self.active = active
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def serialize(self) -> dict:
        data = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'username': self.username,
            'phone': self.phone,
            'verified_account': self.verified_account
        }

        return data

    def __repr__(self) -> str:
        return '<User %r>' % self.username


class Token(Base, Model):
    """ Token's model class.

    Column:
        id (integer, primary key)
        jti (string)
        token_type (string)
        user_identity (string)
        revoked (bool)
        expires (datetime)

    Attributes:
        jti (str): Unique identifier for the JWT
        token_type (str): Token type text
        user_identity (str): User ID text
        revoked (bool): Indicates when a token has been revoked
        expires (datetime): Expiration date
    """

    __tablename__ = 'tokens'

    id = Column(Integer, autoincrement=True, primary_key=True)
    jti = Column(String(36), nullable=False)
    token_type = Column(String(10), nullable=False)
    user_identity = Column(String(50), nullable=False)
    revoked = Column(Boolean, nullable=False)
    expires = Column(DateTime, nullable=False)

    def __init__(self, jti: str = None, token_type: str = None,
                 user_identity: str = None, revoked: bool = False,
                 expires: datetime = None) -> None:
        self.jti = jti
        self.token_type = token_type
        self.user_identity = user_identity
        self.revoked = revoked
        self.expires = expires

    def serialize(self) -> dict:
        data = {
            'id': self.id,
            'jti': self.jti,
            'token_type': self.token_type,
            'user_identity': self.user_identity,
            'revoked': self.revoked,
            'expires': self.expires
        }

        return data

    def __repr__(self) -> str:
        return '<Token %r>' % self.jti


class Category(Base, Model):
    """
    Category's model class.
    Column:
        id (integer, primary key)
        parent_id (integer)
        name (string)
        active (bool)
    Attributes:
        parent_id (integer): id of father
        name (string): Category's name
        active (bool): Define this category is active
    """

    __tablename__ = 'categories'

    id = Column(Integer, autoincrement=True, primary_key=True)
    parent_id = Column(Integer, nullable=True)
    name = Column(String(36), nullable=False)
    active = Column(Boolean, default=False)

    def __init__(self, parent_id: int = None, name: str = '', active: bool = False):
        self.parent_id = parent_id
        self.name = name
        self.active = active

    def serialize(self) -> dict:
        data = {
            'id': self.id,
            'parent_id': self.parent_id,
            'name': self.name,
            'active': self.active
        }

        return data

    def __repr__(self) -> str:
        return '<Category %r>' % self.name


class Product(Base, Model):
    """ Product's model class.

        Column:
            id (integer, primary key)
            name (string)

        Attributes:
            name (str): Product's name
        """

    __tablename__ = 'products'

    id = Column(Integer, autoincrement=True, primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'),  nullable=False)
    name = Column(String(36))
    description = Column(String(100), nullable=True)
    active = Column(Boolean, default=True)
    is_fractional = Column(Boolean, nullable=False)
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    def __init__(self, category_id: int = 757, name: str = None, description: str = None, active: bool = True,
                 is_fractional: bool = True, verified: bool = False, created_at: datetime = datetime.now(),
                 updated_at: datetime = datetime.now(), deleted_at: datetime = datetime.now()) -> None:
        self.category_id = category_id
        self.name = name
        self.description = description
        self.active = active
        self.is_fractional = is_fractional
        self.verified = verified
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def serialize(self) -> dict:
        data = {
            'id': self.id,
            'category_id': self.category_id,
            'name': self.name,
            'description': self.description,
            'is_fractional': self.is_fractional,
            'verified': self.verified,
        }

        return data

    def __repr__(self) -> str:
        return '<Product %r>' % self.name
