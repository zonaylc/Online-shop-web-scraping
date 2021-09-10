import scrapy
import bs4
from zalando.items import ZalandoItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import json


with open("link430.json", "r") as f:
    temp_list = json.load(f)
    product_list = list(map(lambda x: x["product_urls"], temp_list))

start_urls = []
for p in product_list:
    for i in p:
        start_urls.append(i)
            
        
        
class PhotoSpider(CrawlSpider):
    name = 'photo'
    allowed_domains = ['zalando.at']
    
    def start_requests(self):
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_info)
            
   

    def parse_info(self, response):                  
        helper = response.xpath('//span[@class="u-6V88 ka2E9k uMhVZi FxZV-M z-oVg8 pVrzNP zN9KaA"]/text()').extract()
        counter = 0  
        
        url_index = start_urls.index(response.url)
        print("Link-Index:", url_index)
        
        for info in helper:
            counter += 1
            
            
            x = re.search("^Unser Model.", info)
            if x:
                print("水啦!")
                               
                item = ZalandoItem()
                item['image_urls'] = response.xpath('//li[@class="LiPgRT DlJ4rT hPWzFB"]//img/@src').extract() 
                yield item
            
            else:
                print("媽的垃圾!")
                

