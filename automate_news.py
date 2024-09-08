#__author__ =NGUYEN
#__IMPORT LIBRARIES__#
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

import schedule
import time as time
import pandas as pd
import platform
import json

#_________________SETUP INITIALIZATIONS_________________#

OS_NAME = platform.system()
if OS_NAME == 'Darwin':
    options = Options()
    options.add_argument("--headless")
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(options=options)
elif OS_NAME == 'Linux':
    options = Options()
    options.add_argument("start-maximized") # open Browser in maximized mode
    options.add_argument("disable-infobars") # disabling infobars
    options.add_argument("--disable-extensions") # disabling extensions
    options.add_argument("--disable-gpu") # applicable to windows os only
    options.add_argument("--disable-dev-shm-usage") # overcome limited resource problems
    options.add_argument("--no-sandbox") # Bypass OS security model
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    service = Service('/usr/lib/chromium-browser/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)


#-----------------SETUP DATABASE-----------------#
with open('websites.json', 'r') as json_file:
    list_of_websites = json.load(json_file)


#-----------------FUNCTIONS-----------------#
def extract_news_list(list_of_website: dict):
    print("Start extracting news ...")
    for website in list_of_website:
        driver.get(list_of_website[website]['link'])
        xpath = list_of_website[website]['xpath']
        elements = driver.find_elements(By.XPATH, xpath)
        
        title = []
        link = []
        for element in elements:
            title.append(element.text if element.text != '' else 'No title')
            link.append(element.get_attribute('href'))
            
        my_dict = {'title': title, 'link': link}
        df = pd.DataFrame(my_dict)
        df.to_csv(f'csv_folder/{website}.csv', index=False)
        print(f'Extracted {website} successfully')
    driver.quit()  
    

#-----------------MAIN-----------------#
# schedule.every(10).minutes.do(extract_news_list, list_of_websites)
# while True:
#     print(
#         "The program is running, it will extract news every 30 minutes"
#     )
#     extract_news_list(list_of_websites)
#     time.sleep(1800)
extract_news_list(list_of_websites)
