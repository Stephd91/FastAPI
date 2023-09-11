# tests/test_crud.py
from app import crud
from sqlalchemy.orm import Session
from app.main import app  # Import your FastAPI app

# Use FastAPI's TestClient to send HTTP requests to your app
from fastapi.testclient import TestClient

# To connect to our learn_de database
from app.db.config_sqlalchemy import engine

# Create a TestClient instance
client = TestClient(app)


def test_get_card_by_id():
    # Create a mock database session using a temporary PostgreSQL database
    with Session(engine) as db:
        # Replace 'known_card_id' with the ID of a card you want to test
        known_card_id = 66

        # Call the function with the known card ID
        card = crud.crud_card.get_card_by_id(db, known_card_id)
        print(card)
        print(type(card))

        # Assert that 'card' contains the expected information
        # Check if a card was found
        assert card is not None
        # Check if the card's ID matches the known card ID
        assert card.id == known_card_id


def test_get_cards():
    with Session(engine) as db:
        cards = crud.crud_card.get_cards(db, skip=0, limit=5)
        print(cards)
        print(type(cards))
        print(cards[0].question)

        assert len(cards) == 5
        assert cards is not None
