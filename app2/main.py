from fastapi import FastAPI

from . import models # imports models.py
from .database import engine
from .routers import user, post, auth, vote # imports user.py, post.py from router folder
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# get the routes from post and user in routers folder
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
