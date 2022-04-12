from tkinter import N
import requests
from bs4 import BeautifulSoup
import uuid
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from sqlalchemy import true
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
from aws_scraper import aws_rds, aws_s3_download, aws_s3_upload, aws_s3_upload_folder
import shutil


class EconCalScraper:
    def __init__(self, url= 'https://www.myfxbook.com/', tab = 'econ_calendar', headless = True):
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
        if headless == True:
            op.add_argument('--headless')
            op.add_argument('--no-sandbox')
            op.add_argument('--disable-dev-shm-usage')
            #op.add_argument("--window-size=1024,768")
            op.add_argument("--window-size=1920,1080")
            op.add_argument("--remote-debugging-port=9222")
        #op.add_argument('--incognito')
        self.driver = Chrome(ChromeDriverManager().install(), options= op)
        self.driver.get(url)
        self.driver.maximize_window()
        self.driver.save_screenshot('scrn.png')
        self.wait = WebDriverWait(self.driver, 15)
        try:
            self.wait.until(EC.element_to_be_clickable((By.ID, 'dismissGdprConsentBannerBtn'))).click()
        except Exception as e:
            print(e)
            pass
        self.img_list = [dict.fromkeys(['UUID', 'Image', 'Extension'])]
        self.link_dict = [dict.fromkeys(['UUID', 'Links'])]
        self.img_dict = {'UUID':[], 'Image':[], 'Extension':[]}
        time.sleep(1)
        print(1)
        self.getPage()
        print(11)
        self.mkPath()
        

    def getPage(self, toggle = input('Toggle cell?')):
        '''
        Method used on instantiation to navigate to selected tab as specified in tab argument
        '''
        if toggle == 'yes'.lower():
            print(2)
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.menu-toggler'))).click()
            self.driver.save_screenshot('src_2.png')
        else:
            pass
        if self._tab == 'econ_calendar':
            print(3)
            self.actionChainClick(self.wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[contains(@class, "nav navbar-nav")]/li/a[@data-gtag = "popular-economic-calendar"]'))))
            print('Curent name; ', __name__)
            self.popupEsc()
        elif self._tab == 'fin_cal':
            self.actionChainClick(self.wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[contains(@class, "nav navbar-nav")]/li/a[@data-gtag = "popular-calculators"]'))))
            self.popupEsc()
        elif self._tab == 'news':
            self.actionChainClick(self.wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[contains(@class, "nav navbar-nav")]/li/a[@data-gtag = "popular-news"]'))))
            self.popupEsc()
        elif self._tab == 'spread':
            self.actionChainClick(self.wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[contains(@class, "nav navbar-nav")]/li/a[@data-gtag = "popular-spreads"]'))))
            self.popupEsc()
        elif self._tab == 'sentiment':
            self.actionChainClick(self.wait.until(EC.presence_of_element_located((By.XPATH, '//ul[contains(@class, "nav navbar-nav")]/li/a[@data-gtag = "popular-outlook"]'))))
            self.popupEsc()
        elif self._tab == 'heatmap':
            self.actionChainClick(self.wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[contains(@class, "nav navbar-nav")]/li/a[@data-gtag = "popular-heatmap"]'))))
            self.popupEsc()
        elif self._tab == 'correlation':
            self.actionChainClick(self.wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[contains(@class, "nav navbar-nav")]/li/a[@data-gtag = "popular-correlation"]'))))
            self.popupEsc()

    def actionChainClick(self, el):
        actions = ActionChains(self.driver)
        actions.move_to_element(el)
        #actions.click(el)
        actions.click()
        actions.perform()

    def popupEsc(self):
        '''
        Also applied on instantiation. Refreshes page so that pop add which shows up shortly after navigating to any given tab is removed
        '''
        wait = WebDriverWait(self.driver, 15)
        time.sleep(2)
        self.driver.refresh()
        time.sleep(2)
        try: 
            wait.until(EC.element_to_be_clickable((By.ID, 'blockWebNotification'))).click()
        except:
            pass
    
    def quitScrap(self):
        '''
        Closes chrome window and quits driver
        '''
        time.sleep(1)
        self.driver.close()
        self.driver.quit()

    def __str__(self):
        return str(self.driver.current_url)
    
    def getImgs(self, ext = ''):
        '''
        Yields imags ending with extension as set by ext argument:
        ext = jpg/png or any other valid extension used for images. If set as '' or not specified all images
              scrapped
        '''
        print(self.driver.current_url)
        time.sleep(2)
        element = self.driver.find_elements(By.XPATH, '//img')
        img_type = re.compile(f'{ext}$')
        for i in element:
            if re.findall(img_type, i.get_attribute('src')) != []:
                self.img_list.append({'UUID': str(uuid.uuid4()), 'Image' :i.get_attribute('src'), 'Extension': i.get_attribute('src').split('.')[-1]})
                #print(i.get_attribute('src'))
                self.img_dict['UUID'].append(str(uuid.uuid4()))
                self.img_dict['Image'].append(i.get_attribute('src'))
                self.img_dict['Extension'].append(i.get_attribute('src').split('.')[-1])
        #self.quitScrap()
        self.img_list = self.img_list[1:]
        print(self.img_list)
        #elf.img_link_dict['Images'].extend(self.img)
        self.archImg()
        return self.img_dict, self.img_list

    def addUUID(self, obj):
        '''
        Convenience method used to append a UUID to each indvidual observation for other methods
        '''
        uuid_ls = [str(uuid.uuid4()) for i in range(len(obj))]
        return uuid_ls

    def getLinks(self):
        '''
        Yields all links existing on chosen tab 
        '''
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
        '''
        Makes raw_data folder for storing json files should the folder not already exist
        '''
        if 'raw_data' not in os.listdir(Path(Path.cwd())):
            os.mkdir(Path(Path.cwd(), 'raw_data'))

    def mkImgFold(self):
        '''
        Makes image folder within workding directory if it doesn't already exist
        '''
        #print('#'*20)
        #print(os.listdir(Path(Path.cwd(), 'Datapipe','raw_data')))
        #print('#'*20)
        if 'images' not in os.listdir(Path(Path.cwd(), 'raw_data')):
            os.mkdir(Path(Path.cwd(), 'raw_data', 'images'))
    
    def uploadImg(self):
        '''
        Uploads image onto images subfolder within raw_data folder
        '''
        self.mkImgFold()
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
        num_list = []
        for j in os.listdir(Path(Path.cwd(), 'raw_data', 'images')):
            num_list.append(int(j.split('.')[0].zfill(4)))
        for i, img_url in enumerate(self.img_list, start=len(num_list)):
            print(img_url)
            print('#'*20)
            print(img_url)
            print('#'*20)
            if (img_url['Image'].split('.')[-1] in ['png']):
                req = request.Request(img_url['Image'], headers=headers)
                resp = request.urlopen(req)
                resp_data_byte = resp.read()  #.decode('utf-8')
                resp_data = resp_data_byte #.decode('utf-8')
                with open(Path(Path.cwd(), 'raw_data', 'images', f'{i}.png'), 'wb') as img_file:
                    img_file.write(resp_data)

    def archImg(self):
        '''
        Stores individual image links into a json file
        '''
        with open(Path(Path.cwd(), 'raw_data', 'data.json'), 'r+') as f:
            try:
                pyfile = json.load(f)
                f.seek(0)
                for uid_val, img_val, ext_val in zip(self.img_dict['UUID'], self.img_dict['Image'], self.img_dict['Extension']):
                    if uid_val not in pyfile['UUID']:
                        pyfile['UUID'].append(uid_val)
                        pyfile['Image'].append(img_val)
                        pyfile['Extension'].append(ext_val)
                json.dump(pyfile, f)
                print(pyfile)
            except Exception as e:
                print(e)
                json.dump(self.img_dict, f)
        f.close()

    @property
    def tab(self):
        return self.tab

    @tab.setter
    def tab(self, new_val):
        self._tab = new_val

    @classmethod
    def allLinks(cls):
        '''
        Given nature of data the number of images on any given page insufficient to meet criteria specified in tasks.

        This class method aggregates images stored across all tabs on Myfxbook site storing the images in a list 
        '''
        time.sleep(5)
        link_list = []
        for i in ['econ_calendar','fin_cal','news','spread','sentiment','heatmap','correlation']:
            time.sleep(2)
            new_inst = cls(url = 'https://www.myfxbook.com/', tab = i)
            new_inst.getLinks()
            print(new_inst.link_dict)
            for i in new_inst.link_dict[1:]:
                print(i)
                print(i.keys())
                print(i.values())
                if 'Links' in i.keys():
                    link_list.extend(i['Links'])
            #link_list.extend([j['Links'] for j in new_inst.link_dict])
            time.sleep(5)
            new_inst.quitScrap()
        link_list = set(link_list)
        print(len(link_list))
        print(link_list)
        return link_list
    
    @classmethod
    def reset(cls, new_tb, url = 'https://www.myfxbook.com/'):
        cls.inst = None
        cls.inst = EconCalScraper(url= url, tab= new_tb)
        return cls.inst


if __name__ == '__main__':
    tab_input = input('Input tab you would like to navigate to. Must be one of (i) econ_calendar, (ii) fin_cal, (iii) news, (iv) spread, (v) sentiment, (vi) heatmap, (vii) correlation ')
    scraper = EconCalScraper(tab=tab_input, headless=True)
    time.sleep(2)
    scraper.getLinks()
    scraper.getImgs(ext='png')
    scraper.uploadImg()
    scraper.archImg()
    scraper.quitScrap()

    upload_to_s3 = input('Upload to s3 bucket?')
    if upload_to_s3 == 'yes'.lower():
        aws_s3_upload_folder()

    all_links = input('Get all links?')
    if all_links == 'yes'.lower():    
        # Running of all Links class method
        scraper3 = EconCalScraper(tab='spread', headless=True)
        scraper3.quitScrap()
        time.sleep(2)
        scraper3.allLinks()

    