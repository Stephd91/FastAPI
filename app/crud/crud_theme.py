from sqlalchemy.orm import Session
from sqlalchemy import func

# Import sqlalchemy models + pydantic models
from app.models.model import Theme

# from app.schemas.theme import ThemeBase


# ----------- Themes  -----------
def get_themes(db: Session, limit: int = 30):
    return db.query(Theme).distinct().limit(limit).all()


def get_themes_names(db: Session, limit: int = 10):
    distinct_themes = db.query(Theme.theme).distinct().limit(limit).all()
    theme_names = [theme.theme for theme in distinct_themes]
    print(theme_names)
    return theme_names


def get_theme_by_theme_name(db: Session, theme_name: str):
    return db.query(Theme).filter(Theme.theme == theme_name).first()
