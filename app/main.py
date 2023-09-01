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


# --------------- ANKI HOMEPAGE endpoint "/app" ---------------
# Afficher les cartes + les thèmes distincts -- TEST OK
@app.get(
    "/app/",
    response_model=list[schema.Card],
    response_class=HTMLResponse,
    name="app",
)
def read_cards_themes(
    request: Request,
    skip: int = 0,
    card_limit: int = 100,
    theme_limit: int = 10,
    db: Session = Depends(get_db),
):
    """Retrieve cards and their themes + the distinct theme names to
    display on the main body of "app.html"

    Args:
        request (Request): _description_
        skip (int, optional): _description_. Defaults to 0.
        card_limit (int, optional): nb cards max displayed. Defaults to 100.
        theme_limit (int, optional): nb theme max displayed. Defaults to 10.
        db (Session, optional): sqlalchemy session

    Returns:
        _type_: app.html (Jinja2 template)
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
    request: Request,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    cards = crud.get_cards(db, skip=skip, limit=limit)
    card_themes = [(card, card.theme_name) for card in cards]
    print(card_themes[0][1].theme)
    return templates.TemplateResponse(
        "app.html", {"request": request, "card_themes": card_themes}
    )


# --------------- FLASH SESSION endpoint "/flash-session" ---------------
@app.post(
    "/flash-session/",
    response_class=HTMLResponse,
    response_model=schema.Temp,
    name="start_flash_session",
)
def flash_session(
    request: Request,
    themes: list[str] = Form(...),
    num_cards: int = Form(...),
    db: Session = Depends(get_db),
):
    # Fetch the list of cards
    flash_cards = crud.get_x_card_by_theme_list(db, themes, num_cards)
    # Extract relevant card information for rendering
    card_info = []
    for card in flash_cards:
        card_info.append(
            {
                "theme": card.theme_name.theme,
                "question": card.question,
                "answer": card.answer,
            }
        )

    # based on the pydantic Temp object, that will fill the table "Temp_session"
    # with the reader_id of the user and the card_id of each card restitued
    # from the get_x_card_by_theme_list() function
    # we need to iterate to create a new line in the Temp_session table for each card
    reader_id = 1  # En attendant de terminer les fonctions liées aux users
    session_id = crud.find_last_session_id(db=db)
    for card in flash_cards:
        temp_session = schema.TempCreate(
            reader_id=reader_id, card_id=card.id, session_id=session_id
        )
        crud.create_temp_session(db=db, temp_session=temp_session)

    card_count = len(card_info)

    context = {"request": request, "card_info": card_info, "card_count": card_count}
    return templates.TemplateResponse("flash_session.html", context)


# --------------- USER CREATION endpoint "/signup" ---------------
# Define a GET route for the sign-up page with csrf_token
@app.get("/signup/", response_class=HTMLResponse, name="signup")
def get_signup_page(request: Request):
    csrf_token = request.cookies.get("csrf_token")
    return templates.TemplateResponse(
        "signup.html", {"request": request, "csrf_token": csrf_token}
    )


# Define a POST route to create a new user
@app.post(
    "/signup/",
    response_class=HTMLResponse,
    response_model=schema.UserCreate,
    name="create_user",
)
def create_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    csrf_token: str = Form(...),
    db: Session = Depends(get_db),
):
    user = schema.UserCreate(
        username=username,
        email=email,
        password=password,
    )
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = crud.create_user(db=db, user=user)
    context = {"request": request, "new_user": new_user, "csrf_token": csrf_token}
    return templates.TemplateResponse("signup.html", context)


# --------------- CARD CREATION endpoint "/card-creation" ---------------
# Define a GET route for the create card page
@app.get(
    "/create-card/",
    response_class=HTMLResponse,
    name="create-card",
)
def get_create_card(
    request: Request,
    theme_limit: int = 10,
    db: Session = Depends(get_db),
):
    themes_names = crud.get_themes_names(db, limit=theme_limit)
    context = {"request": request, "themes_names": themes_names}
    return templates.TemplateResponse("create_card.html", context)


# Define a POST route to create a new card
@app.post(
    "/create-card/",
    response_class=HTMLResponse,
    response_model=schema.Card,
    name="create_card",
)
def create_card(
    request: Request,
    question: str = Form(...),
    answer: str = Form(...),
    theme_name: str = Form(...),
    db: Session = Depends(get_db),
):
    theme = crud.get_theme_by_theme_name(db, theme_name=theme_name)
    creator_id = 1  # En attente de création de la fonction AuthJWT
    card = schema.CardCreate(
        question=question,
        answer=answer,
    )
    new_card = crud.create_anki_card(
        db,
        card=card,
        user_id=creator_id,
        theme_id=theme.id,
    )
    context = {"request": request, "new_card": new_card}
    return templates.TemplateResponse("create_card.html", context)


# ------------------ JUNK --------------------
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
