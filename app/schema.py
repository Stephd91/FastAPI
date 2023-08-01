# To avoid confusion between the SQLAlchemy models and the Pydantic models, we will have :
# --> the file models.py with the SQLAlchemy models
# --> the file schemas.py with the Pydantic models
#  Pydantic models, like Card and User, define a "schema" (valid data shape)
# Their role is to validate and ensure that the received data adheres to the
# specified structure and data types defined below ==> integrity and consistency of data
# If the data doesn't match the requirements, Pydantic will raise validation errors.
from pydantic import BaseModel
from typing import Optional


# ----------- Anki Cards -----------
# For creating a basic Anki Card, which requires question and answer
class CardBase(BaseModel):
    """Initiate a CardBase object
    Args:
        BaseModel (_type_): initiate the pydantic model
    """

    question: str
    answer: str


# CardCreate hérite des attributs question et answer de notre CardBase
# sans ajouter d'attributs supplémentaires
class CardCreate(CardBase):
    pass


# This class will create a complete Anki Card in our database
# with all the required values
class Card(CardBase):
    id: int
    theme_id: int
    creator_id: Optional[int]

    # To allow Pydantic to work with ORM objects and simplify data serialization/de-serialization during interaction with sqlalchem
    # Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict
    class Config:
        orm_mode = True  # This is setting a config value, not declaring a type


# ----------- Themes -----------
class ThemeBase(BaseModel):
    theme: str


class Theme(ThemeBase):
    id: int

    class Config:
        orm_mode = True


# ----------- Users -----------
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    username: str
    password: str


class User(UserBase):
    id: int
    is_active: bool
    cards: list[CardCreate] = []

    class Config:
        orm_mode = True


# ----------- Temporary session  -----------
class TempBase(BaseModel):
    reader_id: int
    card_id: int


class Temp(TempBase):
    id: int
    cards: list[Card] = []
    reader: User
    theme: list[Theme] = []

    class Config:
        orm_mode = True


# ----------- Autres objets custom  -----------
"""class CardWithTheme(BaseModel):
    list_card: list[Card]
    list_theme: list[Theme]"""
