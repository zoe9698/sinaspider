# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nickname = scrapy.Field()
    txt = scrapy.Field()
    date = scrapy.Field()
    device = scrapy.Field()
    favorate_count = scrapy.Field()
    forward_count = scrapy.Field()
    comment_count = scrapy.Field()
    like_count = scrapy.Field()
