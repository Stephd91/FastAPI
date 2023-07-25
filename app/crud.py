# Import Session to declare the type of the db parameters and have better type checks and completion in functions
from sqlalchemy.orm import Session

# Import sqlalchemy models + pydantic models
import model, schema

# Goal of this script : create functions that are only dedicated to interacting with the database independent of path operation function
# --> easily reuse them in multiple parts and also add unit tests for them

"""----------- Anki Cards -----------"""


# Read anki cards (max 30)
def get_cards(db: Session, skip: int = 0, limit: int = 30):
    return db.query(model.Anki_cards).offset(skip).limit(limit).all()


# Read anki cards themes name given their theme_id
def get_card_by_theme_id(db: Session, theme_id: int):
    return db.query(model.Anki_cards).filter(model.Anki_cards.theme_id == theme_id)


# Create a new anki card. We could also use a dict to get the keywords arguments "theme, question, answer" by passing **card.dict() to the db_card object
def create_anki_card(db: Session, card: schema.CardCreate, user_id: int):
    db_card = model.Anki_cards(
        theme=card.theme, question=card.question, answer=card.answer, creator_id=user_id
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


# Modify an existing  anki card
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


"""----------- Users -----------"""


# Read a single user by its ID
def get_user(db: Session, user_id: int):
    return db.query(model.User).filter(model.User.id == user_id).first()


# Read a single user by its username
def get_user(db: Session, username: str):
    return db.query(model.User).filter(model.User.username == username).first()


# Creat a new user
def create_user(db: Session, user: schema.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    # Create a SQLAlchemy model instance "db_user" with necessary data (email and password as described in schema.UserCreate) :
    db_user = model.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)  # Add that instance object to the database session
    db.commit()  # Commit the changes to the database (so that they are saved)
    db.refresh(
        db_user
    )  # Refresh the instance (so that it contains any new data from the database, like the generated ID)
    return db_user


"""----------- Temporary session  -----------"""


# Create a new session with x cards for a specified user and specified theme(s) by the user
def create_temp_session(db: Session, user_id: int, theme_id: list):
    cards = get_cards()
    return db.query(model.Temp_session).filter(
        model.Temp_session.reader_id == user_id,
        model.Temp_session.cards == cards,
        db.query(model.Anki_cards).filter(model.Anki_cards.theme_id == theme_id),
    )
