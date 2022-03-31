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
    def __init__(self, url = 'https://www.crunchyroll.com', tab = 'popular', headless = True):
        self.tab = tab
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
        #op.add_argument('--incognito')
        self.driver = Chrome(ChromeDriverManager().install(), options= op)
        self.driver.get(url)
        self.driver.maximize_window()
        self.accRejCookies()
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.opt-in > button.opt-in__close'))).click()
        self.getShows()
        self.pickSection(tab)

    def __repr__(self):
        return str(self.driver.current_url)

    def accRejCookies(self, rej = False):
        wait = WebDriverWait(self.driver, 10)
        if rej == True:
            cookies =  wait.until(EC.element_to_be_clickable((By.ID, '_evidon-decline-button')))
            cookies.click()
        else:
            cookies =  wait.until(EC.element_to_be_clickable((By.ID, '_evidon-accept-button')))
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
    
    def getAlphaPg(self, letter = 'a'):
        '''
        letter argument may either incclude any of the alphabet a-z in lower case, "#" or "all"
        '''
        #soup = BeautifulSoup(requests.get(self.driver.current_url).content, 'html.parser')
        #print(soup.prettify)
        time.sleep(2)
        url = "/en-gb/videos/anime/alpha?group="+letter
        try:
            self.driver.find_element(By.XPATH, f'//div[@id="content-menu-top"]/div/a[@href = "{url}"]').click()
        except:
            print('Method only valid if "alphabet" selected as tab argument')

    def filterGenre(self, genre = ['action']):
        '''
        genre argument: Must be a list comprising of any combination of the following values:
            "action", "adventure", "comedy", "drama", "fantasy", "harem", "historical", "idols",
            "isekai", "magical-girls", "mecha", "music", "mystery", "post-apocalyptic", "romance",
            "sci-fi", "seinen", "shojo", "shonen", "slice of life", "sports", "supernatural", "thriller"
        '''
        time.sleep(2)
        self.driver.find_element(By.ID, 'genres_link').click()
        for i in genre:
            self.driver.find_element(By.ID, i).click()
            time.sleep(1)

    def getWebpage(self):
        print(self.driver.current_url)
        soup = BeautifulSoup(requests.get(self.driver.current_url).text, 'html.parser')
        print(soup.prettify())
        return soup

    def getLinks(self):
        print(f'Current URL: {self.driver.current_url}')



if __name__ == '__main__':
    sc = aniScraper(tab='alphabet')
    #print(sc)
    sc.getAlphaPg(letter='b')
    time.sleep(3)
    sc.filterGenre(genre=['action', 'mecha', 'music', 'mystery'])
    time.sleep(3)
    sc.getWebpage()
    time.sleep(2)
    sc.quitDriver()

#print(BeautifulSoup(requests.get('https://www.crunchyroll.com/en-gb/videos/anime/genres/sci-fi#/videos/anime/genres/sci-fi,supernatural')))