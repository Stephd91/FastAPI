# 1) import FastAPI : a Python class that provides all the functionality for your API.
from fastapi import FastAPI
import model, schema #for constructing our tables in the database and the schemas
from config_sqlalchemy import engine, SessionLocal #for connection to our learn_de databse
from fastapi.templating import Jinja2Templates #for server-side rendering

# 2) Connect to database and create the database tables defined in our model.py file
model.Base.metadata.create_all(bind=engine)

# 3) create a FastAPI "instance" : the app variable will be an "instance" of the class FastAPI. 
# This will be the main point of interaction to create all your API.
# We also declare the templates to use for the server-side rendering with jinja
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 4) create path operations = endpoints = routes
# "Path" here refers to the last part of the URL starting from the first "/"
# ex : In this URL https://example.com/items/foo the path is items/foo
# While building an API, the "path" is the main way to separate "concerns" and "resources".
#The @app.get("/") tells FastAPI that the function right below is in charge of handling requests that go to: the path "/" using a get operation
@app.get("/") # This path operation decorator tells FastAPI that the function below corresponds to the path "/" with an operation get.
async def root(): # 4) define the path operation function
    test = input("What's your name ?")
    return {"message": "Hello, "+ test +" !"}

@app.get("/items/{item_number}") 
async def read_item(item_number : int): # Declare the type of a path parameter in the function using standard Python type annotations
    item_percent = item_number/100
    return {"item": item_percent}
