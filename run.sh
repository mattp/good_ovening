#!/bin/bash

# Set up session variables
DATE=`date +%Y-%m-%d`
XML_FILE="./xml/$DATE.xml"
IMG_OUTDIR="./img"

echo "###################"
echo "Starting crawler..."
if [ -a $XML_FILE ]; then
    echo "Site already crawled today ($DATE). Skipping."
else
    # Run the crawler to get XML output
    scrapy crawl fireplace_crawler -o $XML_FILE -t xml
    echo "Crawled data extracted to: $XML_FILE"
fi

# Initialize the database (if needed) and insert extracted elements
echo -e "\nInitializing database..."
python -m db.sqlite_init
echo -e "\nStarting database insertion..."
python -m extract -i $XML_FILE
echo "Database insertion complete."

# Download images from links in XML
echo -e "\nDownloading images..."
python -m img_downloader -i $XML_FILE -o $IMG_OUTDIR
echo "Images downloaded."

# Clean up
echo -e "\nDone."
echo "###################"
