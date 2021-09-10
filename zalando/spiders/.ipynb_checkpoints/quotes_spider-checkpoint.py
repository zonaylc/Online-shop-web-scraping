import scrapy
from scrapy.selector import Selector
from zalando.items import ZalandoItem, ZalandoItemInfo
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logzero import logfile, logger


# Initialize the webdriver
driverpath = r"C:\Users\smile\zalando\chromedriver\chromedriver.exe"


class QuotesSpider(CrawlSpider):
    name = "quotes"
    logfile("quotes_spider.log", maxBytes=1e6, backupCount=3)
    allowed_domains = ['zalando.at']
    start_urls = ["https://www.zalando.at/bekleidung/"] 
    
    rules = (Rule(LinkExtractor(allow="/bekleidung/", restrict_xpaths='//a[@class="cat_link-8qswi"]'), callback="parse", follow=True),
        Rule(LinkExtractor(allow="/levis", deny='/outfits/', restrict_xpaths='//article[@class="_0mW-4D _0xLoFW JT3_zV mo6ZnF jtKZOh _78xIQ-"]'),callback="parse", follow=True),)  

        
    def parse(self, response):
#         driver = webdriver.Chrome()  # To open a new browser window and navigate it
        # Use headless option to not open a new browser window
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        desired_capabilities = options.to_capabilities()
        driver = webdriver.Chrome(executable_path=driverpath, desired_capabilities=desired_capabilities)
        
        driver.get("https://www.zalando.at/bekleidung/")
        
        # Implicit wait
        driver.implicitly_wait(10)
        
        # Explicit wait
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "kMvGAR _6-WsK3 Md_Vex Nk_Omi _MmCDa to_CKO _0xLoFW FCIprz NN8L-8 _7Cm1F9 ka2E9k uMhVZi FxZV-M RzUmIb LyRfpJ heRAwu K82if3 heWLCX mo6ZnF")))
        countries = driver.find_elements_by_class_name("kMvGAR _6-WsK3 Md_Vex Nk_Omi _MmCDa to_CKO _0xLoFW FCIprz NN8L-8 _7Cm1F9 ka2E9k uMhVZi FxZV-M RzUmIb LyRfpJ heRAwu K82if3 heWLCX mo6ZnF")
#         zaI4jo JT3_zV _0xLoFW _78xIQ- EJ4MLB
        countries_count = 0
        # Using Scrapy's yield to store output instead of explicitly writing to a JSON file
        for country in countries:
            yield {
                        "country": country.text,
                    }
            countries_count += 1
            driver.quit()
            logger.info(f"Total number of Countries in openaq.org: {countries_count}")
            
            
#         page = response.url.split("/")[-2]
#         filename = f'quotes-{page}.html'
#         with open(filename, 'wb') as f:
#             f.write(response.body)
#         self.log(f'Saved file {filename}')

#         Selector(text=body).xpath('//span/text()').get()


# <button aria-label="" class="kMvGAR _6-WsK3 Md_Vex Nk_Omi _MmCDa to_CKO _0xLoFW FCIprz NN8L-8 _7Cm1F9 ka2E9k uMhVZi FxZV-M RzUmIb LyRfpJ heRAwu K82if3 heWLCX mo6ZnF" type="button" aria-haspopup="true" aria-expanded="false" tabindex="0" id="picker-trigger"><span class="lRlpGv Uxq3DH QylWsg rp08yg JCuRr_ z-oVg8 _7Cm1F9 ka2E9k uMhVZi FxZV-M"><span class="_7Cm1F9 ka2E9k uMhVZi FxZV-M z-oVg8 weHhRC">Bitte Größe wählen</span></span><svg class="zds-icon RC794g X9n9TI DlJ4rT _9l1hln DlJ4rT gtYS_z nXkCf3 H3jvU7" height="1em" width="1em" focusable="false" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M2.86 7.48c.3-.3.77-.3 1.06 0l7.55 7.55c.3.29.77.29 1.06 0l7.55-7.55a.75.75 0 111.06 1.06l-7.55 7.55c-.88.87-2.3.87-3.18 0L2.86 8.54a.75.75 0 010-1.06z"></path></svg></button>