# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import Select
 
    
driverpath = r"C:\Users\smile\zalando\chromedriver\chromedriver.exe"

driver = webdriver.Chrome(executable_path=driverpath)
driver.get("https://www.zalando.at/diesel-umtee-randalthreepack-t-shirt-3-pack-t-shirt-basic-whitedark-blueblack-di122o0b9-a11.html")
 
# 抓取下拉選單元件
select = Select(driver.find_elements_by_class_name("kMvGAR _6-WsK3 Md_Vex Nk_Omi _MmCDa to_CKO _0xLoFW FCIprz NN8L-8 _7Cm1F9 ka2E9k uMhVZi FxZV-M RzUmIb LyRfpJ heRAwu K82if3 heWLCX mo6ZnF"))