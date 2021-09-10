# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZalandoItem(scrapy.Item):

    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()

class ZalandoItemInfo(scrapy.Item):
    item_id = scrapy.Field()
    product_name = scrapy.Field()
    product_url = scrapy.Field()
    brand = scrapy.Field()
    size_choices = scrapy.Field()
    fitting_info = scrapy.Field()
    imgs = scrapy.Field()
    table_head = scrapy.Field()
    size_chart = scrapy.Field()
    measurement_chart = scrapy.Field()

    
class LinksItem(scrapy.Item):

    product_urls = scrapy.Field()

    
class RecordItem(scrapy.Item):
#     count = scrapy.Field()
    link = scrapy.Field()