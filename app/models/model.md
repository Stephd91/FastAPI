# Necessary imports
Import sqlalchemy packages to create our tables
```python
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, text
from sqlalchemy.orm import relationship
```

Import our Base class declared in the config_alchemy.py thanks to the declarative-base function
```python
from app.db.config_sqlalchemy import Base
```

# Goal of this model script :
Define tables and columns from our Python classes using the ORM. In SQLAlchemy, this is enabled through a declarative mapping.
The most common pattern is constructing a base class using the SQLALchemy declarative_base function (located in the config_sqlachemy file) and then we just have to create all DB model classes that will inherit from this base class.

example : create an Anki_cards table
```python
class Anki_cards(Base):
    __tablename__ = "anki_cards"  # name of the table
    # Create model attributes/columns for this table :
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question = Column(String(256), nullable=False)
    answer = Column(String(256), nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    theme_id = Column(Integer, ForeignKey("themes.id"))

    creator_user = relationship("User", back_populates="created_cards")
    session_cards = relationship("Temp_session", back_populates="cards")
    theme_name = relationship("Theme", back_populates="cards")
```


