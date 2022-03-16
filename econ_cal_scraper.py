import string
import sys
from xml.dom.minidom import Element
import requests
from bs4 import BeautifulSoup
import uuid
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from scrapy import Selector
import re

class EconCalScraper:
    def __init__(self, url= 'https://www.myfxbook.com/', tab = 'econ_calendar'):
        '''
        Accepted tab arguments: 
        (1) econ_calendar: For economic calndar
        (2) fin_calc: Financial calculator
        (3) news: General news
        (4) spread: Bid-ask spreads for selection of forex pairs
        (5) heatmap: Heatmap for cuurency movements within a given timeframe
        (6) correlation: Correlation for selection of forex pairs
        (7) sentiment: For selection of forex pairs
        '''
        self._tab = tab
        self.url = url
        op = webdriver.ChromeOptions()
        op.add_argument('--incognito')
        self.driver = Chrome(ChromeDriverManager().install(), options= op)
        self.driver.get(url)
        self.wait = WebDriverWait(self.driver, 15)
        self.wait.until(EC.element_to_be_clickable((By.ID, 'dismissGdprConsentBannerBtn'))).click()
        img_link_dict = {}
        self.link_list = []
        self.img = []
        time.sleep(1)
        self.getPage()

    def getPage(self):
        if self._tab == 'econ_calendar':
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[contains(@class, "nav navbar-nav")]/li/a[@data-gtag = "popular-economic-calendar"]'))).click()
            print('Curent name; ', __name__)
            self.popupEsc()
        elif self._tab == 'fin_cal':
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[contains(@class, "nav navbar-nav")]/li/a[@data-gtag = "popular-calculators"]'))).click()
            self.popupEsc()
        elif self._tab == 'news':
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[contains(@class, "nav navbar-nav")]/li/a[@data-gtag = "popular-news"]'))).click()
            self.popupEsc()
        elif self._tab == 'spread':
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[contains(@class, "nav navbar-nav")]/li/a[@data-gtag = "popular-spreads"]'))).click()
            self.popupEsc()
        elif self._tab == 'sentiment':
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[contains(@class, "nav navbar-nav")]/li/a[@data-gtag = "popular-outlook"]'))).click()
        elif self._tab == 'heatmap':
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[contains(@class, "nav navbar-nav")]/li/a[@data-gtag = "popular-heatmap"]'))).click()
            self.popupEsc()
        elif self._tab == 'correlation':
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[contains(@class, "nav navbar-nav")]/li/a[@data-gtag = "popular-correlation"]'))).click()
            self.popupEsc()

    def popupEsc(self):
        wait = WebDriverWait(self.driver, 15)
        time.sleep(2)
        self.driver.refresh()
        time.sleep(2)
        try: 
            wait.until(EC.element_to_be_clickable((By.ID, 'blockWebNotification'))).click()
        except:
            pass
    
    def quitScrap(self):
        time.sleep(1)
        self.driver.close()
        self.driver.quit()

    def __str__(self):
        return str(self.driver.current_url)
    
    def getImgs(self, ext = '.png'):
        print(self.driver.current_url)
        time.sleep(2)
        element = self.driver.find_elements(By.XPATH, '//img')
        img_type = re.compile(f'{ext}$')
        for i in element:
            if re.findall(img_type, i.get_attribute('src')) != []:
                print(i.get_attribute('src'))
                self.img.append(i.get_attribute('src'))
        self.quitScrap()
        print(self.img)
        return self.img

    def addUUID(self):
        uuid_ls = [uuid.uuid4() for i in range(len(self.df))]
        print(uuid_ls)
        self.df['UUID'] = uuid_ls

    def getLinks(self):
        print('Current Page URL: ',self.driver.current_url)
        time.sleep(5)
        element = self.driver.find_elements(By.XPATH, '//a')
        print(self.driver.title)
        time.sleep(2)
        fxsitelinks = re.compile(r'https://www.myfxbook.com/.*')
        for i in element:
            if (i.get_attribute('href') is not None):
                if re.findall(fxsitelinks, i.get_attribute('href')) != []:
                    print(i.get_attribute('href'))
                    self.link_list.append(i.get_attribute('href'))
        time.sleep(5)
        self.quitScrap()
        return self.link_list
    
    @property
    def tab(self):
        return self.tab

    @tab.setter
    def tab(self, new_val):
        self._tab = new_val
    
    @classmethod
    def allLinks(cls):
        time.sleep(5)
        link_list = []
        for i in ['econ_calendar','fin_cal','news','spread','sentiment','heatmap','correlation']:
            new_inst = cls(url = 'https://www.myfxbook.com/', tab = i)
            new_inst.getLinks()
            link_list.extend(new_inst.link_list)
            time.sleep(5)
        link_list = set(link_list)
        print(len(link_list))
        print(link_list)
        return link_list
    
    @classmethod
    def reset(cls, new_tb, url = 'https://www.myfxbook.com/'):
        cls.inst = None
        cls.inst = EconCalScraper(url= url, tab= new_tb)
        return cls.inst


#for i in ['econ_calendar', 'fin_cal', 'news', 'spread', 'sentiment', 'heatmap', 'correlation']:    
#    scraper = EconCalScraper(tab=i)
#    time.sleep(10)
#    scraper.quitScrap()
#    print('Done for: ', i)
#    time.sleep(3)

'''
scraper = EconCalScraper(tab='econ_calendar')
scraper.getEvent()
scraper.quitScrap()

print(scraper.df.head())
scraper.addUUUID()
time.sleep(2)
print(scraper.df.head())
'''



'''
    scraper = EconCalScraper(tab='econ_calendar')
    time.sleep(2)
    scraper.getImgs()
'''
if __name__ == '__main__':
    scraper = EconCalScraper(tab='econ_calendar')
    #scraper.getLinks()
    scraper.allLinks()

    #time.sleep(3)
    #scraper.allLinks()
    scraper.quitScrap()
