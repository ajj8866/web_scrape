from importlib.resources import contents
from multiprocessing.connection import wait
import string
import sys
import requests
from bs4 import BeautifulSoup
import requests
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
        #compiler = re.compile(r'/quote/\w*/chart\?p=\w*')
        #search_url = 'https://uk.finance.yahoo.com/quote/' + ticker + '?p=' + ticker + '&.tsrc=fin-tre-srch'
        self.tab = tab
        self.url = url
        op = webdriver.ChromeOptions()
        op.add_argument('--incognito')
        self.driver = Chrome(ChromeDriverManager().install(), options= op)
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 15)
        wait.until(EC.element_to_be_clickable((By.ID, 'dismissGdprConsentBannerBtn'))).click()
        time.sleep(1)

        if tab == 'econ_calendar':
            wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[contains(@class, "nav navbar-nav")]/li/a[@data-gtag = "popular-economic-calendar"]'))).click()
            self.popupEsc()
        elif tab == 'fin_cal':
            wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[contains(@class, "nav navbar-nav")]/li/a[@data-gtag = "popular-calculators"]'))).click()
            self.popupEsc()
        elif tab == 'news':
            wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[contains(@class, "nav navbar-nav")]/li/a[@data-gtag = "popular-news"]'))).click()
            self.popupEsc()
        elif tab == 'spread':
            wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[contains(@class, "nav navbar-nav")]/li/a[@data-gtag = "popular-spreads"]'))).click()
            self.popupEsc()
        elif tab == 'sentiment':
            wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[contains(@class, "nav navbar-nav")]/li/a[@data-gtag = "popular-outlook"]'))).click()
        elif tab == 'heatmap':
            wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[contains(@class, "nav navbar-nav")]/li/a[@data-gtag = "popular-heatmap"]'))).click()
            self.popupEsc()
        elif tab == 'correlation':
            wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[contains(@class, "nav navbar-nav")]/li/a[@data-gtag = "popular-correlation"]'))).click()
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
        self.driver.close()

    def __repr__(self):
        return self.driver.current_url

    def getEvent(self):
        time.sleep(2)
        if self.tab == 'econ_calendar':
            soup = BeautifulSoup(requests.get(self.driver.current_url).content, 'html.parser')
            for i in soup.find_all('tr', id = re.compile(r'calRow\d*')):
                for j in i.find_all('td', class_ = 'calendarToggleCell'):
                    print(j.get_text().strip())
            print('#'*20)

    def getLinks(self):
        soup = BeautifulSoup(requests.get(self.driver.current_url).content, 'html.parser')
        for i in soup.find_all('a'):          
            print(i.attrs['href'])


#for i in ['econ_calendar', 'fin_cal', 'news', 'spread', 'sentiment', 'heatmap', 'correlation']:    
#    scraper = EconCalScraper(tab=i)
#    time.sleep(10)
#    scraper.quitScrap()
#    print('Done for: ', i)
#    time.sleep(3)
scraper = EconCalScraper(tab='econ_calendar')
scraper.getEvent()
scraper.quitScrap()