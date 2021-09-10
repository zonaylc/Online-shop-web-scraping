import scrapy
import bs4
from zalando.items import ZalandoItem, ZalandoItemInfo, LinksItem, RecordItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re


from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import json


with open("link430.json", "r") as f:
    temp_list = json.load(f)
    product_list = list(map(lambda x: x["product_urls"], temp_list))

start_urls = []
for p in product_list:
    for i in p:
        start_urls.append(i)
            
        
        
class BackupSpider(CrawlSpider):
    name = 'backup'
    allowed_domains = ['zalando.at']
    
    def start_requests(self):
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_info)
            
   

    def parse_info(self, response):                  
        record = RecordItem()
        helper = response.xpath('//span[@class="u-6V88 ka2E9k uMhVZi FxZV-M z-oVg8 pVrzNP zN9KaA"]/text()').extract()
        counter = 0  
        
        url_index = start_urls.index(response.url)
        print("Link-Index:", url_index)
        
        for info in helper:
            driverpath = r"C:\Users\smile\zalando\chromedriver\chromedriver.exe"
            counter += 1
            
            record['crwal_times'] = counter
            record['link_page'] = url_index
            yield record
            
            x = re.search("^Unser Model.", info)
            if x:
                print("水啦嘎洽!")
                               
                item = ZalandoItemInfo()
                item['item_id'] = '430L'+ str(url_index) +'I' + f'{counter:07}'
                item['brand'] = response.xpath('//h3[@class="OEhtt9 ka2E9k uMhVZi uc9Eq5 pVrzNP _5Yd-hZ"]/text()').extract()
                item['product_url'] = response.url
                item['product_name'] = response.xpath('//h1[@class="OEhtt9 ka2E9k uMhVZi z-oVg8 pVrzNP w5w9i_ _1PY7tW _9YcI4f"]/text()').extract()
                item['fitting_info'] = helper

                item['imgs'] = response.xpath('//li[@class="LiPgRT DlJ4rT hPWzFB"]//img/@src').getall()
                

                driver = webdriver.Chrome(executable_path=driverpath)
                driver.get(response.url)
                wait = WebDriverWait(driver, 15)
                wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@id="picker-trigger"]'))).click()
                result = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//form//span//span')))
                
                temp = []
                for r in result:
                    temp.append(r.text)

                item['size_choices'] = temp
                driver.quit()
                
                driver2 = webdriver.Chrome(executable_path=driverpath)
                driver2.get(response.url)
                wait = WebDriverWait(driver2, 25)
                wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Passform"]'))).click()
                try:
                    wait.until(EC.element_to_be_clickable((By.XPATH, '//button//span[text()="Größentabelle"]'))).click()
                except:
                    driver2.quit()
                    
                table_head = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//table//thead')))
                table_body = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//table//tbody')))

                item['table_head'] = []

                for h in table_head:
                    item['table_head'].append(h.text)

                item['size_chart'] = table_body[0].text
                item['measurement_chart'] =  table_body[1].text
                        
                driver2.quit()
                
                yield item
                print(counter)             
            
            else:
                print("媽的垃圾!")
                

