# Import Session to declare the type of the db parameters and have better type checks and completion in functions
from sqlalchemy.orm import Session
from sqlalchemy import func

# Import sqlalchemy models + pydantic models
import model, schema

# Goal of this script : create functions that are only dedicated to interacting with the database independent of path operation function
# --> easily reuse them in multiple parts and also add unit tests for them


# ----------- Anki Cards -----------
# Read anki cards (max 30)
def get_cards(db: Session, skip: int = 0, limit: int = 30):
    return db.query(model.Anki_cards).offset(skip).limit(limit).all()


# Read anki cards themes name given their theme_id
def get_card_by_theme_id(db: Session, theme_id: int):
    return db.query(model.Anki_cards).filter(model.Anki_cards.theme_id == theme_id)


def get_x_card_by_theme_list(db: Session, themes: list, card_num: int):
    # Get theme IDs based on theme names
    theme_ids = db.query(model.Theme.id).filter(model.Theme.theme.in_(themes)).all()

    # Calculate the number of cards per theme
    cards_per_theme = card_num // len(theme_ids)
    remaining_cards = card_num % len(theme_ids)

    # Get cards from each theme
    cards = []
    for theme_id in theme_ids:
        query = (
            db.query(model.Anki_cards)
            .filter(model.Anki_cards.theme_id == theme_id[0])
            .order_by(func.random())
        )

        # Fetch the cards and add to the list
        theme_cards = query.limit(cards_per_theme).all()
        cards.extend(theme_cards)

    # If there are remaining cards, fetch and add them
    if remaining_cards > 0:
        query = db.query(model.Anki_cards).filter(
            model.Anki_cards.theme_id == theme_ids[0][0]
        )
        remaining_theme_cards = query.limit(remaining_cards).all()
        cards.extend(remaining_theme_cards)
    return cards


# Create a new anki card. We could also use model.dump() to get the keywords
# arguments "question, answer" by passing card.model_dump() to the db_card object
def create_anki_card(db: Session, card: schema.CardCreate, user_id: int, theme_id: int):
    db_card = model.Anki_cards(
        question=card.question,
        answer=card.answer,
        theme_id=theme_id,
        creator_id=user_id,
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


# Modify an existing  anki card /// TO DO !!!
def modify_anki_card(
    db: Session, card: schema.Card, card_id: int, user_id: int, theme_id: int
):
    # find the anki_card with the specified card_id
    db_card = db.query(model.Anki_cards).filter(model.Anki_cards.id == card_id)
    if db_card is None:
        raise ValueError(f"The Anki card with ID {card_id} does not exist.")
    else:
        db_card_modif = model.Anki_cards(
            question=card.question,
            answer=card.answer,
            creator_id=user_id,
            theme_id=theme_id,
        )
    db.commit()
    db.refresh(db_card_modif)
    return db_card_modif


# Delete an existing  anki card /// TO DO !!!
# def delete_anki_card():
#     return


# ----------- Themes  -----------
def get_themes(db: Session, limit: int = 30):
    return db.query(model.Theme).distinct().limit(limit).all()


def get_themes_names(db: Session, limit: int = 10):
    distinct_themes = db.query(model.Theme.theme).distinct().limit(limit).all()
    theme_names = [theme.theme for theme in distinct_themes]
    print(theme_names)
    return theme_names


def get_theme_by_theme_name(db: Session, theme_name: str):
    return db.query(model.Theme).filter(model.Theme.theme == theme_name).first()


# ----------- Users -----------
# Read a single user by its ID
def get_user(db: Session, user_id: int):
    return db.query(model.User).filter(model.User.id == user_id).first()


# Read a single user by its email
def get_user_by_email(db: Session, email: str):
    return db.query(model.User).filter(model.User.email == email).first()


# Creat a new user
def create_user(db: Session, user: schema.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    # Create a SQLAlchemy model instance "db_user" with necessary data (email and password as described in schema.UserCreate) :
    db_user = model.User(
        username=user.username,
        email=user.email,
        hashed_password=fake_hashed_password,
    )
    db.add(db_user)  # Add that instance object to the database session
    db.commit()  # Commit the changes to the database (so that they are saved)
    db.refresh(
        db_user
    )  # Refresh the instance (so that it contains any new data from the database, like the generated ID)
    return db_user


# ----------- Temporary session  -----------
# Create a new line in temp_session with the reader_id and the card_id
def create_temp_session(db: Session, temp_session: schema.TempCreate):
    db_temp_session = model.Temp_session(
        session_id=temp_session.session_id,
        reader_id=temp_session.reader_id,
        card_id=temp_session.card_id,
    )
    db.add(db_temp_session)
    db.commit()
    db.refresh(db_temp_session)
    return db_temp_session


def find_last_session_id(db: Session):
    # Find the largest session_id in the temp_session table
    max_session_id = db.query(func.max(model.Temp_session.session_id)).scalar()

    # Increment the largest session_id by 1 for the new entry
    session_id = max_session_id + 1 if max_session_id is not None else 1
    return session_id
