from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2 # imports models.py, schemas.py, utils.py etc...
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from ..database import engine, get_db

router = APIRouter(
    # saying that every URL in this python file starts with /post
    # now you can just replace the path with "/" instead of "/post"
    # /post/{id} will look like /{id}
    prefix = "/posts", # dont forget the comma
    # this tags your route operators for fastapi's documentation. 
    # Notice that it is a list, meaning you can add multple tags
    tags = ["Posts"]
)

# the response is expecting specific columns but the db.query is returning all columns.
# changing it to List[] helps make them compatible. 
# limit allows users to limit how many posts to return while skip allows users to skip over however many posts
# Default number for limit and skip can be set in function parameter
# Search parameter is optional. Keyword does not have to exactly match the post title.
# eg in the url: /posts&limit=3&skip=2
# eg in the url: /post&search=guide%20tours   "%20" is space in HEXA ASCII
@router.get("/", response_model= List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit : int = 10, skip : int = 0, search: Optional[str] = ""):
    
    # keep here for documentation
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

#query the database for posts and include votes from users
    # by default, SQLalchemy does inner join. isouter = True changes it to outer join
    # label changes the column name
    # copy the .filter() stuff over from post = db.query(models.Post).....
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, 
                                         isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(results)
    return posts

'''
data type for a post-> title: str, content str
Response_model sends back data to the user based on the schema you specify.
response_model allows you to restrict the data you are sending back to the user.
oauth2.get_current_user checks that user have the correct JWT token and credential to access the API endpoint
at the same time Depends(oauth2.get_current_user) also returns the user stated in the JWT token.
'''
@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)): 

# pass the data from post (argument) into new_post. Below is an ineffective way to get the input.
    # new_post = models.Post(title= post.title, content = post.content, published = post.published)

# instead use python dictionary and unpack it with '**'. Below code does the same thing as above
    new_post = models.Post(owner_id = current_user.id, # add owner_id to the new_post
                           **post.model_dump()) # convert post to a dictionary and unpack it with **
    db.add(new_post) # add new post to database
    db.commit() # commit to database
    db.refresh(new_post) # retreive the new_post. (Eqivalent to getting the output from SQL RETURNING keyword)

    print(current_user.email)
    return new_post

# retrieve one individual post
@router.get("/{id}", response_model = schemas.PostOut)
def get_post(id : int, db: Session = Depends(get_db)): 
    # id : int validates if input can be converted into int, then auto converts into int
    # After data validation, pass the data from id into %s. Need to type cast into string first
                    # filter is like running the WHERE keyword in SQL
                    # .first() finds the first instance of the data and returns it
    # post = db.query(models.Post).filter(models.Post.id == id).first()

# query the database for the specific post and the votes for it
    post = results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, 
                                         isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()

    # If database did not find a post, post will be set to None
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id: {id} was not found")
    return post


# Status code of 204 indicate that a HTTP request has been successfully completed, 
# and there is no message body
@router.delete("/{id}")
def delete_post(id : int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # similar to getting one post. Query for the post
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # get the post from the query
    post = post_query.first()

    # If post is not found
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id: {id} does not exist")
    # If user tries to delete posts that are not theirs by checking from current_user = Depends(oauth2.get_current_user)
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail = f"Not authorised to perform requested action")
    # If post is found, delete it
    post_query.delete(synchronize_session = False)
    db.commit()

    return Response(status_code= status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model= schemas.Post)
def update_post(id : int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # query to find the specific post
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # grab the post from the query
    post = post_query.first()

    # If post id is not found
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id: {id} does not exist")
    
    # If user tries to update posts that are not theirs by checking from current_user = Depends(oauth2.get_current_user)
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail = f"Not authorised to perform requested action")
    
    # If post exists
    post_query.update(updated_post.model_dump(), synchronize_session = False)
    # commit to the database
    db.commit()
    # send the updated info to the user
    return post_query.first()