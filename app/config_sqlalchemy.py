# 1) Import the SQLAlchemy parts and the environment variables (with decouple)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from decouple import config

"""import subprocess
# Exécutez la commande `sudo su - postgres`
output = subprocess.call(["sudo", "su", "-","postgres"])"""

# 2) Create a database URL for SQLAlchemy to connect to the PostgreSQL database ("postgresql://user:password@postgresserver/db")
# Load environment variables from .env
DB_USER = config("DB_USER")
DB_PASSWORD = config("DB_PASSWORD")
DB_HOST = config("DB_HOST")
DB_PORT = config("DB_PORT")
DB_NAME = config("DB_NAME")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# 3) Create a SQLAlchemy "engine" to handle connexion to the postgreSQL database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 4) Create a SessionLocal class with the function "sessionmaker"
# The class itself is not a database session yet, each instance of the SessionLocal class will be a database session
# We name it SessionLocal to distinguish it from the Session we are importing from SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5) Create a Base class to declare ou tables in model.py
# the function declarative_base() returns a class
# This class will be called to create each of the database models or classes (the ORM models)
Base = declarative_base()
