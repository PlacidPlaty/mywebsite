from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

# tokenUrl is the API path used in auth.py
oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "/login")

"""
To create JWT tokens
Need to provide SECRET_KEY, Algorithm, Expiration time
It is not a good idea to store your SECRET_KEY in your code
"""

SECRET_KEY = "cfe042b7e3ba319a6cc0e6126ecc8c509f557b5b0fa648a18348d346443a7758"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    # create a copy of the data so that you can manipulate it further.
    to_encode = data.copy()
    print("something")

    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    # update the payload with expiry timing
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

    return encoded_jwt

# To verify if a token is real
# credentials_exception is used if JWT token is incorrect
# Raise except if there are errors with the Token, return the Token's data if no errors
def verify_access_token(token : str, credentials_exception):

    try:
                                # Expects a list in the algorithms
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        # check the type of token created in auth.py to see which payload you can get
        # in this case you can extract the id from the payload
        id : str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credentials_exception
    
    return token_data
    
# able to protect certain API paths by checking for user's credentials.
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                                          detail = f"Could not validate credentials",
                                          headers = {"WWW-Authenticate": "Bearer"})
    
    # verfiy the token is valid and extract the user details from the database
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user