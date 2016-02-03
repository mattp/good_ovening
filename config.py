#!/usr/bin/python

### Configuration for good_ovening package ###

# XPATH for image sources in the data XML
IMG_SRC_XPATH = "./item/images/value/src"

### Configuration for good_ovening.db package ###

# Database names
DB_PATH = "./db/good_ovening.db"
LISTINGS_TABLE = "listings"

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
FIREPLACE_WORDS = ["ovn", "peis", "vedfyring", "vedovn", "peisovn", "ildsted"]
