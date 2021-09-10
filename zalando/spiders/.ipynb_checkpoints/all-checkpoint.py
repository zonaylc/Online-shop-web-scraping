import scrapy
import bs4
from zalando.items import ZalandoItem, ZalandoItemInfo
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
import re
import time


from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
import json


# with open("all_crawled_links.json", "r") as f:
#     start_urls = json.load(f)
            
start_urls = ["https://www.zalando.at/pullandbear-strickjacke-beige-puc21i0e2-b11.html",
            "https://www.zalando.at/nike-performance-sport-bh-bronze-eclipsesmokey-mauve-n1241i0b7-g11.html",
            "https://www.zalando.at/pullandbear-shorts-mottled-light-blue-puc21s07x-k11.html",
            "https://www.zalando.at/oysho-satin-mit-spitze-nachthemd-mauve-oy181p0ek-i11.html",
            "https://www.zalando.at/adidas-performance-crew-ardy-sweatshirt-black-ad541g0fv-q11.html",
            "https://www.zalando.at/adidas-originals-ryv-crop-top-t-shirt-basic-white-ad121d0x2-a11.html",
            "https://www.zalando.at/adidas-performance-3-stripe-tee-funktionsshirt-khaki-ad541d1iz-n11.html",
            "https://www.zalando.at/nike-sportswear-tee-crew-t-shirt-print-champagne-ni121d0ja-i11.html",
            "https://www.zalando.at/arket-bluse-white-dusty-aru21e00n-b11.html",
            "https://www.zalando.at/vero-moda-petite-vmannabelle-34-dress-freizeitkleid-honeysuckle-vm021c09t-j11.html",
             "https://www.zalando.at/hunkemoeller-short-set-nachtwaesche-set-maroon-hm181p0ew-o11.html",
             "https://www.zalando.at/stradivarius-skort-minirock-white-sth21b07i-a12.html",
             "https://www.zalando.at/edc-by-esprit-pull-on-shorts-light-khaki-ed121s06u-n11.html",
             "https://www.zalando.at/pullandbear-jeans-straight-leg-dark-blue-puc21n0ab-k11.html",
             "https://www.zalando.at/tom-tailor-denim-relaxed-shorts-deep-black-to721s02i-q11.html",
             "https://www.zalando.at/edc-by-esprit-pull-on-shorts-light-khaki-ed121s06u-n11.html",
             "https://www.zalando.at/pullandbear-mit-farblich-abgesetztem-patentmuster-top-white-puc21d1me-a11.html",
             "https://www.zalando.at/pullandbear-mit-cut-outs-freizeitkleid-white-puc21c0mf-a11.html",
             "https://www.zalando.at/nike-performance-indy-pack-bra-sport-bh-mit-leichter-stuetzkraft-blackwhite-n1241i0b4-q11.html",
             "https://www.zalando.at/nike-performance-indy-pro-bra-sport-bh-mit-leichter-stuetzkraft-plum-chalkwhitemetallic-silver-n1241i0a1-j11.html",
             "https://www.zalando.at/puma-evoknit-seamless-crop-top-pu141d0ag-c11.html"]

class AllSpider(CrawlSpider):
    name = 'all'
    allowed_domains = ['zalando.at']
    counter = 0

    
    def start_requests(self):
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_info)
            
   

    def parse_info(self, response):                  
        self.counter +=1
        driverpath = r"C:\Users\smile\zalando\chromedriver\chromedriver.exe"
        
        options = webdriver.ChromeOptions()
        ua = UserAgent()
        userAgent = ua.random
        
        options.add_argument(f'user-agent={userAgent}')      
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        
            
        url_index = start_urls.index(response.url)
        print("Link-Index:", url_index)
            
                
        item = ZalandoItemInfo()
        item['item_id'] = '230L'+ str(url_index) +'I' + f'{self.counter:05}' 
        item['brand'] = response.xpath('//h3[@class="OEhtt9 ka2E9k uMhVZi uc9Eq5 pVrzNP _5Yd-hZ"]/text()').extract()
        item['product_url'] = response.url
        item['product_name'] = response.xpath('//h1[@class="OEhtt9 ka2E9k uMhVZi z-oVg8 pVrzNP w5w9i_ _1PY7tW _9YcI4f"]/text()').extract()
        item['fitting_info'] = response.xpath('//span[@class="u-6V88 ka2E9k uMhVZi FxZV-M z-oVg8 pVrzNP zN9KaA"]/text()').extract()
        item['imgs'] = response.xpath('//li[@class="LiPgRT DlJ4rT hPWzFB"]//img/@src').getall()
                
            
        driver = webdriver.Chrome(executable_path=driverpath,options=options)
        driver.get(response.url)                
        wait = WebDriverWait(driver, 25)
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@id="picker-trigger"]'))).click()
        except Exception as e:
            print(str(e))      

        try: 
            result = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//form//span//span')))
        except Exception as e:
            print(str(e))
            
        temp = []
        for r in result:
            temp.append(r.text)
            item['size_choices'] = temp
         
        
        driver.quit()


        
        yield item         
                
        
        
        