from pydantic import BaseModel

# define schema 
'''
A Pydantic's BaseModel named UserSchema is defined with 4 attributes, 
serving as a structured data schema for representing user information.
BaseModel offers data validation and parising of incoming data.
'''

class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    nickname: str