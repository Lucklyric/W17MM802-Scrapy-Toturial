# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class CSStaff(scrapy.Item):
    name = scrapy.Field()
    position = scrapy.Field()
    department = scrapy.Field()
    area= scrapy.Field()
    phone= scrapy.Field()
    email= scrapy.Field()
