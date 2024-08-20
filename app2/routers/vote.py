from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import engine, get_db

router = APIRouter(
    prefix = "/vote",
    tags = ["Vote"]
)

@router.post("/", status_code= status.HTTP_201_CREATED)
def vote():
    