from fileinput import close
from lib2to3.pgen2 import driver
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
from pandas import json_normalize
from scrapy import Selector
import re
import os
import json
from pathlib import Path
from urllib.request import urlretrieve
import urllib
from urllib import request
from datetime import datetime as dt
import shutil


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
        self.link_dict = [dict.fromkeys(['UUID', 'Links'])]
        self.img_dict = [dict.fromkeys(['UUID', 'Image', 'Extension'])]
        time.sleep(1)
        self.getPage()
        self.mkPath()

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
    
    def getImgs(self, ext = ''):
        print(self.driver.current_url)
        time.sleep(2)
        element = self.driver.find_elements(By.XPATH, '//img')
        img_type = re.compile(f'{ext}$')
        for i in element:
            if re.findall(img_type, i.get_attribute('src')) != []:
                print(i.get_attribute('src'))
                self.img_dict.append({'UUID': str(uuid.uuid4()), 'Image' :i.get_attribute('src'), 'Extension': i.get_attribute('src').split('.')[-1]})
        #self.quitScrap()
        self.img_dict = self.img_dict[1:]
        print(self.img_dict)
        #elf.img_link_dict['Images'].extend(self.img)
        return self.img_dict

    def addUUID(self, obj):
        uuid_ls = [uuid.uuid4() for i in range(len(obj))]
        return uuid_ls

    def getLinks(self):
        print('Current Page URL: ',self.driver.current_url)
        time.sleep(5)
        element = self.driver.find_elements(By.XPATH, '//a')
        print(self.driver.title)
        time.sleep(2)
        print(self.link_dict)
        fxsitelinks = re.compile(r'https://www.myfxbook.com/.*')
        for i in element:
            if (i.get_attribute('href') is not None):
                if re.findall(fxsitelinks, i.get_attribute('href')) != []:
                    print(i.get_attribute('href'))
                    self.link_dict.append({'Links': i.get_attribute('href')})
                    self.link_dict.append({'UUID': str(uuid.uuid4())})
        time.sleep(5)
        #self.quitScrap()
        #self.img_link_dict['Images'].extend(self.link_list)
        print(self.link_dict)
        return self.link_dict
    
    def mkPath(self):
        if 'raw_data' not in os.listdir(Path(Path.cwd(), 'Datapipe')):
            os.mkdir(Path(Path.cwd(), 'Datapipe', 'raw_data'))

    def mkImgFold(self):
        print('#'*20)
        print(os.listdir(Path(Path.cwd(), 'Datapipe','raw_data')))
        print('#'*20)
        if 'images' not in os.listdir(Path(Path.cwd(), 'Datapipe','raw_data')):
            os.mkdir(Path(Path.cwd(), 'Datapipe', 'raw_data', 'images'))
    
    def uploadImg(self):
        self.mkImgFold()
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
        num_list = []
        for j in os.listdir(Path(Path.cwd(), 'Datapipe', 'raw_data', 'images')):
            num_list.append(int(j.split('.')[0].zfill(4)))
        for i, img_url in enumerate(self.img_dict, start=len(num_list)):
            if (img_url['Image'].split('.')[-1] in ['png']):
                req = request.Request(img_url['Image'], headers=headers)
                resp = request.urlopen(req)
                resp_data_byte = resp.read()  #.decode('utf-8')
                resp_data = resp_data_byte #.decode('utf-8')
                with open(Path(Path.cwd(), 'Datapipe', 'raw_data', 'images', f'{i}.png'), 'wb') as img_file:
                    img_file.write(resp_data)

    def archImg(self):
        dum_img_list = []
        dum_img_uuid = []
        for i in self.img_dict:
            dum_img_list.append(i['Image'])
            dum_img_uuid.append(i['UUID'])
        new_img_dict = {'Images': dum_img_list, 'UUID': dum_img_uuid}
        with open(Path(Path.cwd(), 'Datapipe', 'raw_data', 'data.json'), 'a+') as f:
            #temp_file = json.load(f)
            #print(temp_file)
            f.write(json.dumps(new_img_dict))
            f.write('\n')
            f.close()

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
    #scraper.getLinks()
    scraper.allLinks()

    #time.sleep(3)
    #scraper.allLinks()
    scraper.quitScrap()


'''
if __name__ == '__main__':
    scraper = EconCalScraper(tab='econ_calendar')
    time.sleep(2)
    scraper.getImgs(ext='png')
    time.sleep(2)
    scraper.uploadImg()
    #scraper.archImg()
    scraper.quitScrap()
