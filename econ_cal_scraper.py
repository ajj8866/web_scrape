import string
import sys
import requests
from bs4 import BeautifulSoup
import requests
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
        self.tab = tab
        self.url = url
        self.data = [dict.fromkeys(['ID', 'Date', 'Time to Event', 'Country', 'Event', 'Impact', 'Previous', 'Consensus', 'Actual'])]
        print(self.data)
        op = webdriver.ChromeOptions()
        op.add_argument('--incognito')
        self.driver = Chrome(ChromeDriverManager().install(), options= op)
        self.driver.get(url)
        self.wait = WebDriverWait(self.driver, 15)
        self.wait.until(EC.element_to_be_clickable((By.ID, 'dismissGdprConsentBannerBtn'))).click()
        self.link_list = []
        time.sleep(1)
        self.getPage()

    def getPage(self):
        if self.tab == 'econ_calendar':
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[contains(@class, "nav navbar-nav")]/li/a[@data-gtag = "popular-economic-calendar"]'))).click()
            self.popupEsc()
        elif self.tab == 'fin_cal':
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[contains(@class, "nav navbar-nav")]/li/a[@data-gtag = "popular-calculators"]'))).click()
            self.popupEsc()
        elif self.tab == 'news':
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[contains(@class, "nav navbar-nav")]/li/a[@data-gtag = "popular-news"]'))).click()
            self.popupEsc()
        elif self.tab == 'spread':
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[contains(@class, "nav navbar-nav")]/li/a[@data-gtag = "popular-spreads"]'))).click()
            self.popupEsc()
        elif self.tab == 'sentiment':
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[contains(@class, "nav navbar-nav")]/li/a[@data-gtag = "popular-outlook"]'))).click()
        elif self.tab == 'heatmap':
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[contains(@class, "nav navbar-nav")]/li/a[@data-gtag = "popular-heatmap"]'))).click()
            self.popupEsc()
        elif self.tab == 'correlation':
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[contains(@class, "nav navbar-nav")]/li/a[@data-gtag = "popular-correlation"]'))).click()
            self.popupEsc()
        self.df = None

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

    def __str__(self):
        return str(self.driver.current_url)

    def getEvent(self):
        time.sleep(2)
        ls = []
        if self.tab == 'econ_calendar':
            soup = BeautifulSoup(requests.get(self.driver.current_url).content, 'html.parser')
            table_row = soup.find_all('tr', id = re.compile(r'calRow\d*')) 
            for i in table_row:
                dum_ls = []
                print(i['data-row-id'])
                dum_ls.append(i['data-row-id'])
                print(len(soup.find_all('td', class_ = 'calendarToggleCell')))
                for j in i.find_all('td', class_ = 'calendarToggleCell'):
                    print(j.get_text().strip())
                    dum_ls.append(j.get_text().strip())
                    ls.append(dum_ls)
                print(dum_ls)
                self.data.append({'ID': int(dum_ls[0]), 'Date': dum_ls[1], 'Time to Event': dum_ls[2], 'Country': dum_ls[4], 'Event': dum_ls[5], 'Impact': dum_ls[6], 'Previous': dum_ls[7], 'Consensus': dum_ls[8], 'Actual': dum_ls[9]})
        self.df = pd.DataFrame(self.data)
        self.addUUUID()
        self.df.set_index(['ID', 'UUDI'], inplace=True)
        self.df = self.df.iloc[1:]
    
    def addUUUID(self):
        uuid_ls = [uuid.uuid4() for i in range(len(self.df))]
        print(uuid_ls)
        self.df['UUID'] = uuid_ls

    #def getLinks(self):
    #    soup = BeautifulSoup(requests.get(self.driver.current_url).content, 'html.parser')
    #    for i in soup.find_all('a'):          
    #        print(i.attrs['href'])

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
        self.tab = new_val
    
    def allLinks(self):
        time.sleep(5)
        link_list = []
        for i in ['econ_calendar','fin_cal','news','spread','sentiment','heatmap','correlation']:
            self.tab = i
            self.getLinks()
            link_list.append(self.link_list)
            time.sleep(5)
        print(link_list)



    

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

scraper = EconCalScraper(tab='econ_calendar')
scraper.getLinks()
scraper.allLinks()
#time.sleep(3)
#scraper.allLinks()