from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas # imports models.py, schemas.py, utils.py etc...
from sqlalchemy.orm import Session
from typing import List
from ..database import engine, get_db

router = APIRouter()

# the response is expecting specific columns but the db.query is returning all columns.
# changing it to List[] helps make them compatible. 
@router.get("/posts", response_model= List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

'''
data type for a post-> title: str, content str
returns a HTTP 201 when successful 
and response_model sends back data to the user based on the schema you specify.
response_model allows you to restrict the data you are sending back to the user.
'''
@router.post("/posts", status_code= status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db)): # reference the Post pydantic model

# pass the data from post (argument) into new_post. Below is an ineffective way to get the input.
    # new_post = models.Post(title= post.title, content = post.content, published = post.published)

# instead use python dictionary and unpack it with '**'. Below code does the same thing as above
    new_post = models.Post(**post.model_dump()) # convert post to a dictionary and unpack it with **
    db.add(new_post) # add new post to database
    db.commit() # commit to database
    db.refresh(new_post) # retreive the new_post. (Eqivalent to getting the output from SQL RETURNING keyword)

    return new_post

# retrieve one individual post
@router.get("/posts/{id}", response_model = schemas.Post)
def get_post(id : int, db: Session = Depends(get_db)): 
    # id : int validates if input can be converted into int, then auto converts into int
    # After data validation, pass the data from id into %s. Need to type cast into string first
                    # filter is like running the WHERE keyword in SQL
                    # .first() finds the first instance of the data and returns it
    post = db.query(models.Post).filter(models.Post.id == id).first()

    # If database did not find a post, post will be set to None
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id: {id} was not found")
    return post


# Status code of 204 indicate that a HTTP request has been successfully completed, 
# and there is no message body
@router.delete("/posts/{id}")
def delete_post(id : int, db: Session = Depends(get_db)):
    # similar to getting one post
    post = db.query(models.Post).filter(models.Post.id == id)

    # If post is not found
    if post.first() == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id: {id} does not exist")
    # If post is found, delete it
    post.delete(synchronize_session = False)
    db.commit()

    return Response(status_code= status.HTTP_204_NO_CONTENT)

@router.put("/posts/{id}", response_model= schemas.Post)
def update_post(id : int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # query to find the specific post
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # grab the post if it exists
    post = post_query.first()

    # If post id is not found
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id: {id} does not exist")
    
    # If post exists
    post_query.update(updated_post.model_dump(), synchronize_session = False)
    # commit to the database
    db.commit()
    # send the updated info to the user
    return post_query.first()