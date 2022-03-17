import sys
import requests
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

op = webdriver.ChromeOptions()
op.add_argument('--incognito')
driver = Chrome(ChromeDriverManager().install(), options= op)

driver.get('https://www.zoopla.co.uk/')
print(driver.current_url)
time.sleep(2)
iframe_gdpr = driver.find_element(By.CSS_SELECTOR, 'iframe#gdpr-consent-notice')
driver.switch_to.frame(iframe_gdpr)
driver.find_element(By.ID, 'save').click()

# print(sys.executable)
time.sleep(2)
driver.close()