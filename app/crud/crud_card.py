from sqlalchemy.orm import Session
from sqlalchemy import func, text

# Import sqlalchemy models + pydantic models
from app.models.model import Anki_cards
from app.schemas.schema_card import CardCreate, CardUpdate
from app.models.model import Theme


# ----------- Anki Cards -----------
# Read anki cards (max 30)
def get_cards(db: Session, skip: int = 0, limit: int = 30):
    return db.query(Anki_cards).offset(skip).limit(limit).all()


# [For training purpose] Get an anki card by its with pure SQL query
def get_card_by_id(db: Session, card_id: int):
    query = text("SELECT * FROM Anki_Cards WHERE id = :card_id")
    # query will return a str
    return db.execute(query, {"card_id": card_id}).fetchone()


# Read anki cards themes name given their theme_id
def get_card_by_theme_id(db: Session, theme_id: int):
    return db.query(Anki_cards).filter(Anki_cards.theme_id == theme_id)


def get_x_card_by_theme_list(db: Session, themes: list, card_num: int):
    # Get theme IDs based on theme names
    theme_ids = db.query(Theme.id).filter(Theme.theme.in_(themes)).all()

    # Calculate the number of cards per theme
    cards_per_theme = card_num // len(theme_ids)
    remaining_cards = card_num % len(theme_ids)

    # Get cards from each theme
    cards = []
    for theme_id in theme_ids:
        query = (
            db.query(Anki_cards)
            .filter(Anki_cards.theme_id == theme_id[0])
            .order_by(func.random())
        )

        # Fetch the cards and add to the list
        theme_cards = query.limit(cards_per_theme).all()
        cards.extend(theme_cards)

    # If there are remaining cards, fetch and add them
    if remaining_cards > 0:
        query = db.query(Anki_cards).filter(Anki_cards.theme_id == theme_ids[0][0])
        remaining_theme_cards = query.limit(remaining_cards).all()
        cards.extend(remaining_theme_cards)
    return cards


# Create a new anki card. We could also use model.dump() to get the keywords
# arguments "question, answer" by passing card.model_dump() to the db_card object
def create_anki_card(db: Session, card: CardCreate, user_id: int, theme_id: int):
    db_card = Anki_cards(
        question=card.question,
        answer=card.answer,
        theme_id=theme_id,
        creator_id=user_id,
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


# Modify an existing  anki card
def modify_anki_card(db: Session, card_id: int, card: CardUpdate):
    # find the anki_card with the specified card_id
    card_to_modify = db.query(Anki_cards).filter(Anki_cards.id == card_id).first()

    # Update the card's properties
    card_to_modify.question = card.question
    card_to_modify.answer = card.answer
    card_to_modify.creator_id = card.creator_id

    db.commit()
    db.refresh(card_to_modify)
    return card_to_modify


# Delete an existing  anki card
def delete_anki_card(db: Session, card_id: int):
    card_to_delete = db.query(Anki_cards).filter(Anki_cards.id == card_id).first()
    if card_to_delete:
        db.delete(card_to_delete)
        db.commit()
        return card_to_delete
    else:
        return None
