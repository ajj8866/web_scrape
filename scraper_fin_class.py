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
import re

class FinScraper:
    def __init__(self, ticker, url= 'https://uk.finance.yahoo.com/'):
        #compiler = re.compile(r'/quote/\w*/chart\?p=\w*')
        compiler = re.compile(r'.*AMZN.*')
        self.ticker = ticker
        #search_url = 'https://uk.finance.yahoo.com/quote/' + ticker + '?p=' + ticker + '&.tsrc=fin-tre-srch'
        self.url = url
        op = webdriver.ChromeOptions()
        op.add_argument('--incognito')
        self.driver = Chrome(ChromeDriverManager().install(), options= op)
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.NAME, 'agree'))).click()
        time.sleep(2)
        wait.until(EC.element_to_be_clickable((By.ID, 'yfin-usr-qry'))).send_keys(self.ticker)
        time.sleep(2)
        wait.until(EC.element_to_be_clickable((By.ID, 'yfin-usr-qry'))).send_keys(Keys.ENTER)
        print('Current handle: ', self.driver.current_window_handle)
        wait.until(EC.url_changes(self.driver.current_url))
        soup = BeautifulSoup(requests.get(self.driver.current_url).content, 'html.parser')
        print('#'*20)
        print(self.driver.current_url)
        print('New handle: ',self.driver.current_window_handle)
        print('#'*20)
        time.sleep(2)
        print(soup.prettify())
        for i in soup.find_all('a'):
            print(i.attrs['href'])

    def __repr__(self):
        return self.driver.current_url
    
    def getLinks(self):
        soup = BeautifulSoup(requests.get(self.driver.current_url).content, 'html.parser')
        for i in soup.find_all('a'):
            print(i.attrs['href'])
    
    def quitDriver(self):
        self.driver.close()


scrp = FinScraper(ticker='AMZN')
print(FinScraper)
#scrp.getLinks()
time.sleep(5)
scrp.quitDriver()