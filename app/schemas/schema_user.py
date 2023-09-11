from pydantic import BaseModel
from .schema_card import CardCreate


# ----------- Users -----------
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    """
    Initiate a UserCreate that inherits email attributes from UserBase
    and adds the required username and password
    """

    username: str
    password: str


class User(UserBase):
    """
    Initiate a User pydantic object that inherits email from UserBase
    and adds the required user_id, is_active and optional cards created by the user
    """

    id: int
    is_active: bool
    cards: list[CardCreate] = []

    class Config:
        orm_mode = True
