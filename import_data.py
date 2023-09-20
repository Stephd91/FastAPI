import os
import pandas as pd
from app.models import model
from app.config.config_sqlalchemy import engine, SessionLocal, Base

# Step 1: Drop all the tables /!\
# Use it wisely because all the values in the database will be deleted
# with SessionLocal() as session:
#    model.Base.metadata.drop_all(bind=engine)

# Step 2: Recreate the tables with the correct schema
Base.metadata.create_all(bind=engine)

# Step 3: Read the csv file using pandas
csv_file = os.path.join("", os.path.curdir, "Anki_cards.csv")
df = pd.read_csv(csv_file, delimiter=";")
df.columns = df.columns.str.lower()

# Importing Themes
print("Démarrage de l'import des données dans la table theme ...")
theme_id_map = {}  # Define the theme_id_map dictionary
with SessionLocal() as session:
    for theme_name in df["theme"].unique():
        if theme_name not in theme_id_map:
            theme = model.Theme(theme=theme_name)
            session.add(theme)
            session.commit()
            session.refresh(theme)  # Ensure that the theme is inserted and get its ID
            theme_id_map[theme_name] = theme.id

print("Theme IDs being inserted into the 'themes' table:")
for theme_name, theme_id in theme_id_map.items():
    print(f"{theme_name}: {theme_id}")

print("Import des données dans la table themes terminé.")

print("Démarrage de l'import des données dans la table anki_cards ...")

# Importing Anki Cards with Theme IDs
print(theme_id_map)
df["theme_id"] = df["theme"].map(theme_id_map)
df.drop(columns=["theme"], inplace=True)
# Reset the index of the DataFrame to start from 0
# df.reset_index(drop=True, inplace=True)
df.to_sql("anki_cards", con=engine, index=False, if_exists="append")

print("Import des données dans la table anki_cards terminé.")

print("Démarrage de l'import des données dans la table users ...")
fake_user = {
    "id": 1,
    "username": "rootuser",
    "email": "fakemail@mail.com",
    "hashed_password": "fakepassword",
}

with SessionLocal() as session:
    user = model.User(**fake_user)
    session.add(user)
    session.commit()
    session.refresh(user)

print("Import des données dans la table users terminé.")
