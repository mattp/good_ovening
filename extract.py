#!/usr/bin/python
import sys
import config as conf
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
        # Initialize the container for the database row, populate, and yield
        db_row = OvenDatabaseRow()
        db_row.set_ad_id(item.find(conf.AD_ID_KEY).text)
        db_row.set_ad_link(item.find(conf.AD_LINK_KEY).text)
        descriptions = item.find(conf.DESCS_KEY).findall("value")
        headers = [u'%s' % d.find("header").text for d in descriptions]
        data = ["\n".join([u'%s' % d.text for d in desc.find("data").findall("value")])
                for desc in descriptions]
        desc_text = "\n".join(["%s\n%s" % (h, d) for h, d in zip(headers, data)])
        db_row.set_oven_type(extract_oven_type(desc_text))
        lat = None
        lng = None
        yield db_row

def extract_oven_type(description):
    """Given a list of relevant descriptions for an ad listing, attempt to determine the
    correct oven type"""
    desc_words = [w.lower() for w in description.split()]
    print(desc_words)
    return "OVEN"
    
        
def insert_database_rows(rows):
    """Insert any meaningful data from the given list of DatabaseRow
    objects into the database """
    pass

        
if __name__=="__main__":

    # Handle command-line arguments
    (opts, args) = parser.parse_args()
    if not opts.input_file:
        parser.error("Input file required")

    # Extract database items from the XML
    db_rows = extract_database_rows(opts.input_file)

    # Insert database rows
    insert_database_row(db_rows)
    
