# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FireplaceCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    ad_id = scrapy.Field()
    ref_link = scrapy.Field()
    ad_link = scrapy.Field()
    descriptions = scrapy.Field()
    images = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    overview_details = scrapy.Field()
