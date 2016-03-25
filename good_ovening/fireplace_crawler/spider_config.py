#!/usr/bin/python

# Required crawler configuration items
NAME = "fireplace_crawler"
DOMAIN = "m.finn.no"
ALLOWED_DOMAINS = [DOMAIN]
START_URL_POSTFIXES = ["/realestate/homes/search.html",
                       "/realestate/newbuildings/search.html",
                       "/realestate/plots/search.html",
                       "/realestate/leisuresale/search.html",
                       "/realestate/leisureplots/search.html",
                       "http://m.finn.no/r/feriehus-hytteutleie/search.html?location=0.25002&location=1.25002.20001", # Norway only
                       "/r/feriehus-hytteutleie/search.html",
                       "/realestate/lettings/search.html",
                       "/realestate/companyforsale/search.html"]
START_URLS = ["http://%s%s" % (DOMAIN, postfix) for postfix in START_URL_POSTFIXES]

# Listing headers to keep content for
COLLECT_HEADERS = ["oppvarming"]

# Regex for finding things from links
BROWSE_URL = "/realestate/browse.html"
SEARCH_URL = "/search.html"
ADID_REGEX = "finnkode=[0-9]+"

# Crawler search XPaths 
OUTER_SEARCH_LINK_XPATH = '//div[@data-quicklink="%s"]/div/div/nav/div/div/ul/li/a/@href' % BROWSE_URL
INNER_SEARCH_LINK_XPATH = '//span[@class="hidelt768"]/a/@href'
AD_LINK_XPATH = '//div[@class="unit flex align-items-stretch result-item"]/a/@href'

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
GEO_REGEX = "%s=-*[0-9]+.[0-9]+"
