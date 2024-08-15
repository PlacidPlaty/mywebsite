from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# create a schema with pydantic
# this class extends BaseModel and other classes will extend it
# this makes the schemas more flexible and reuseable
# handle user requests
class PostBase(BaseModel):
    title: str
    content: str
    # set default value to True even if not specified in json input
    published: bool = True

# handle creation and update of posts as they are fundamentally the same
# extend PostBase
class PostCreate(PostBase):
    # 'pass' makes PostCreate do the same thing as PostBase
    pass

# Handle sending data to user (response)
class Post(PostBase):
    # specify what you want to send back to the user
    # title, content and published are already inherited from PostBase
    created_at: datetime
# by default, pydantic can only read python dictionaries. 
# This can produce errors if you use it with ORMs like SQLalchemy
# writing the code below can make it accept non dictionary formats
    class Config:
        orm_mode = True

# handle creation of users
class UserCreate(BaseModel):
    email: EmailStr # Pydantic type that validates that a string is an email.
    password: str

# handle response to User based requests
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
# By default, pydantic can only read python dictionaries. 
# This can produce errors if you use it with ORMs like SQLalchemy writing the code below can make it accept non dictionary formats
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email : EmailStr
    password : str

# for returning of JWT Token to users
class Token(BaseModel):
    access_token : str
    token_type : str
# Data needed to create a token
class TokenData(BaseModel):
    id : Optional[str] = None
