# Necessary imports
Import pydantic BaseModel to declare the initiate the different schemas
```python
from pydantic import BaseModel
from typing import Optional
```
# Goal of these schema scripts :
Pydantic models, like Card and User, define a "schema" (valid data shape).\
Their role is to validate and ensure that the received data adheres to the specified structure and data types defined below ==> integrity and consistency of data.\
If the data doesn't match the requirements, Pydantic will raise validation errors.

To allow Pydantic to work with ORM objects and simplify data serialization/de-serialization during interaction with sqlalchemy, Pydantic's orm_mode = True will tell the Pydantic model to read the data even if it is not a dict

Example : create a Card pydantic schema
```python
class Card(CardBase):
    """
    This class will create a complete Anki Card in our database with all the required values
    """

    id: int
    theme_id: int
    creator_id: Optional[int]

    
    class Config:
        orm_mode = True  # This is setting a config value, not declaring a type
```