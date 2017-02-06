#!/usr/bin/python
# -- coding: utf-8 --
import sys
import re
import string
import good_ovening.config as conf
from optparse import OptionParser
from xml_parser import OvenXMLParser
from good_ovening.db.database_row import OvenDatabaseRow
from good_ovening.db.database import SQLiteDatabase

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
        origin_page = extract_origin_page(item.find(conf.REF_LINK_KEY).text.split("?")[0])
        db_row.set_origin_page(origin_page)
        descriptions = item.find(conf.DESCS_KEY).findall("value")
        headers = [u'%s' % d.find("header").text for d in descriptions]
        data = ["\n".join([u'%s' % d.text for d in desc.find("data").findall("value")])
                for desc in descriptions]
        desc_text = "\n".join(["%s\n%s" % (h, d) for h, d in zip(headers, data)])
        db_row.set_oven_type(extract_oven_type(desc_text))
        db_row.set_lat(item.find(conf.LAT_KEY).text)
        db_row.set_lng(item.find(conf.LNG_KEY).text)
        overview_details = item.find(conf.OVERVIEW_DETAILS_KEY)
        if overview_details not None:
            overview_details = []
        floor_size = extract_floor_size(overview_details)
        db_row.set_floor_size(floor_size)
        yield db_row

def extract_origin_page(ref_link):
    """Get the name of the origin page from the reference link """
    sani_link = ref_link.replace("http://", "")
    sani_link = re.sub(r"\?.*", "", sani_link)
    link_split = sani_link.split('/')
    if "search.html" in link_split:
        origin_page = link_split[link_split.index("search.html") - 1]
    else:
        origin_page = "NONE"
    return origin_page
        
def extract_oven_type(description):
    """Given a list of relevant descriptions for an ad listing, attempt to determine the
    correct oven type"""

    # Sanitize the input text
    sani_desc = description.lstrip().rstrip().lower()
    punc_regex = re.compile('[%s]' % re.escape(string.punctuation))
    sani_desc = punc_regex.sub(' ', sani_desc)
    
    # Find the correct oven type
    max_count = 1
    max_priority = 0
    max_word = "none"
    for oven_word, priority in conf.FIREPLACE_WORDS.iteritems():
        oven_regex = r'\b%s\b' % oven_word
        oven_count = len(re.findall(oven_regex, sani_desc))
        update = (priority > max_priority and oven_count > 0) or \
                 (priority == max_priority and oven_count > max_count)
        if update:
            max_count = oven_count
            max_priority = priority
            max_word = oven_word
            
    # Check if any modifiers appear for that word
    if max_word != "none":
        for modifier in conf.FIREPLACE_MODIFIERS:
            mod_regex = r'%s\W%s' % (modifier, max_word)
            if re.search(mod_regex, sani_desc):
                max_word = "%s %s" % (modifier, max_word)
    return max_word    

def extract_floor_size(overview_details):
    """Get the floor size from the list of overview items """
    for od in overview_details:
        overview_item_key = unicode(od[0].text.lower())
        if (overview_item_key == conf.FLOOR_SIZE_OVERVIEW_ITEM):
            floor_size = od[1].text.strip().split(' ')[0]
            return floor_size
    
def insert_database_rows(rows, db_name):
    """Insert any meaningful data from the given list of DatabaseRow
    objects into the database """
    db = SQLiteDatabase.get_instance()
    for row in rows:
        values = ",".join([row.get_ad_id(), "'%s'" % row.get_ad_link(),
                           "'%s'" % row.get_origin_page(),
                           "'%s'" % row.get_oven_type(),
                           "'%s'" % row.get_lat(),
                           "'%s'" % row.get_lng(),
                           "'%s'" % row.get_floor_size()])
        query = "REPLACE INTO %s VALUES(%s)" % (conf.LISTINGS_TABLE, values)
        db.execute_query(db_name, query)
        
if __name__=="__main__":

    # Handle command-line arguments
    (opts, args) = parser.parse_args()
    if not opts.input_file:
        parser.error("Input file required")

    # Extract database items from the XML
    db_rows = extract_database_rows(opts.input_file)

    # Insert database rows
    insert_database_rows(db_rows, conf.DB_PATH)
    
