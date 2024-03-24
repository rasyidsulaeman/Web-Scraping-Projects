from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time


url = 'https://www.goodreads.com'

path = '/Users/macbookair/Documents/Driver/chromedriver'
service = Service(executable_path=path)

options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
driver = webdriver.Chrome(service=service, options=options)
driver.get(url)

genre_xpath = '//*[@id="browseBox"]/div[2]/div[4]/a[6]'

reads = driver.find_element(By.XPATH, genre_xpath)
reads.click()

close_block = 'gr-iconButton'

close = driver.find_element(By.Tyu, close_block)
close.click()