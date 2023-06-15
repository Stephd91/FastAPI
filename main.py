# 1) import FastAPI : a Python class that provides all the functionality for your API.
from fastapi import FastAPI

# 2) create a FastAPI "instance" : the app variable will be an "instance" of the class FastAPI. 
# This will be the main point of interaction to create all your API.
app = FastAPI()

# 3) create a path operation = endpoint = route
# "Path" here refers to the last part of the URL starting from the first /
# ex : In this URL https://example.com/items/foo the path is items/foo
# While building an API, the "path" is the main way to separate "concerns" and "resources".
#The @app.get("/") tells FastAPI that the function right below is in charge of handling requests that go to: the path "/" using a get operation
@app.get("/") # This path operation decorator tells FastAPI that the function below corresponds to the path "/"" with an operation get.
async def root():
    return {"message": "Hello World"}
print("test")
