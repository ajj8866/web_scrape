
import sys
import py
import requests
from bs4 import BeautifulSoup
import uuid
from datetime import datetime as dt
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
import os
from econ_cal_scraper import EconCalScraper
from sqlalchemy import create_engine
from pathlib import Path
import json

class newsCalendar(EconCalScraper):
    econ_tab = 'econ_calendar'
    def __init__(self, url='https://www.myfxbook.com/'):
        super().__init__(url, headless=False, tab = newsCalendar.econ_tab)
        self.df = None
        data_keys = dict.fromkeys(['ID', 'Date', 'Time to Event', 'Country', 'Event', 'Impact', 'Previous', 'Consensus', 'Actual'])
        self.data = [dict.fromkeys(['ID', 'Date', 'Time to Event', 'Country', 'Event', 'Impact', 'Previous', 'Consensus', 'Actual'])]
        self.data_dict = None
    
    def transformData(self):
        id_ls, uuid_ls, date_ls, tte_ls, ctry_ls, ev_ls, imp_ls, prev_ls, cons_ls, act_ls, tm_ls = [], [],[], [], [], [], [], [], [], [], []
        data_dict = dict(self.df)
        for i in range(len(self.df)):
            id_ls.append(self.df['ID'].iloc[i])
            uuid_ls.append(str(self.df['UUID'].iloc[i]))
            date_ls.append(self.df['Date'].iloc[i])
            tte_ls.append(self.df['Time to Event'].iloc[i])
            ctry_ls.append(self.df['Country'].iloc[i])
            ev_ls.append(self.df['Event'].iloc[i])
            imp_ls.append(self.df['Impact'].iloc[i])
            prev_ls.append(self.df['Previous'].iloc[i])
            cons_ls.append(self.df['Consensus'].iloc[i])
            act_ls.append(self.df['Actual'].iloc[i])
            #tm_ls.append(self.df['Formatted Date'].iloc[i])
        self.data_dict = {'ID': id_ls, 'UUID': uuid_ls, 'Date': date_ls, 'Time to Event': tte_ls, 'Country': ctry_ls, 'Event': ev_ls, 'Impact': imp_ls, 'Previous': prev_ls, 'Consensus': cons_ls, 'Actual': act_ls} #, 'Formatted Date': tm_ls}
        print('#'*20)
        print(self.df['ID'].iloc[0])
        print('#'*20)
        print(self.data_dict)
        
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
        self.df['UUID'] = self.addUUID(obj=self.df)
        #self.df.set_index(['ID', 'UUID'], inplace=True)
        #self.df['Formatted Date'] = self.df['Date'].apply(lambda i: dt.strptime(i, "%B %d, %H:%M"))
        self.df = self.df.iloc[1:]
        self.df['Date'] = self.df['Date'].apply(lambda i: i + ' 2022')
        self.df['Formatted Date'] = self.df['Date'].apply(lambda i: dt.strptime(i, '%b %d, %H:%M %Y'))
        print(self.df)
        return self.df, self.data

    def calData(self):
        json_cal = Path(Path.cwd(), 'Datapipe', 'raw_data', 'news_data.json')
        print(json_cal.exists)
        if json_cal.is_file() == False:
            with open(json_cal, 'w') as fw:
                json.dump(self.data_dict, fw)
        else:
            with open(json_cal, 'r+') as f:
                try:
                    pyfile = json.load(f)
                    f.seek(0)
                    for id, uuid, dte, ttevent, ctry, ev, imp, pre, con, act  in zip(self.data_dict['ID'], self.data_dict['UUID'], self.data_dict['Date'], self.data_dict['Time to Event'], self.data_dict['Country'], self.data_dict['Event'], self.data_dict['Impact'], self.data_dict['Previous'], self.data_dict['Consensus'], self.data_dict['Actual']): #, self.data_dict['Formatted Date']):
                        #formd
                        if id not in pyfile['ID']:
                            pyfile['ID'].append(id)
                            pyfile['UUID'].append(uuid)
                            pyfile['Date'].append(dte)
                            pyfile['Time to Event'].append(ttevent)
                            pyfile['Country'].append(ctry)
                            pyfile['Event'].append(ev)
                            pyfile['Impact'].append(imp)
                            pyfile['Previous'].append(pre)
                            pyfile['Consensus'].append(con)
                            pyfile['Actual'].append(act)
                            #pyfile['Formatted Date'].append(formd)
                    f.seek(0)
                    json.dump(pyfile, f)
                    print(pyfile)
                except Exception as e:
                    print('Exception')
                    print(e)
                    print('yeah excep')
                    f.seek(0)
                    json.dump(self.data_dict, f)
            f.close()



if __name__ == '__main__':
    print('#'*20)
    cal = newsCalendar()
    print(cal._tab)
    print('#'*20)
    print(cal.wait)
    cal.getEvent()
    #cal.toSql()
    cal.transformData()
    time.sleep(2)
    cal.calData()
    cal.quitScrap()