import scrapy
import bs4
from zalando.items import RecordItem
from scrapy.spiders import CrawlSpider
import re


from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from logzero import logger, logfile
import json


with open("link230.json", "r") as f:
    temp_list = json.load(f)
    product_list = list(map(lambda x: x["product_urls"], temp_list))

start_urls = []
for p in product_list:
    for i in p:
        start_urls.append(i)
    
    
class ValidsSpider(CrawlSpider):
    name = 'valids'
    allowed_domains = ['zalando.at']

    
    def start_requests(self):
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_info)
            
   

    def parse_info(self, response):

        helper = response.xpath('//span[@class="u-6V88 ka2E9k uMhVZi FxZV-M z-oVg8 pVrzNP zN9KaA"]/text()').extract()
            
        for info in helper:

            x = re.search("^Unser Model.", info)
            if x:
                print("水啦嘎洽!")
                
                item = RecordItem()
                item['link'] = response.url
                yield item

            
 

