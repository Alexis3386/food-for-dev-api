"""
This module contains the necessary classes and functions for
interacting with the database.

It uses the SQLAlchemy library to create a database engine
and a session factory.

The [Base](cci:2:///home/alexis/food-for-dev/src/database.py:14:0-15:8) 
class is the base class for all SQLAlchemy models.

The `SessionLocal` is a session factory that creates a new session.

The `SQLALCHEMY_DATABASE_URL` is the URL of the database.

The `engine` is the SQLAlchemy database engine.

The `SessionLocal` is a session factory.

"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy models.
    """
