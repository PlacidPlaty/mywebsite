from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime
from typing import Optional
from pydantic.types import conint #to validate int is within a certain range

####################################################

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

####################################################

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

# Handle sending data to user (response). Extend PostBase
class Post(PostBase):
    # specify what you want to send back to the user
    # title, content and published are already inherited from PostBase
    created_at: datetime
    owner_id: int
    owner: UserOut # Return the owner type as specified in models.py's Post
# by default, pydantic can only read python dictionaries. 
# This can produce errors if you use it with ORMs like SQLalchemy
# writing the code below can make it accept non dictionary formats
    class Config:
        orm_mode = True

# to deal with the left outer join query in get_post
class PostOut(BaseModel):
    Post: Post # Set it to return the Post schema
    votes: int

    class Config:
        orm_mode = True

####################################################

# for returning of JWT Token to users
class Token(BaseModel):
    access_token : str
    token_type : str
# Data needed to create a token
class TokenData(BaseModel):
    '''
    newer version of pydantic does not allow parsing of int to str
    since id is an int while below id is declared as str, 
    an error will occur when trying trying to authenticate with JWT token
    model_config = ConfigDict(coerce_numbers_to_str=True) helps with the issue
    '''
    model_config = ConfigDict(coerce_numbers_to_str=True)

    id : Optional[str] = None


# For vote
class Vote(BaseModel):
    post_id: int
    # either 0 or 1. 1 likes the post, 0 is no vote
    dir: int = Field(ge=0, le = 1) # try using Field first as conint gets an error
    # dir: conint(le=1) # shown in video but gives an error