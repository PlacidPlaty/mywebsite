from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import List
import time
import psycopg2
from psycopg2.extras import RealDictCursor # to include column names in your SQL query
from sqlalchemy.orm import Session

from . import models, schemas, utils # imports models.py, schemas.py, utils.py etc...
from .database import engine, get_db
from .routers import user, post # imports user.py, post.py from router folder


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# get the routes from post and user in routers folder
app.include_router(post.router)
app.include_router(user.router)

# connections to database can fail so use a try statement
# cursor_factory= RealDictCursor give you the column name
while True: # keep trying to connect to the database until it passes
    try:
        connection = psycopg2.connect(host= 'localhost', database= 'mywebsite', user= 'postgres', 
                                    password= 'rootuser', cursor_factory= RealDictCursor)
        # use to execute SQL statements
        cursor = connection.cursor()
        print("Database connection was successful")
        break
    # store the error variable in error
    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        # sleep for 2 secs and try again 
        time.sleep(2) 


@app.get("/")
def read_root():
    return {"Hello": "World"}
