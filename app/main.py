# STEP 1
# import FastAPI : a Python class that provides all the functionality for your API.
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import (
    StaticFiles,
)  # for all front-end files like images, custom css, ...
from fastapi.templating import Jinja2Templates  # for server-side rendering

# Import for constructing our tables in the database and the schemas,
# and interacting with them via crud operations
import model, schema, crud
from config_sqlalchemy import (
    engine,
    SessionLocal,
)  # for connection to our learn_de database
from sqlalchemy.orm import Session

from pathlib import Path

# STEP 2
# Connect to database and create the database tables defined in our model.py file
# Normally you would probably initialize your database (create tables, etc) with Alembic
model.Base.metadata.create_all(bind=engine)

# STEP 3
# Create a FastAPI "instance" : the app variable will be an "instance" of the class FastAPI.
# This will be the main point of interaction to create all your API.
# We also declare the templates to use for the server-side rendering with jinja
app = FastAPI()
# Mount the "static" directory to serve static files
# app.mount("/static", StaticFiles(directory="static"), name="static")
# Define the path to the "static" folder
static_folder = Path(__file__).parent / "static"
# Mount the "static" folder to serve static files
app.mount("/static", StaticFiles(directory=static_folder), name="static")
templates = Jinja2Templates(directory="templates")


# To open a SQLAlchemy session for each request, we need a dependency to have for each request an independent database session/connection (SessionLocal)
# Our dependency will create a new SQLAlchemy SessionLocal that will be used in a single request, and then close it once the request is finished
# Then, a new session is created for the next request.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# STEP 4
# Create path operations = endpoints = routes
# "Path" here refers to the last part of the URL starting from the first "/"
# ex : In this URL https://example.com/items/foo the path is items/foo
# While building an API, the "path" is the main way to separate "concerns" and "resources".
# The @app.get("/") tells FastAPI that the function right below is in charge of handling requests that go to: the path "/" using a get operation
"""@app.get("/") # This path operation decorator tells FastAPI that the function below corresponds to the path "/" with an operation get.
async def root(): # Define the path operation function
    test = input("What's your name ?")
    return {"message": "Hello, "+ test +" !"}

@app.get("/items/{item_number}") 
async def read_item(item_number : int): # Declare the type of a path parameter in the function using standard Python type annotations
    item_percent = item_number/100
    return {"item": item_percent}"""


# APP HOMEPAGE
@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ANKI HOMEPAGE
# Afficher jusqu'à 8 cartes -- TEST OK
@app.get(
    "/cards/",
    response_model=list[schema.Card],
    response_class=HTMLResponse,
    name="cards",
)
def read_cards(
    request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    """_summary_

    Args:
        request (Request): _description_
        skip (int, optional): _description_. Defaults to 0.
        limit (int, optional): _description_. Defaults to 10.
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        _type_: _description_
    """
    cards = crud.get_cards(db, skip=skip, limit=limit)
    card_themes = [(card, card.theme_name) for card in cards]
    return templates.TemplateResponse(
        "app.html", {"request": request, "card_themes": card_themes}
    )


# Afficher les themes pour sélection par l'utilisateur lors d'une flash session -- TODOO !!!
@app.get("/themes", response_model=list[schema.Theme], response_class=HTMLResponse)

# Afficher une carte selon son ID -- TEST KO !!
@app.get("/cards_html/{id}", response_model=schema.Card, response_class=HTMLResponse)
async def read_cards_html(request: Request, id: int, db: Session = Depends(get_db)):
    # Catch the card by its ID given in the route
    card = db.query(model.Anki_cards).filter(model.Anki_cards.id == id).first()
    return templates.TemplateResponse(
        "app.html",
        {
            "request": request,
            "theme": card.theme_id,
            "question": card.question,
            "answer": card.answer,
        },
    )


@app.post("/launch-flash-session/")
def launch_flash_session(selected_themes: list = Form(schema.Theme)):
    # Here, you can perform the logic to handle the selected themes for the flash session
    # For example, you can process the selected themes and generate the flash session content.

    # Return a response or redirect to the appropriate page after processing the selected themes
    return {"message": "Flash session launched successfully!"}
