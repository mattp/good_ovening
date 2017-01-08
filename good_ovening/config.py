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
class VersionConfig(object):

    def __init__(self, version):
        self.version = version
        self.schemas = {}

    def get_version(self):
        """Return the schema version string """
        return self.version    

    def add_schema_dict(self, schema_name, schema_dict):
        """Add an OrderedDict representing a schema with the given name. """
        assert type(schema_dict) == OrderedDict, "Schema must be type OrderedDict, " \
            "found '%r'" % type(schema_dict)
        self.schemas[schema_name] = schema_dict

    def get_schema_dict(self, schema_name):
        """Return the schema dict representing the given schema name (if it exists) """
        assert schema_name in self.schemas, "Schema %r not present in schemas" % schema_name
        return self.schemas[schema_name]
        
    def schema_name_gen(self):
        """Yield all schema names for this VersionConfig """
        for schema_name in self.schemas:
            yield schema_name

    def has_schema(self, schema_name):
        """Whether or not the given schema name is present in this VersionConfig """
        return schema_name in self.schemas
    
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
VERSION_CONFIG_001 = VersionConfig("0.0.1")
VERSION_CONFIG_001.add_schema_dict("listings", LISTINGS_SCHEMA_001)
VERSION_CONFIG_002 = VersionConfig("0.0.2")
VERSION_CONFIG_001.add_schema_dict("listings", LISTINGS_SCHEMA_002)
VERSIONS_CONFIGS = {"0.0.1":VERSION_CONFIG_001, "0.0.2":VERSION_CONFIG_002}
# VERSION_SCHEMAS = {"0.0.1":OrderedDict([("listings", LISTINGS_SCHEMA_001)]),
#                   "0.0.2":OrderedDict([("listings", LISTINGS_SCHEMA_002)])}


# Current database table schemas
LISTINGS_SCHEMA = LISTINGS_SCHEMA_002

# XML element keys
REF_LINK_KEY = "ref_link"
ORIGIN_PAGE_KEY = "origin_page"
AD_LINK_KEY = "ad_link"
AD_ID_KEY = "ad_id"
LAT_KEY = "lat"
LNG_KEY = "lng"
DESCS_KEY = "descriptions"
IMGS_KEY = "images"

# Other keys
OVEN_TYPE_KEY = "oven_type"

# Known words for fireplace/oven (with priority values)
FIREPLACE_WORDS = {"ovn":1, "peis":2, "vedfyring":2, "vedovn":2, "peisovn":2,
                   "ildsted":2, "stålpeis":2, "kamin":2, "vedkamin":2, "ovner":2,
                   "klebersteinovn":2, "vedfyr":2, "elementpeis":2, "tegnsteinspeis":2,
                   "pelletsovn":2, "rundbrenner":2, "ildsteder":2, "koksovn":2,
                   "støpejernsovn":2, "kakkelovn":2, "vedpeis":2, "peiser":2,
                   "rundovn":2, "fjernvarme":2, "varmepumpe":2, "sentralvarmeanlegg":2}

FIREPLACE_MODIFIERS = ["moderne", "eldre", "nydelig", "åpen", "ny", "nyere", "murt"]
