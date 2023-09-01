# Import necessary sqlalchemy packages to create our tables
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, text
from sqlalchemy.orm import relationship

# Import our Base class declared in the config_alchemy.py thanks to the delclarative-base function
from config_sqlalchemy import Base

from uuid import UUID, uuid4


# We want to define tables and columns from our Python classes using the ORM.
# In SQLAlchemy, this is enabled through a declarative mapping.
# The most common pattern is constructing a base class using the SQLALchemy declarative_base function (located in the config_sqlachemy file)
# and then we just have to create all DB model classes that will inherit from this base class.
class Anki_cards(Base):
    __tablename__ = "anki_cards"  # The __tablename__ attribute tells SQLAlchemy the name of the table to use in the database for each of these models
    # Create model attributes/columns for this table :
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(256), nullable=False)
    answer = Column(String(256), nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    theme_id = Column(Integer, ForeignKey("themes.id"))

    creator_user = relationship("User", back_populates="created_cards")
    session_cards = relationship("Temp_session", back_populates="cards")
    theme_name = relationship("Theme", back_populates="cards")


class Theme(Base):
    __tablename__ = "themes"
    # Create model attributes/columns for this table :
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    theme = Column(String(256), nullable=False)

    # One-to-Many relationship :
    cards = relationship("Anki_cards", back_populates="theme_name")


class User(Base):
    __tablename__ = "users"
    # Create model attributes/columns for this table :
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(256), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # One-to-Many relationships :
    created_cards = relationship("Anki_cards", back_populates="creator_user")
    reading_cards = relationship("Temp_session", back_populates="reader")


class Temp_session(Base):
    __tablename__ = "temp_session"
    # Create model attributes/columns for this table :
    uuid = Column(
        String,
        primary_key=True,
        index=True,
        server_default=text(
            "uuid_generate_v4()"
        ),  # Generate a new UUID on the server-side
        unique=True,
        nullable=False,
    )
    session_id = Column(Integer, nullable=False)
    reader_id = Column(Integer, ForeignKey("users.id"))
    card_id = Column(Integer, ForeignKey("anki_cards.id"))

    reader = relationship("User", back_populates="reading_cards")
    cards = relationship("Anki_cards", back_populates="session_cards")
