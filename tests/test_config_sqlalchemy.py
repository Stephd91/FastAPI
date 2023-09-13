import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.main import app
from app.dependencies import get_db

from app.schemas.schema_card import CardCreate


@pytest.fixture(name="session")
def session_fixture():
    # Create an in-memory PostgreSQL database for testing
    engine = create_engine("postgresql+psycopg2://", echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create the database tables
    from app.models import model  # Import your models

    model.Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_card(client: TestClient):
    # Define test data
    card_data = {
        "question": "this is a test from pytest",
        "answer": "OK",
        "theme_name": "Databases",
    }
    # Make a POST request to the create-card endpoint
    response = client.post(
        "/create-card/",
        json=card_data,
        headers={"Content-Type": "application/json"},
    )
    data = response.json()
    print(data)

    assert response.status_code == 422
    assert data is not None
