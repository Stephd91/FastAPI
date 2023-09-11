from sqlalchemy.orm import Session
from sqlalchemy import func

# Import sqlalchemy models + pydantic models
from app.models.model import User
from app.schemas.schema_user import UserCreate


# ----------- Users -----------
# Read a single user by its ID
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


# Read a single user by its email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


# Creat a new user
def create_user(db: Session, user: UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    # Create a SQLAlchemy model instance "db_user" with necessary data
    # (email and password as described in schemas.user.UserCreate) :
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=fake_hashed_password,
    )
    # Add that instance object to the database session
    db.add(db_user)
    # Commit the changes to the database (so that they are saved)
    db.commit()
    # Refresh the instance (so that it contains any new data from the database,
    #  like the generated ID)
    db.refresh(db_user)
    return db_user
