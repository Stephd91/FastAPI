from app.db.config_sqlalchemy import SessionLocal

# Server-side rendering
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


# To open a SQLAlchemy session for each request, we need a dependency to have
# for each request an independent database session/connection (SessionLocal).
# Our dependency will create a new SQLAlchemy SessionLocal that will be used
# in a single request, and then close it once the request is finished
# Then, a new session is created for the next request.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
