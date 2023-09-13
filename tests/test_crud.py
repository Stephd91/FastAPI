"""# tests/test_crud.py

def test_get_card_by_id():
    # Create a mock database session using a temporary PostgreSQL database
    with SessionLocalTest(engine_test) as db:
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
    with SessionLocalTest(engine_test) as db:
        cards = crud.crud_card.get_cards(db, skip=0, limit=5)
        print(cards)
        print(type(cards))
        print(cards[0].question)

        assert len(cards) == 5
        assert cards is not None


def test_create_cards():
    with SessionLocalTest(engine_test) as db:
        # Generate data for the test
        card_data = {"question": "this is a test from pytest", "answer": "OK"}
        card = CardCreate(**card_data)
        user_id = 1
        theme_id = 1

        # Test the crud function create_anki_card()
        created_card = crud.crud_card.create_anki_card(db, card, user_id, theme_id)

        # Fetch the card from the database to check if it matches
        fetched_card = (
            db.query(Anki_cards).filter(Anki_cards.id == created_card.id).first()
        )
        print(fetched_card)
        print(type(fetched_card))
        print(fetched_card.question)

        # Assertions to check if the created card matches the expected data
        assert fetched_card is not None
        assert fetched_card.question == card_data["question"]
        assert fetched_card.answer == card_data["answer"]
        assert fetched_card.theme_id == theme_id
        assert fetched_card.creator_id == user_id


def test_modify_cards():
    with SessionLocalTest(engine_test) as db:
        # Generate data for the test
        card_data = {
            "question": "Modified !",
            "answer": "!!!",
            "creator_id": 1,
            "theme_name": "Data Engineering Intro",
        }
        card = CardUpdate(**card_data)
        card_id = 98

        # Test the crud function modify_anki_card()
        modified_card = crud.crud_card.modify_anki_card(db, card_id, card)

        # Fetch the card from the database to check if it matches
        fetched_card = (
            db.query(Anki_cards).filter(Anki_cards.id == modified_card.id).first()
        )
        print(fetched_card)
        print(type(fetched_card))
        print(fetched_card.question)

        # Assertions to check if the created card matches the expected data
        assert fetched_card is not None
        assert fetched_card.question == card_data["question"]
        assert fetched_card.answer == card_data["answer"]
        assert fetched_card.creator_id == card_data["creator_id"]


drop_test_database()
"""
