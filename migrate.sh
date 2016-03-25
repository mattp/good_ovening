#!/bin/bash
DB="good_ovening/db/good_ovening.db"
DB_BKP="${DB}.bkp"

# Back up the database
if [ -f $DB ]; then
    echo "Backing up database..."
    mv $DB $DB_BKP
fi

# Reinsert any existing XML
for f in `ls xml/*.xml`; do echo "Inserting ${f}"; ./reinsert.sh $f; done
