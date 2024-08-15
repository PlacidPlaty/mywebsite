from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    tags = ["Authentication"]
)

@router.post("/login", response_model= schemas.Token)
# use fastapi's OAuth2PasswordRequestForm
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), 
          db: Session = Depends(database.get_db)):
# OAuth2PasswordRequestForm stores the user's login input as "username" and "password"
# in this case the email is stored as a field called username in user_credential.
    # .first() gets the first instance of the user where email matches

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail = f"Invalid Credentials")
    
    # verify that the hashed password from the user and the one in the db are the same
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail = f"Invalid Credentials")
    
    # create a token. For the payload only add in user_id 
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    # return token
    return {"access_token": access_token, "token_type" : "bearer"}