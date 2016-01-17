#!/usr/bin/python
import re
import string
import urlparse
import fireplace_crawler.spider_config as conf
from fireplace_crawler.items import FireplaceCrawlerItem
from scrapy.spiders import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request

class FireSpider(Spider):

    # Already seen search pages
    crawled_pages = []
    
    # Configure the name and domain of the Spider
    name = conf.NAME
    allowed_domains = conf.ALLOWED_DOMAINS
    start_urls = conf.START_URLS
    # start_urls = ["http://m.finn.no/realestate/newbuildings/ad.html?finnkode=60494095&seg=homes&ref=fas"]
    
    def parse(self, response):
        """Recursively crawl from the starting URL and add all links"""        
        # Get the links
        hxs = Selector(response)
        ad_links = hxs.xpath(conf.AD_LINK_XPATH).extract()
        
        # Make a new Request for each link found on the starting page
        for ad_link in ad_links:
            item = FireplaceCrawlerItem()
            item['ref_link'] = response.url
            item['ad_link'] = urlparse.urljoin(response.url, ad_link)
            # "http://%s%s" % (self.allowed_domains[0], ad_link)
            yield Request(urlparse.urljoin(response.url, ad_link),
                          meta={'item':item}, callback=self.parse_listing)

        # Rerun for NEXT pages from the start
        # search_links = hxs.xpath(conf.SEARCH_LINK_XPATH).extract()
        # for search_link in search_links:
        #     if ("page=" in search_link) and not (search_link in self.crawled_pages):
        #         self.crawled_pages.append(search_link)
        #         yield Request(urlparse.urljoin(response.url, search_link), callback=self.parse)
            
    def parse_listing(self, response):
        """Parse the desired data from the links found on the start page"""

        # Re-get the item and create a corresponding Selector
        item = response.request.meta['item']
        hxs = Selector(response)

        # Get the ad id from the URL
        item['ad_id'] = re.search(conf.ADID_REGEX, response.url).group(0).split('=')[1]
        
        # Get the geo coordinates from the map-link URL
        item['lat'], item['lng'] = self._parse_geo_coordinates(hxs)
                    
        # Get the header and data items from the descriptions
        item['descriptions'] = self._filter_descriptions(self._parse_descriptions(hxs))

        # Get the image sources and labels
        item['images'] = self._filter_images(self._parse_images(hxs))
        
        yield item


    def _parse_geo_coordinates(self, hxs):
        """Parse the geographical coordinates (lat,lng) using the given Selector"""
        try:
            maplink = hxs.xpath(conf.MAP_LINK_XPATH).extract()[0]
            lat = re.search(conf.GEO_REGEX % "lat", maplink).group(0).split('=')[1]
            lng = re.search(conf.GEO_REGEX % "lng", maplink).group(0).split('=')[1]
        except:
            lat = "Unavailable"
            lng = "Unavailable"
        return lat, lng
        
    def _parse_descriptions(self, hxs):
        """Parse the listing descriptions (headers and content) using the
        given Selector """
        listing_descs = hxs.xpath(conf.DESC_BASE_XPATH)
        descs = []
        desc_append = descs.append
        for lds in listing_descs:
            try:
                raw_header = lds.xpath(conf.DESC_HEADER_XPATH).extract()[0]
                raw_pars = lds.xpath(conf.DESC_PAR_XPATH).extract()
                desc_append({"header":raw_header.lstrip().rstrip(),
                             "data":[p.lstrip().rstrip() for p in raw_pars]})
            except:
                print("Couldn't parse listing description")
        return descs

    def _parse_images(self, hxs):
        """Parse the list of images to get sources and labels """
        image_objs = hxs.xpath(conf.IMAGES_BASE_XPATH)
        images = []
        images_append = images.append
        for img_obj in image_objs:
            img_src = img_obj.xpath(conf.IMAGES_SRC_XPATH).extract()[0]
            img_label = img_obj.xpath(conf.IMAGES_LABEL_XPATH).extract()[0]
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
