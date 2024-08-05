from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(DATABASE_URL, connect_args = {"check_same_threat": False})
SessionLocal = sessionmaker(autocommit=False, autoflush = False, bind = engine)
Base = declarative_base()