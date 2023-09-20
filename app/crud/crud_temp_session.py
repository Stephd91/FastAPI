from sqlalchemy.orm import Session
from sqlalchemy import func
import uuid

# Import sqlalchemy models + pydantic models
from app.models.model import Temp_session
from app.schemas.schema_temp_session import TempCreate


# ----------- Temporary session  -----------
# Create a new line in temp_session with the reader_id and the card_id
def create_temp_session(db: Session, temp_session: TempCreate):
    db_temp_session = Temp_session(
        id=str(uuid.uuid4()),
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
    max_session_id = db.query(func.max(Temp_session.session_id)).scalar()

    # Increment the largest session_id by 1 for the new entry
    session_id = max_session_id + 1 if max_session_id is not None else 1
    return session_id
