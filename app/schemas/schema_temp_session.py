from pydantic import BaseModel
from .schema_card import Card
from .schema_user import User


# ----------- Temporary session  -----------
class TempBase(BaseModel):
    """
    Initiate a basic TempBase object which requires the session_id, reader_id and optionnal card_id
    """

    session_id: int
    reader_id: int
    card_id: int | None


class TempCreate(TempBase):
    """
    Initiate a TempCreate that inherits attributes from TempBase
    """

    pass


class Temp(TempBase):
    """
    This class will create a complete Temporary session in our database with all the required values
    """

    uuid: str
    session_id: int
    cards: list[Card] = []
    reader: User
    # themes: list[Theme] = []

    class Config:
        orm_mode = True
