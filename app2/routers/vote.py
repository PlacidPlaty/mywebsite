from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db
from .. import schemas, database, models, oauth2

router = APIRouter(
    prefix = "/vote",
    tags = ["Vote"]
)

@router.post("/", status_code= status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), 
         current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post: # if post not found
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id: {vote.post_id} does not exist")
        
    # check if the specific user has already liked the post
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, 
                                                models.Vote.user_id == current_user.id)
    # if the query found a post, means the user has already liked the post
    found_vote = vote_query.first()

    # if user provided a direction of 1, they want to vote on the post
    if (vote.dir == 1):
        # if the vote is found, found_vote == True
        if found_vote:
                raise HTTPException(status_code= status.HTTP_409_CONFLICT,
                                    detail = f"user {current_user.id} has already voted on post {vote.post_id}")
        
        # if vote not found, means user has not voted on post
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}
    # if the user provided a direction of 1, they want to delete an existing vote
    else:
        # if post_id is not found, found_vote == False. 
        if not found_vote:
             raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                                 detail = "Vote does not exist")
        # if vote was found
        vote_query.delete(synchronize_session = False)
        db.commit()

        return {"message": "Successfully deleted vote"}