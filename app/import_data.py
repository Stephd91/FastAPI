from config_sqlalchemy import engine
import pandas as pd

# Read the csv file using pandas 
df = pd.read_csv("../Anki_cards.csv", delimiter=";")
df.columns = df.columns.str.lower()
print("Démarrage de l'import des données dans la table anki_cards ...")

# Import our data into the "anki_cards" table. 
# As the table is already declared through the "model.py" script, we need to add "if_exists='append'" 
df.to_sql('anki_cards', con=engine, index=False, if_exists="append")

print("Import des données terminé.")