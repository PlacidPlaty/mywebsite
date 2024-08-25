from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # for CORS

from . import models # imports models.py
from .database import engine
from .routers import user, post, auth, vote # imports user.py, post.py from router folder
from .config import settings

# this line is kept for documentation
# used by SQLalchemy but since alembic is used now, it is not needed.
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# get the routes from post and user in routers folder
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# create a list of urls that your application can talk to
# if you want any url to be able to talk to your application. use the wildcard '*'
# origins = ["*"]
origins = ["https://www.google.com"]
# middleware is a function that runs before every request.
# it is used by web frameworks
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

