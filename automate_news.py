from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import time as time
import pandas as pd


#website initializations
chromedriver_autoinstaller.install()
driver = webdriver.Chrome()
options = Options()
options.add_argument("--headless")


#-----------------WEBSITES-----------------#
list_of_websites = {
    'vnexpress': {
        'link': 'https://vnexpress.net/',
        'xpath': '//h3[@class="title-news"]/a'
    },
    
    'zing': {
        'link': 'https://znews.vn/',
        'xpath': '//p[@class="article-title"]/a'
    },
}

#-----------------FUNCTIONS-----------------#
def extract_news_list(list_of_website: dict):
    for website in list_of_website:
        driver.get(list_of_website[website]['link'])
        xpath = list_of_website[website]['xpath']
        elements = driver.find_elements(By.XPATH, xpath)
        
        title = []
        link = []
        for element in elements:
            title.append(element.text)
            link.append(element.get_attribute('href'))
            
        my_dict = {'title': title, 'link': link}
        df = pd.DataFrame(my_dict)
        df.to_csv(f'{website}.csv', index=False)
        print(f'Extracted {website} successfully')
    driver.quit()  
    

#-----------------MAIN-----------------#
extract_news_list(list_of_websites)