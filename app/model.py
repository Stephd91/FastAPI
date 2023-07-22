# Import necessary sqlalchemy packages to create our tables
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
# Import our Base class declared in the config_alchemy.py thanks to the delclarative-base function
from config_sqlalchemy import Base

# We want to define tables and columns from our Python classes using the ORM. 
# In SQLAlchemy, this is enabled through a declarative mapping. 
# The most common pattern is constructing a base class using the SQLALchemy declarative_base function (located in the config_sqlachemy file)
# and then we just have to create all DB model classes that will inherit from this base class.
class Anki_cards(Base):
    __tablename__ = "anki_cards" #The __tablename__ attribute tells SQLAlchemy the name of the table to use in the database for each of these models
    #Create model attributes/columns for this table :
    id = Column(Integer, primary_key=True, index=True) 
    theme = Column(String(256), nullable=False)
    question = Column(String(256), nullable=False)
    answer = Column(String(256), nullable=False)

    session_cards = relationship("Session", back_populates="cards")

class User(Base):
    __tablename__ = "users"
    #Create model attributes/columns for this table :
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(256), nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    reading_cards = relationship("Session", back_populates="reader")

class Session(Base):
    __tablename__ = "temp_session"
    id = Column(Integer, primary_key=True, index=True)
    reader_id = Column(Integer, ForeignKey("users.id"))
    card_id = Column(Integer, ForeignKey("anki_cards.id"))

    reader = relationship("User", back_populates="reading_cards")
    cards = relationship("Anki_cards", back_populates="session_cards")
