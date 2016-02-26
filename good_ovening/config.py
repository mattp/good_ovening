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

# Migration data
LISTINGS_SCHEMA_001 = OrderedDict([
    ("ad_id", "INTEGER PRIMARY KEY"),
    ("ad_link", "VARCHAR(250)"),
    ("ref_link", "VARCHAR(250)"),
    ("oven_type", "VARCHAR(20)"),
    ("lat", "VARCHAR(10)"),
    ("lng", "VARCHAR(10)")])
LISTINGS_SCHEMA_002 = OrderedDict([
    ("ad_id", "INTEGER PRIMARY KEY"),
    ("ad_link", "VARCHAR(250)"),
    ("origin_page", "VARCHAR(30)"),
    ("oven_type", "VARCHAR(20)"),
    ("lat", "VARCHAR(10)"),
    ("lng", "VARCHAR(10)")])
COLUMN_UPDATES = {"ref_link":"origin_page"}
VERSION_SCHEMAS = {"0.0.1":[LISTINGS_SCHEMA_001], "0.0.2":[LISTINGS_SCHEMA_002]}

# Database table schemas
LISTINGS_SCHEMA = LISTINGS_SCHEMA_002

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

# Known words for fireplace/oven (with priority values)
FIREPLACE_WORDS = {"ovn":1, "peis":2, "vedfyring":2,
                   "vedovn":2, "peisovn":2, "ildsted":2}
FIREPLACE_MODIFIERS = ["åpen", "ny"]
