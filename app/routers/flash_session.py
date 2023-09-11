from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.schema_temp_session import Temp, TempCreate
from app.crud import crud_temp_session, crud_card

# Server-side rendering
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["flash-session"], default_response_class=HTMLResponse)
templates = Jinja2Templates(directory="app/templates")


# --------------- FLASH SESSION endpoint "/flash-session" ---------------
@router.post(
    "/flash-session/",
    response_model=Temp,
    name="start_flash_session",
)
def flash_session(
    request: Request,
    themes: list[str] = Form(...),
    num_cards: int = Form(...),
    db: Session = Depends(get_db),
):
    """
    Start a flash session with the specified themes and number of cards.

    Args:
        ▪️request (Request): HTTP request object provided by FastAPI.
        ▪️themes (list[str], optional): A list of theme names selected by the \
            user for the flash session.
        ▪️num_cards (int, optional): The number of flash cards selected by the\
            to be included in the session.
        ▪️db (Session, optional): SQLAlchemy database session.

    Returns:
        ▪️HTML Response: flash_session.html (Jinja2 template)
        ▪️schema.Temp: A new row in the Temp_session table will be inserted for
          each card displayed to the user.
    """
    # Fetch the list of cards
    flash_cards = crud_card.get_x_card_by_theme_list(db, themes, num_cards)
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
    reader_id = 1  # ⚒️En attendant de terminer les fonctions liées aux users
    session_id = crud_temp_session.find_last_session_id(db=db)
    for card in flash_cards:
        temp_session = TempCreate(
            reader_id=reader_id, card_id=card.id, session_id=session_id
        )
        crud_temp_session.create_temp_session(db=db, temp_session=temp_session)

    card_count = len(card_info)

    context = {"request": request, "card_info": card_info, "card_count": card_count}
    return templates.TemplateResponse("flash_session.html", context)
