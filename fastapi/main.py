from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# class extends BaseModel
class Post(BaseModel):
    title: str
    content: str
    # set default value to True even if not specified in json input
    published: bool = True
    # Optional field that defaults to None
    rating: Optional[int] = None

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}

# data type for a post-> title: str, content str
@app.post("/createposts")
def create_posts(post : Post): # reference the Post pydantic model
    return {"new_posts": post}