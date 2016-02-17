#!/bin/bash

# Set up session variables
XML_FILE=$1

# Initialize the database (if needed) and insert extracted elements
echo "###################"
echo -e "Initializing database..."
python -m good_ovening.db.sqlite_init
echo -e "\nStarting database insertion..."
python -m good_ovening.extract -i $XML_FILE
echo "Database insertion complete."

# Clean up
echo -e "\nDone."
echo "###################"
