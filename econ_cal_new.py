
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
    def __init__(self, url='https://www.myfxbook.com/', start_engine = False):
        '''
        Addtion of an empty dictionary of keys to comprise of data scrapped in methods within childlcass
        If start_engine parameter set to true connection to RDS instance established and toSql method may 
        be used

        '''
        super().__init__(url, headless=True, tab = newsCalendar.econ_tab)
        self.df = None
        self.data = [dict.fromkeys(['ID', 'Date', 'Time to Event', 'Country', 'Event', 'Impact', 'Previous', 'Consensus', 'Actual'])]
        self.data_dict = None
        # SQL/RDS Parameters
        self.start_engine = start_engine
        if start_engine == True:
            DATABASE_TYPE = 'postgresql'
            DBAPI = 'psycopg2'
            ENDPOINT = str(input('Enter endpoint'))
            USER = 'postgres'
            PASSWORD = input('Enter RDS password')
            PORT = 5432
            DATABASE = 'postgres'
            self.engine = create_engine(f'{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}')
            self.engine.connect()
    
    def transformData(self):
        '''
        Converts list of dictionaries into dictionary of list 
        '''
        time.sleep(2)
        self.getEvent()
        self.data_dict = {key: [dic[key] for dic in self.data] for key in self.data[0]}
        return self.data_dict

    def toSql(self):
        '''
        Calls getEvent method prior to uploading data yielded from getEvent method onto 
        RDS instance
        '''
        if self.start_engine == True:
            self.getEvent()
            self.df.to_sql('Data_Release_Calendar', self.engine, if_exists='replace')
        else:
            print('SQL engine not connected on instantiation')
        
    def getPage(self):
        return super().getPage()

    def getEvent(self):
        '''
        Iterates through all rows in table on page, storing the data as values for the dictionary set on
        instantiation and converted to a dataframe 
        '''
        super().getPage()
        time.sleep(2)
        ls = []
        soup = BeautifulSoup(requests.get(self.driver.current_url).content, 'html.parser')
        table_row = soup.find_all('tr', id = re.compile(r'calRow\d*')) 
        for i in table_row:
            dum_ls = []
            #print(i['data-row-id'])
            dum_ls.append(i['data-row-id'])
            #print(len(soup.find_all('td', class_ = 'calendarToggleCell')))
            for j in i.find_all('td', class_ = 'calendarToggleCell'):
                #print(j.get_text().strip())
                dum_ls.append(j.get_text().strip())
                ls.append(dum_ls)
                print(dum_ls[1])
            self.data.append({'ID': int(dum_ls[0]), 'Date': dum_ls[1], 'Time to Event': dum_ls[2], 'Country': dum_ls[4], 'Event': dum_ls[5], 'Impact': dum_ls[6], 'Previous': dum_ls[7], 'Consensus': dum_ls[8], 'Actual': dum_ls[9]})
        self.df = pd.DataFrame(self.data)
        self.df['UUID'] = self.addUUID(obj=self.df)
        self.df = self.df.iloc[1:]
        print('time_con_1')
        self.df['Date'] = self.df['Date'].apply(lambda i: i + ' 2022')
        print('time_con_2')
        print(self.df.head())
        self.df['Formatted Date'] = self.df['Date'].apply(lambda i: dt.strptime(i, '%b %d, %H:%M %Y'))
        print('time_con_3')
        self.df.drop_duplicates(subset = ['ID'], keep = 'last', inplace = True)
        print('time_con_4')
        df_dum = self.df.copy()
        print('time_con_5')
        df_dum['Formatted Date'] = df_dum['Formatted Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        print('time_con_6')
        print(self.df.iloc[-10:])
        self.data = df_dum.to_dict(orient = 'records')
        return self.df, self.data

    def calData(self):
        '''
        Appends new observations (using ID as unique key) onto json file news_data.json
        '''
        time.sleep(2)
        self.transformData()
        json_cal = Path(Path.cwd(), 'raw_data', 'news_data.json')
        if json_cal.is_file() == False:
            with open(json_cal, 'w') as fw:
                json.dump(self.data_dict, fw)
        else:
            with open(json_cal, 'r+') as f:
                try:
                    pyfile = json.load(f)
                    f.seek(0)
                    for id, uuid, dte, ttevent, ctry, ev, imp, pre, con, act, formd  in zip(self.data_dict['ID'], self.data_dict['UUID'], self.data_dict['Date'], self.data_dict['Time to Event'], self.data_dict['Country'], self.data_dict['Event'], self.data_dict['Impact'], self.data_dict['Previous'], self.data_dict['Consensus'], self.data_dict['Actual'], self.data_dict['Formatted Date']): #, self.data_dict['Formatted Date']):
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
                            pyfile['Formatted Date'].append(formd.strftime('%Y-%m-%d'))
                    f.seek(0)
                    json.dump(pyfile, f)
                except Exception as e:
                    print('JSON file currently empty so dumping all observations')
                    print(e)
                    f.seek(0)
                    json.dump(self.data_dict, f)
            f.close()



if __name__ == '__main__':
    inst_engine = input('Start SQL engine on instantiation and upload to RDS? All data will be uploaded to RDS if "yes"')
    if inst_engine == 'yes'.lower():
        cal = newsCalendar(start_engine=True)
        try:
            cal.getEvent()
            cal.toSql()
            print(cal.data)
            print(cal.data_dict)
            print(cal.df.head())
            cal.quitScrap()
        except Exception as e:
            print('#'*20)
            print('Exception: ', e)
            print('#'*20)
            cal.quitScrap()
    else:
        cal = newsCalendar(start_engine=False)
        try:
            cal.getEvent()
            print(cal.data)
            print(cal.data_dict)
            print(cal.df.head())
            cal.quitScrap()
        except Exception as e:
            print('#'*20)
            print('Exception: ', e)
            print('#'*20)
            cal.quitScrap()



