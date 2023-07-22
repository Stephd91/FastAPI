# To avoid confusion between the SQLAlchemy models and the Pydantic models, we will have :
# --> the file models.py with the SQLAlchemy models
# --> the file schemas.py with the Pydantic models
# These Pydantic models, such as Card and User, define a "schema" (a valid data shape)
# Their role is to validate and ensure that the received data adheres to the specified structure and data types defined below ==> integrity and consistency of data
# If the data doesn't match the requirements, Pydantic will raise validation errors.
from pydantic import BaseModel

'''----------- Anki Cards -----------'''
# For creating a basic Anki Card, which requires theme, question and answer
class CardBase(BaseModel):
    theme: str
    question: str
    answer: str

# CardCreate hérite des attributs theme, question et answer de notre CardBase sans ajouter d'attributs supplémentaires
class CardCreate(CardBase):
    pass

# This class will create a complete Anki Card in our database (with its id that is required)
class Card(CardBase):
    id: int
     # To allow Pydantic to work with ORM objects and simplify data serialization/de-serialization during interaction with sqlalchem
    # Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict
    class Config:
        orm_mode = True # This is setting a config value, not declaring a type

'''----------- Users -----------'''
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    email: str
    password: str

class User(UserBase):
    id: int
    is_active: bool
    cards: list[CardCreate]=[]
    class Config:
        orm_mode = True # This is setting a config value, not declaring a type

'''----------- Temporary session  -----------'''
class TempBase(BaseModel):
    reader_id: int
    card_id: int

class Temp(TempBase):
    id: int
    cards: list[Card]=[]
    user: list[User]=[]
    class Config:
        orm_mode = True