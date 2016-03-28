#!/usr/bin/python
import re
import string
import urlparse
import good_ovening.fireplace_crawler.spider_config as sconf
import good_ovening.config as conf
from good_ovening.fireplace_crawler.items import FireplaceCrawlerItem
from scrapy.spiders import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request

class FireSpider(Spider):

    # Already seen search pages
    crawled_pages = []
    
    # Configure the name and domain of the Spider
    name = sconf.NAME
    allowed_domains = sconf.ALLOWED_DOMAINS
    start_urls = sconf.START_URLS
    # start_urls = ["http://m.finn.no/r/feriehus-hytteutleie/search.html?location=0.25002&location=1.25002.20001"]
    
    def parse(self, response):
        """Defer to the correct function for handling the page depending on it's type """
        search_page = re.search(sconf.SEARCH_URL, response.url)
        ad_page = re.search(sconf.ADID_REGEX, response.url)
        if search_page:
            return self.parse_search_page(response)
        elif ad_page:
            return self.parse_listing(response)
        else:
            return None

    def parse_browse_page(self, response):
        """Crawl all search page links on the browse page """
        # Get the links
        hxs = Selector(response)
        search_links = hxs.xpath(sconf.OUTER_SEARCH_LINK_XPATH)

        # Make a new Request for each link found on the browse page
        for search_link in search_links:
            print("CRAWLING BROWSE PAGE: %r" % search_link)
            yield Request(urlparse.urljoin(response.url, search_link),
                          callback=self.parse_search_page)
        
    def parse_search_page(self, response):
        """Recursively crawl from the starting URL and add all links"""        
        # Get the links
        print("CRAWLING SEARCH PAGE: %r" % response.url)
        hxs = Selector(response)
        ad_links = hxs.xpath(sconf.AD_LINK_XPATH).extract()
                
        # Make a new Request for each link found on the starting page
        for ad_link in ad_links:
            item = FireplaceCrawlerItem()
            item[conf.REF_LINK_KEY] = response.url
            item[conf.AD_LINK_KEY] = urlparse.urljoin(response.url, ad_link)
            yield Request(urlparse.urljoin(response.url, ad_link),
                          meta={'item':item}, callback=self.parse_listing)

        # Rerun for NEXT pages from the start
        search_links = hxs.xpath(sconf.INNER_SEARCH_LINK_XPATH).extract()
        for search_link in search_links:
            if ("page=" in search_link) and not (search_link in self.crawled_pages):
                self.crawled_pages.append(search_link)
                yield Request(urlparse.urljoin(response.url, search_link), callback=self.parse)
            
    def parse_listing(self, response):
        """Parse the desired data from the links found on the start page"""

        # Re-get the item and create a corresponding Selector
        if 'item' in response.request.meta:
            item = response.request.meta['item']
        else:
            item = {}

        hxs = Selector(response)
        print("CRAWLING AD PAGE: %r" % response.url)

        # Get the ad id from the URL
        item[conf.AD_ID_KEY] = re.search(sconf.ADID_REGEX, response.url).group(0).split('=')[1]
        
        # Get the geo coordinates from the map-link URL
        item[conf.LAT_KEY], item[conf.LNG_KEY] = self._parse_geo_coordinates(hxs)
                    
        # Get the header and data items from the descriptions
        item[conf.DESCS_KEY] = self._filter_descriptions(self._parse_descriptions(hxs))

        # Get the image sources and labels
        item[conf.IMGS_KEY] = self._filter_images(self._parse_images(hxs))
        
        yield item


    def _parse_geo_coordinates(self, hxs):
        """Parse the geographical coordinates (lat,lng) using the given Selector"""
        try:
            maplink = hxs.xpath(sconf.MAP_LINK_XPATH).extract()[0]
            print("MAP LINK: %s" % maplink)
            lat = re.search(sconf.GEO_REGEX % "lat", maplink).group(0).split('=')[1]
            print("LATITUDE: %s" % lat)
            lng = re.search(sconf.GEO_REGEX % "lng", maplink).group(0).split('=')[1]
            print("LONGITUDE: %s" % lng)
        except:
            lat = "Unavailable"
            lng = "Unavailable"
        return lat, lng
        
    def _parse_descriptions(self, hxs):
        """Parse the listing descriptions (headers and content) using the
        given Selector """
        listing_descs = hxs.xpath(sconf.DESC_BASE_XPATH) + hxs.xpath(sconf.DESC_BASE_XPATH_ALT)
        descs = []
        desc_append = descs.append
        for lds in listing_descs:
            try:
                raw_header = lds.xpath(sconf.DESC_HEADER_XPATH).extract()
                if len(raw_header) > 0:
                    header = raw_header[0].lstrip().rstrip()
                else:
                    header = "NOT FOUND"
                raw_pars = lds.xpath(sconf.DESC_PAR_XPATH).extract()
                data = [p.lstrip().rstrip() for p in raw_pars]
                desc_append({"header":header, "data":data})
            except Exception, e:
                print("Couldn't parse listing description")
                print(e)
        return descs

    def _parse_images(self, hxs):
        """Parse the list of images to get sources and labels """
        image_objs = hxs.xpath(sconf.IMAGES_BASE_XPATH)
        images = []
        images_append = images.append
        for img_obj in image_objs:
            img_src = img_obj.xpath(sconf.IMAGES_SRC_XPATH).extract()[0]
            img_label = img_obj.xpath(sconf.IMAGES_LABEL_XPATH).extract()[0]
            images_append({"src":img_src, "label":img_label})
        return images

    def _filter_descriptions(self, descriptions):
        """Filter descriptions for fireplace words in the content """
        return filter(lambda d: self._has_fireplace_words("\n".join(d['data'])), descriptions)

    def _filter_images(self, images):
        """Filter images for fireplace words in the label """
        return filter(lambda d: self._has_fireplace_words(d['label']), images)
    
    def _has_fireplace_words(self, text):
        """Determine if the provided text contains any of the known fireplace words """
        sani_text = text.lstrip().rstrip().lower()
        punc_regex = re.compile('[%s]' % re.escape(string.punctuation))
        sani_text = punc_regex.sub(' ', sani_text)
        for fp_word in conf.FIREPLACE_WORDS:
            m = re.search(" %s " % fp_word, sani_text)
            if m:
                return True
        return False
