#!/usr/bin/python
import sys
from optparse import OptionParser
from xml_parser import OvenXMLParser
from db.database_row import OvenDatabaseRow

parser = OptionParser()
parser.add_option("-i", "--input", dest="input_file", type="string",
                  help="[Required] Path to input data file in XML format")

def extract_database_rows(xml_filepath):
    """Extract the meaningful data from the given XML file, to prepare it
    for database insertion """
    
    # Initialize an XML parser with the given input file
    oven_xml_parser = OvenXMLParser()
    oven_xml_parser.load_file(xml_filepath)
    assert oven_xml_parser.xml_loaded(), "XML not loaded, extraction could not be completed."

    for item in oven_xml_parser.item_generator():
        # Initialize the container for the database row and yield
        db_row = OvenDatabaseRow(item)
        yield db_row
        

if __name__=="__main__":

    # Handle command-line arguments
    (opts, args) = parser.parse_args()
    if not opts.input_file:
        parser.error("Input file required")

    # Extract database items from the XML
    db_rows = extract_database_rows(opts.input_file)

    # Insert database rows
    insert_
    
