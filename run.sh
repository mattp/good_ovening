#!/bin/bash

# Run the crawler to get XML output
echo "Starting crawler..."
scrapy crawl fireplace_crawler -o data.xml -t xml > log.txt
echo "Crawled data extracted to: './data.xml'"

# Initialize the database (if needed) and insert extracted elements
echo "Starting database insertion..."
python -m db.sqlite_init
echo "Database insertion complete."

# Download images from links in XML

# Clean up

