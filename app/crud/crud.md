# Necessary imports
Import Session to declare the type of the db parameters and have better type checks and completion in functions
```python
from sqlalchemy.orm import Session
from sqlalchemy import func
```

Import sqlalchemy models + pydantic models
```python
from app.models.model import User, Card, Theme, Temp_session
from app.schema import user, card, theme, temp_session 
```

# Goal of theses crud scripts :
Define crud functions that are only dedicated to interacting with the database independent of path operation function
--> easily reuse them in multiple parts and also add unit tests for them

example : Read a single user by its ID
```python
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
```


