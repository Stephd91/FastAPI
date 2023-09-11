from pydantic import BaseModel


# ----------- Themes -----------
class ThemeBase(BaseModel):
    """
    Initiate a basic ThemeBase object which requires the theme name
    """

    theme: str


class Theme(ThemeBase):
    """
    Initiate a Theme pydantic object that inherits theme name from ThemeBase
    and adds the required theme_id
    """

    id: int

    class Config:
        orm_mode = True
