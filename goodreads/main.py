from bs4 import BeautifulSoup
import requests
import re

url = 'https://www.tokopedia.com'

response = requests.get(url)
page = BeautifulSoup(response.text, 'html.parser')

href = page.find('div', class_ = 'css-l3n1jj')
print(href)