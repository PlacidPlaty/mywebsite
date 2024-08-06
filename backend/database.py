from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

''' configuration for connecting to and interacting with a SQLite database using SQLalchemy
Configure a SQLalchemy-based database interaction environment.
It defines a DATABASE_URL pointing to an SQLite database file, 
creates a database enginewith additional configuration for SQLite threat safety,
establishes a session factory with options to control transaction behaviour, 
and sets up a base class for declarative database models.
'''

DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(DATABASE_URL, connect_args = {"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush = False, bind = engine)
Base = declarative_base()