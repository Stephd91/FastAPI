# tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app

# Use FastAPI's TestClient to send HTTP requests to your app
client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response


def test_homepage_router():
    response = client.get("/app")
    assert response.status_code == 200


def test_cards_router():
    response = client.get("/create-card")
    assert response.status_code == 200


def test_flashsession_router():
    # Define test data
    themes = ["Databases", "Cloud"]
    num_cards = 5

    # Make a POST request to the flash_session endpoint
    response = client.post(
        "/flash-session/",
        data={"themes": themes, "num_cards": num_cards},
    )
    assert response.status_code == 200
    # Check if Databases and Cloud are present in the response
    assert "Databases" in response.text
    assert "Cloud" in response.text


# def test_user_router():
