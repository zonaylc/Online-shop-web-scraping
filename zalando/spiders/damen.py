# -*- coding: utf-8 -*-
# Import relevant libraries for Scrapy
import scrapy
import bs4
from zalando.items import ZalandoItem, ZalandoItemInfo, LinksItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re

# Import relevant libararies for Selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from logzero import logger, logfile
import json

        
# Define the spider
class DamenSpider(CrawlSpider):    
    name = 'damen'
    allowed_domains = ['zalando.at']
    

    def start_requests(self):
        start_urls = ["https://www.zalando.at/oysho-triangel-bh-beige-oy181a0pa-b11.html",
                     "https://www.zalando.at/pullandbear-strickjacke-beige-puc21i0e2-b11.html",
                     "https://www.zalando.at/nike-performance-sport-bh-bronze-eclipsesmokey-mauve-n1241i0b7-g11.html",
                     "https://www.zalando.at/pullandbear-shorts-mottled-light-blue-puc21s07x-k11.html",
                     "https://www.zalando.at/oysho-satin-mit-spitze-nachthemd-mauve-oy181p0ek-i11.html",
                     "https://www.zalando.at/adidas-performance-crew-ardy-sweatshirt-black-ad541g0fv-q11.html",
                    "https://www.zalando.at/adidas-originals-ryv-crop-top-t-shirt-basic-white-ad121d0x2-a11.html",
                     "https://www.zalando.at/adidas-performance-3-stripe-tee-funktionsshirt-khaki-ad541d1iz-n11.html"]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_info)


    def parse_info(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
 
            
        item = ZalandoItemInfo()

        helper = response.xpath('//span[@class="u-6V88 ka2E9k uMhVZi FxZV-M z-oVg8 pVrzNP zN9KaA"]/text()').extract()
        counter = 0  #count how many products are valid and be kept

            
        for info in helper:
            x = re.search("^Unser Model.", info)
            if x:
                print("Match!!!")

                item['brand'] = response.xpath('//h3[@class="OEhtt9 ka2E9k uMhVZi uc9Eq5 pVrzNP _5Yd-hZ"]/text()').extract()
                item['product_name'] = response.xpath('//h1[@class="OEhtt9 ka2E9k uMhVZi z-oVg8 pVrzNP w5w9i_ _1PY7tW _9YcI4f"]/text()').extract()
                item['fitting_info'] = helper

                
                item['imgs'] = response.xpath('//li[@class="LiPgRT DlJ4rT hPWzFB"]//img/@src').getall()
                counter += 1

            else:
                    print("Not match!")  

            yield item
        
        
        logger.info(f"Total prodcuts: {counter}")
        logger.info(response.url)


