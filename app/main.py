# STEP 1 : Import FastAPI & librairies
# FastAPI : a Python class that provides all the functionality for your API.
from pathlib import Path
from fastapi import FastAPI, Request

# Handling of all front-end files like images, custom css, ...
from fastapi.staticfiles import StaticFiles

# Server-side rendering
from fastapi.templating import Jinja2Templates

# To connect to our learn_de database
from app.config.config_sqlalchemy import engine

# Import our submodules to construct our tables in the database, the schemas,
# and interacting with them via crud operations
from app.models import model
from app.routers import homepage, flash_session, cards, users


# STEP 2 : Connect to database
# To create and interact with the database tables defined in our model.py file
# Other possibility : initialize database (create tables, etc) with Alembic
model.Base.metadata.create_all(bind=engine)


# STEP 3 : Create a FastAPI "instance"
# the app variable will be an "instance" of the class FastAPI.
# This will be the main point of interaction to create all your API.
# We also declare the templates to use for the server-side rendering with jinja
app = FastAPI()
app.include_router(cards.router)
app.include_router(flash_session.router)
app.include_router(homepage.router)
app.include_router(users.router)


# Define the path to the "static" folder
static_folder = Path(__file__).parent / "static"
# Mount the "static" folder to serve static files
app.mount("/static", StaticFiles(directory=static_folder), name="static")
templates = Jinja2Templates(directory="app/templates")


# STEP 4 : Create path operations = endpoints = routes
# --------------- ANKI LANDING PAGE endpoint "/" ---------------
@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
