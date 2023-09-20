#!/bin/bash

# 1) Import data from anki_cards.csv import python3 si le fichier Anki_card.csv
currDir=$(pwd)
csv="Anki_cards.csv"
import_script="import_data.py"
if [ currDir/csv ]; then
    echo "Importing data from csv..."
    python3 $currDir/$import_script
    echo "Data from csv successfully imported into database !"
else
    echo "Error : missing csv file"
    exit
fi

# 2) Launch Uvicorn server 
uvicorn app.main:app --host 0.0.0.0 --port 80 
