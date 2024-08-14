from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils # imports models.py, schemas.py, utils.py etc...
from sqlalchemy.orm import Session
from ..database import engine, get_db

router = APIRouter(

    # saying that every URL in this python file starts with /users
    # now you can just replace the path with "/" instead of "/users" 
    # /users/{id} will look like /{id}
    prefix = "/users", # dont forget the comma
    # this tags your route operators for fastapi's documentation. 
    # Notice that it is a list, meaning you can add multple tags
    tags = ["Users"]
)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.UserOut)
def create_user(user : schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password using the hash function in utils.py 
    hashed_password = utils.hash(user.password)
    # update the password in the pydantic model 
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# find one user
@router.get("/{id}", response_model = schemas.UserOut)
def get_user(id : int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail = f"User with id: {id} does not exist")
    return user