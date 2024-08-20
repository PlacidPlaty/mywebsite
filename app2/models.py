from .database import Base # get Base from database.py
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

# every model represents a table in the database

# Post model extends Base
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default = 'TRUE', nullable = False)
    # Takes the time at which the data is created. text('now()') is what you would type in postgres's default field
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default=text('now()'))
# Set up One to Many relationship with user
# Reference the tablename NOT the class name. on delete is set to cascade. The foreignkey will be set to not nullable
    owner_id = Column(Integer, ForeignKey("users.id", ondelete= "CASCADE"), nullable = False)
# Set up to return a owner property when you retrieve a post. Fetch the user based on the owner_id and return it!
# Reference the class NOT the table name.
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable = False, unique = True) # All emails are unique to prevent multiple accounts with the same email
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default=text('now()')) 


# Table to track use vote for each post
class Vote(Base):
    __tablename__ = "votes"
    # for foreign key reference the table name and NOT the class name
    user_id = Column(Integer, ForeignKey("users.id", ondelete= "CASCADE"), primary_key = True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete= "CASCADE"), primary_key = True)