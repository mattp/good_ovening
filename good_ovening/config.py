#!/usr/bin/python
# -- coding: utf-8 --
from collections import OrderedDict

### Configuration for good_ovening package ###

# XPATH for image sources in the data XML
IMG_SRC_XPATH = "./item/images/value/src"

### Configuration for good_ovening.db package ###

# Database names
DB_PATH = "good_ovening/db/good_ovening.db"
LISTINGS_TABLE = "listings"

# Database table schemas
LISTINGS_SCHEMA = OrderedDict([
    ("ad_id", "INTEGER PRIMARY KEY"),
    ("ad_link", "VARCHAR(250)"),
    ("ref_link", "VARCHAR(250)"),
    ("oven_type", "VARCHAR(20)"),
    ("lat", "VARCHAR(10)"),
    ("lng", "VARCHAR(10)")])

# XML element keys
REF_LINK_KEY = "ref_link"
AD_LINK_KEY = "ad_link"
AD_ID_KEY = "ad_id"
LAT_KEY = "lat"
LNG_KEY = "lng"
DESCS_KEY = "descriptions"
IMGS_KEY = "images"

# Other keys
OVEN_TYPE_KEY = "oven_type"

# Known words for fireplace/oven
FIREPLACE_WORDS = ["ovn", "peis", u"åpen peis", "vedfyring", "vedovn",
                   "ny vedovn", "peisovn", "ildsted"]
