# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field

class AstroItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    site = Field()
    url = Field()
    spec = Field()
    idx = Field()
    product = Field()
    image_urls = Field()
    images = Field()

    counter = Field()
