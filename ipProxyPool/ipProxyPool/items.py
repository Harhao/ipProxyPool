# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Item,Field


class IpproxypoolItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ip_addr=Field()
    port=Field()
    wholeIP=Field()
    location=Field()
    type=Field()
    netType=Field()
    speed=Field()
    connTime=Field()
    aliveTime=Field()
    verifyTime=Field()
