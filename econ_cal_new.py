
import sys
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
from econ_cal_scraper import EconCalScraper


class newsCalendar(EconCalScraper):
    econ_tab = 'econ_calendar'
    def __init__(self, url='https://www.myfxbook.com/'):
        super().__init__(url, tab = newsCalendar.econ_tab)
        self.df = None
        self.data = self.data = [dict.fromkeys(['ID', 'Date', 'Time to Event', 'Country', 'Event', 'Impact', 'Previous', 'Consensus', 'Actual'])]

    def getPage(self):
        return super().getPage()

    def getEvent(self):
        super().getPage()
        time.sleep(2)
        ls = []
        soup = BeautifulSoup(requests.get(self.driver.current_url).content, 'html.parser')
        print(self.driver.current_url)
        #print(soup.prettify())
        table_row = soup.find_all('tr', id = re.compile(r'calRow\d*')) 
        print(table_row)
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
        self.addUUID()
        self.df.set_index(['ID', 'UUID'], inplace=True)
        self.df = self.df.iloc[1:]
        print(self.df)
        return self.df, self.data

if __name__ == '__main__':
    print('#'*20)
    cal = newsCalendar()
    print(cal._tab)
    print('#'*20)
    print(cal.wait)
    cal.getEvent()
    cal.quitScrap()