# Import necessary sqlalchemy packages to create our tables
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, text
from sqlalchemy.orm import relationship

from ..config.config_sqlalchemy import Base

from sqlalchemy.dialects.postgresql import UUID


class Anki_cards(Base):
    __tablename__ = "anki_cards"  # name of the table
    # Create model attributes/columns for this table :
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
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
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
    )
    session_id = Column(Integer, nullable=False)
    reader_id = Column(Integer, ForeignKey("users.id"))
    card_id = Column(Integer, ForeignKey("anki_cards.id"))

    reader = relationship("User", back_populates="reading_cards")
    cards = relationship("Anki_cards", back_populates="session_cards")
