# STEP 1
# import FastAPI : a Python class that provides all the functionality for your API.
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import (
    StaticFiles,
)  # for all front-end files like images, custom css, ...
from fastapi.templating import Jinja2Templates  # for server-side rendering

# Import for constructing our tables in the database and the schemas,
# and interacting with them via crud operations
import model
import schema
import crud
from config_sqlalchemy import (
    engine,
    SessionLocal,
)  # for connection to our learn_de database
from sqlalchemy.orm import Session

"""# For data quality checking
import great_expectations as gx
data_context = gx.get_context()"""

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
# APP HOMEPAGE endpoint
@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ANKI HOMEPAGE endpoint "/app"
# Afficher les cartes + les thèmes distincts -- TEST OK
@app.get(
    "/app/",
    response_model=list[schema.CardWithTheme],
    response_class=HTMLResponse,
    name="app",
)
def read_cards_themes(
    request: Request,
    skip: int = 0,
    card_limit: int = 1001,
    theme_limit: int = 10,
    db: Session = Depends(get_db),
):
    """_summary_

    Args:
        request (Request): _description_
        skip (int, optional): _description_. Defaults to 0.
        card_limit (int, optional): _description_. Defaults to 10.
        theme_limit (int, optional): _description_. Defaults to 10.
        db (Session, optional): sqlalchemy session

    Returns:
        _type_: _description_
    """
    # Fetch the list of cards
    cards = crud.get_cards(db, skip=skip, limit=card_limit)
    card_with_themes = [(card, card.theme_name) for card in cards]

    # Fetch the list of themes
    themes = crud.get_themes(db, limit=theme_limit)
    print(themes[0].id)
    # Fetch the list of distinct themes
    themes_names = crud.get_themes_names(db, limit=theme_limit)
    # context
    context = {
        "request": request,
        "card_with_themes": card_with_themes,
        "themes": themes,
        "themes_names": themes_names,
    }

    return templates.TemplateResponse("app.html", context)


# Afficher jusqu'à 10 cartes -- TEST OK
@app.get(
    "/cards/",
    response_model=list[schema.Card],
    response_class=HTMLResponse,
    name="cards",
)
def read_cards(
    request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    cards = crud.get_cards(db, skip=skip, limit=limit)
    card_themes = [(card, card.theme_name) for card in cards]
    print(card_themes[0][1].theme)
    return templates.TemplateResponse(
        "app.html", {"request": request, "card_themes": card_themes}
    )


# Afficher les thèmes à selectionner pour la flash session -- TEST OK
# @app.get(
#     "/themes",
#     response_model=list[schema.Theme],
#     response_class=HTMLResponse,
#     name="themes",
# )
# def read_distinct_themes(
#     request: Request, limit: int = 10, db: Session = Depends(get_db)
# ):
#     distinct_themes = crud.get_distinct_themes(db, limit=limit)
#     return templates.TemplateResponse(
#         "app.html", {"request": request, "distinct_themes": distinct_themes}
#     )


# Afficher une carte selon son ID
# @app.get("/cards/{id}", response_model=schema.Card, response_class=HTMLResponse)
# async def read_cards_html(request: Request, id: int, db: Session = Depends(get_db)):
#     # Catch the card by its ID given in the route
#     card = db.query(model.Anki_cards).filter(model.Anki_cards.id == id).first()
#     return templates.TemplateResponse(
#         "app.html",
#         {
#             "request": request,
#             "theme": card.theme_id,
#             "question": card.question,
#             "answer": card.answer,
#         },
#     )


@app.post("/flash-session/")
def launch_flash_session(selected_themes: list = Form(schema.Theme)):
    # Here, you can perform the logic to handle the selected themes for the flash session
    # For example, you can process the selected themes and generate the flash session content.

    # Return a response or redirect to the appropriate page after processing the selected themes
    return {"message": "Flash session launched successfully!"}


@app.get("/flash-session/", response_class=HTMLResponse)
def start_flash_session(request: Request, db: Session = Depends(get_db)):
    # Fetch cards for the flash session
    cards = crud.get_cards(
        db, limit=10
    )  # Assuming you want a maximum of 10 cards in the session

    # Combine both sets of data into a single list of CardWithThemeResponse
    card_themes = [(card, card.theme_name) for card in cards]

    return templates.TemplateResponse(
        "flash_session.html", {"request": request, "card_themes": card_themes}
    )
