from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils # imports models.py, schemas.py, utils.py etc...
from sqlalchemy.orm import Session
from ..database import engine, get_db

router = APIRouter()

@router.post("/users", status_code = status.HTTP_201_CREATED, response_model = schemas.UserOut)
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
@router.get("/users/{id}", response_model = schemas.UserOut)
def get_user(id : int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail = f"User with id: {id} does not exist")
    return user