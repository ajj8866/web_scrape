from multiprocessing.connection import wait
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

class aniScraper:
    def __init__(self, url = 'https://www.crunchyroll.com', tab = 'popular'):
        op = webdriver.ChromeOptions()
        op.add_argument('--incognito')
        self.driver = Chrome(ChromeDriverManager().install(), options= op)
        self.driver.get(url)
        self.rejCookies()
        self.getShows()
        self.pickSection(tab)

    def __repr__(self):
        print(str(self.driver.current_url))

    def rejCookies(self):
        wait = WebDriverWait(self.driver, 10)
        cookies =  wait.until(EC.element_to_be_clickable((By.ID, '_evidon-decline-button')))
        cookies.click()

    def getShows(self):
        shows = self.driver.find_element(By.XPATH, '//a[@href = "/en-gb/videos/anime"]')
        shows.click()
        print(self.driver.current_url)

    def quitDriver(self):
        self.driver.quit()
    
    def pickSection(self, tab = 'popular'):
        '''
        1) If tab argument set to popular Popular anime sorted by popularity
        2) If tab argument set to updated anime sorted by most recent 
        3) If tab argument set to alphabet anime sorted alphabetically 
        4) 
        '''
        time.sleep(2)
        if tab == 'popular':
            self.driver.find_element(By.XPATH, '//div/a[@token= "shows-popular"]').click()
        elif tab == 'updated':
            self.driver.find_element(By.XPATH, '//div/a[@token= "shows-updated"]').click()            
        elif tab == 'alphabet':
            self.driver.find_element(By.XPATH, '//div/a[@token= "shows-alpha"]').click()            
        else:
            print('Please select one of the following arguments: "popular", "updated", "alphabet"')



sc = aniScraper(tab='alphabet')
#print(sc)
time.sleep(3)

sc.quitDriver()