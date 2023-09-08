# tests/test_database.py
from sqlalchemy.orm import Session
from app.crud import get_card_by_id


def test_get_card_by_id():
    # Create a mock database session (you may need to import your Session)
    mock_db_session = Session()

    # Replace 'known_card_id' with the ID of a card you want to test
    known_card_id = 1

    # Call the function with the known card ID
    card = get_card_by_id(mock_db_session, known_card_id)
    print(card)

    # Assert that 'card' contains the expected information
    assert card is not None  # Check if a card was found
    assert card.id == known_card_id  # Check if the card's ID matches the known card ID
    # Add more assertions for other card attributes as needed
