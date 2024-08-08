from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# create a schema with pydantic
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
# returns a HTTP 201 when successful
@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_posts(post : Post): # reference the Post pydantic model
    return {"new_posts": post}

# retrieve one individual post
@app.get("/posts/{id}")
def get_post(id : int, response: Response): 
# id : int validates if input can be converted into int, then auto converts into int
    print(id)
    post = find_post(id) # find_post is not implemented. take it that it is a function to find a post based on the given id
    # if post of given id is not found
    if not post:
        raise HTTPException(status_code= status.HTTP_404_BAD_REQUEST, 
                            detail= f"post with id: {id} was not found")
    return  {"post_detail": post}


# Status code of 204 indicate that a HTTP request has been successfully completed, 
# and there is no message body
@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post():
    # find the index in the array that has required ID
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id: {id} does not exist")
    # remove the post from the array my_posts
    my_posts.pop(index)
    return Response(status_code= status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id : int, post: Post):
    # find the index in the array that has required ID
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id: {id} does not exist")
    
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}