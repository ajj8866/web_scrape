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

starting_url = 'https://www.crunchyroll.com'
op = webdriver.ChromeOptions()
op.add_argument('--incognito')
driver = Chrome(ChromeDriverManager().install(), options= op)


driver.get(starting_url)
soup = BeautifulSoup(driver.current_url, 'html.parser')


#driver.find_element(By.ID, '_evidon-decline-button').click()
wait = WebDriverWait(driver, 10)
cookies = wait.until(EC.element_to_be_clickable((By.ID, '_evidon-decline-button')))
cookies.click()
#search_bar = driver.find_element(By.CSS_SELECTOR, 'input#search-bar-input')
shows = driver.find_element(By.XPATH, '//a[@href = "/en-gb/videos/anime"]')
shows.click()
time.sleep(2)

#search_bar.send_keys('blah')
#search_bar.send_keys(Keys.ENTER)
driver.quit()

