from sqlalchemy import Column, Integer, String
from database import Base

# model the database tables
# create a table called users with id as the pri key
class User(Base):
    __tablename__ = "users"

    id= Column(Integer , primary_key = True, index = True)
    name = Column(String)
    email = Column(String)
    nickname = Column(String)