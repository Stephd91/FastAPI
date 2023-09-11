from pydantic import BaseModel
from typing import Optional


# ----------- Anki Cards -----------
class CardBase(BaseModel):
    """
    Initiate a basic CardBase object which requires question and answer
    """

    question: str
    answer: str


class CardCreate(CardBase):
    """
    Initiate a CardCreate that inherits question and answer attributs
    from CardBase
    """

    pass


class CardUpdate(CardBase):
    """
    Initiate a CardUpdate that inherits question and answer attributs
    from CardBase and adds the required theme name and optional creator_id
    """

    creator_id: Optional[int]
    # creator_id is optional for now ⚒️ waiting to implement user functions
    theme_name: str


class Card(CardBase):
    """
    This class will create a complete Anki Card in our database with all the
    required values
    """

    id: int
    theme_id: int
    creator_id: Optional[int]

    # To allow Pydantic to work with ORM objects and simplify data
    # serialization/de-serialization during interaction with sqlalchemy
    # Pydantic's orm_mode will tell the Pydantic model to read the data
    # even if it is not a dict
    class Config:
        orm_mode = True  # This is setting a config value, not declaring a type
