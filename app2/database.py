from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# for raw sql connection (not being used)
import time
import psycopg2
from psycopg2.extras import RealDictCursor # to include column names in your SQL query

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:rootuser@localhost/mywebsite"

# engine is responsible for SQLAlchemy to connect to postgres DB
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Session allows you to talk to database
SessionLocal = sessionmaker(autocommit=False, autoflush= False, bind=engine)

# Define a base class, all of the tables in postgres will be extending
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''
# For documentation purposes. In case I want to run raw SQL instead of SQLalchemy

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

'''
