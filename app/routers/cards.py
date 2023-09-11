from fastapi import APIRouter, HTTPException, Request, Depends, Form
from fastapi.responses import HTMLResponse, JSONResponse

from sqlalchemy.orm import Session

from app.schemas.schema_card import Card, CardCreate, CardUpdate
from app.crud import crud_theme, crud_card
from app.dependencies import get_db

# Server-side rendering
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["cards"], default_response_class=HTMLResponse)
templates = Jinja2Templates(directory="app/templates")


# --------------- CARD CREATION endpoint "/create-card" ---------------
# Define a GET route for the create card page
@router.get(
    "/create-card/",
    name="create-card",
)
def get_create_card(
    request: Request,
    theme_limit: int = 10,
    db: Session = Depends(get_db),
):
    """
    Displays the HTML page to create a card

    Args:
        request (Request): HTTP request object provided by FastAPI.
        theme_limit (int, optional): Theme list displayed Defaults to 10.
        db (Session, optional): SQLAlchemy database session.

    Returns:
        _type_: create_card.html (Jinja2 template)
    """
    themes_names = crud_theme.get_themes_names(db, limit=theme_limit)
    context = {"request": request, "themes_names": themes_names}
    return templates.TemplateResponse("create_card.html", context)


# Define a POST route to create a new card
@router.post(
    "/create-card/",
    response_model=Card,
    name="create_card",
)
def create_card(
    request: Request,
    question: str = Form(...),
    answer: str = Form(...),
    theme_name: str = Form(...),
    db: Session = Depends(get_db),
):
    """
    Post function that creates a new Anki card.

    This route allows users to create a new Anki card by providing a question,
    an answer, and a theme name. The flashcard is associated with the provided
    theme and is attributed to the authenticated user.

    Args:
        request (Request): HTTP request object provided by FastAPI.
        question (str, optional): question provided by user.
        answer (str, optional): answer provided by user.
        theme_name (str, optional): theme name provided by user.
        db (Session, optional): SQLAlchemy database session.

    Returns:
        ▪️HTML Response: create_card.html (Jinja2 template)
        ▪️schema.Card: The newly created Anki card inserted in the database.
    """
    theme = crud_theme.get_theme_by_theme_name(db, theme_name=theme_name)
    creator_id = 1  # En attente de création de la fonction AuthJWT
    card = CardCreate(
        question=question,
        answer=answer,
    )
    new_card = crud_card.create_anki_card(
        db,
        card=card,
        user_id=creator_id,
        theme_id=theme.id,
    )
    context = {"request": request, "new_card": new_card}
    return templates.TemplateResponse("create_card.html", context)


# --------------- CARD MODIFICATION endpoint "/modify-card" ---------------
# Define a PUT route for the modif-card page
@router.put(
    "/modify-card/{card_id}",
    response_class=JSONResponse,
    response_model=Card,
    name="modify-card",
)
def modif_card(
    # request: Request,
    card_id: int,
    card: CardUpdate,
    db: Session = Depends(get_db),
):
    """
    Modify an existing Anki card.

    Args:
        card_id (int): card_id provided by user in the API route.
        card (schema.CardUpdate): card ORM object returned by the database
        db (Session, optional): SQLAlchemy database session.

    Raises:
        HTTPException: If requested card is not found
        ValueError: If Theme does not exist

    Returns: a modified card object
    """
    # Ensure the card with the specified ID exists
    existing_card = crud_card.get_card_by_id(db, card_id)
    if existing_card is None:
        raise HTTPException(status_code=404, detail=f"Card with ID {card_id} not found")

    # Retrieve the theme by name to get its ID
    theme = crud_theme.get_theme_by_theme_name(db, theme_name=card.theme_name)
    if theme is None:
        raise ValueError(f"The theme {card.theme_name} does not exist.")

    modified_card = crud_card.modify_anki_card(db, card_id, card)
    return modified_card


# --------------- CARD DELETION endpoint "/delete-card" ---------------
# Define a DELETE route for the delete-card page
@router.delete(
    "/delete-card/{card_id}",
    response_class=JSONResponse,
    name="delete-card",
)
def delete_card(
    # request: Request,
    card_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete an existing Anki card.

    Args:
        card_id (int): card_id provided by user in the API route.
        db (Session, optional): SQLAlchemy database session.

    Raises:
        HTTPException: If requested card is not found

    Returns: a JSON message if successfully deleted the card
    """
    card_to_delete = crud_card.delete_anki_card(db=db, card_id=card_id)
    if card_to_delete is None:
        raise HTTPException(status_code=404, detail=f"Card with ID {card_id} not found")

    return {"message": f"Card with ID {card_id} has been successfully deleted"}
