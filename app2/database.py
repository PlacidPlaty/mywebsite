from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:rootuser@localhost/mywebsite"

# engine is responsible for SQLAlchemy to connect to postgres DB
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Session allows you to talk to database
SessionLocal = sessionmaker(autocommit=False, autoflush= False, bind=engine)

# Define a base class, all of the tables in postgres will be extending
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()