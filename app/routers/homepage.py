from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse

from sqlalchemy.orm import Session

from app.schemas.schema_card import Card
from app.crud import crud_theme, crud_card
from app.dependencies import get_db

# Server-side rendering
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["homepage"], default_response_class=HTMLResponse)
templates = Jinja2Templates(directory="app/templates")


# --------------- ANKI HOMEPAGE endpoint "/app" ---------------
# Afficher les cartes + les thèmes distincts -- TEST OK
@router.get(
    "/app/",
    response_model=list[Card],
    name="app",
)
def read_cards_themes(
    request: Request,
    skip: int = 0,
    card_limit: int = 100,
    theme_limit: int = 10,
    db: Session = Depends(get_db),
):
    """
    Retrieve cards and their themes + the distinct theme names to
    display on the main body of "app.html"

    Args:
        ▪️request (Request): HTTP request object provided by FastAPI. \
            It contains info about the incoming request (headers, cookies,...).
        ▪️skip (int, optional): nb cards to skip in the query result\
              (used for pagination). Defaults to 0.
        ▪️card_limit (int, optional): nb cards max retrieved. Defaults to 100.
        ▪️theme_limit (int, optional): nb theme max retrieved. Defaults to 10.
        ▪️db (Session, optional): SQLAlchemy database session created by the\
             `get_db` dependency to allow interaction with the database.

    Returns:
        ▪️HTML Response: app.html (Jinja2 template)
    """
    # Fetch the list of cards
    cards = crud_card.get_cards(db, skip=skip, limit=card_limit)
    card_with_themes = [(card, card.theme_name) for card in cards]

    # Fetch the list of themes
    themes = crud_theme.get_themes(db, limit=theme_limit)
    # Fetch the list of distinct themes
    themes_names = crud_theme.get_themes_names(db, limit=theme_limit)
    # context
    context = {
        "request": request,
        "card_with_themes": card_with_themes,
        "themes": themes,
        "themes_names": themes_names,
    }

    return templates.TemplateResponse("app.html", context)
