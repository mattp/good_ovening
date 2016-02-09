#!/usr/bin/python

# Required crawler configuration items
NAME = "fireplace_crawler"
ALLOWED_DOMAINS = ["m.finn.no"]
START_URLS = ["http://m.finn.no/realestate/homes/search.html"]

# Listing headers to keep content for
COLLECT_HEADERS = ["oppvarming"]

# Crawler search XPaths 
SEARCH_LINK_XPATH = '//span[@class="hidelt768"]/a/@href'
AD_LINK_XPATH = '//div[@class="flex-unit result-item"]/a/@href'

# Listing scraper XPaths
AD_ID_XPATH = '//span/@data-adid'
IMAGES_BASE_XPATH = '//div[@class="hidden"]/img'
IMAGES_SRC_XPATH = '@data-src'
IMAGES_LABEL_XPATH = '@aria-label'
MAP_LINK_XPATH = '//p[@class="maplink"]/a/@href'
DESC_BASE_XPATH = '//div[@class="mbl object-description"]'
DESC_HEADER_XPATH = 'h2/text()'
DESC_PAR_XPATH = 'p/text()'

# Regex for finding lat./lng. coordinates from link
GEO_REGEX = "%s=[0-9]+.[0-9]+"

# Regex for finding ad id from link
ADID_REGEX = "finnkode=[0-9]+"

