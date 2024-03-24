# scraping anime data from myanimelist based on genre
# firstly, we take the data from romance genre 

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import os 
import math

def round_up(n, decimals=0):
    multiplier = 10**decimals
    return math.ceil(n * multiplier) / multiplier

def get_number_of_pages(url):
    response = requests.get(url).text
    page = BeautifulSoup(response, 'html.parser')

    page_num = page.find(class_='pagination ac')
    num = int(page_num.a.string.split(" - ")[-1])

    total_page = page.find(class_='di-ib mt4').span.string[1:-1]
    total_page = int(total_page.replace(",", ""))

    round_num = int(round_up(total_page/num))

    return round_num 

def get_title(category):
    name = category.find(class_ = re.compile('title'))
    span = [s.string for s in name.find_all('span')][1:][::-1]
    span[1] = span[1][:4]
    span[2] = float(span[2])

    return span

def get_info(category):
    info = category.find(class_ = re.compile('info'))
    items = [item.string for item in info.find_all('span')]
    items[3] = items[3].split(" ")[0]

    return items
    
def get_genre(category):
    genre_list = category.find(class_ = re.compile('genre'))
    genre = [gen.a.string for gen in genre_list.find_all('span')]
    
    return genre

def get_source(category):
    property = category.find(class_ = re.compile('properties'))
    source = [prop.string for prop in property.find_all('span')]

    return source[3]

def write_to_csv(data, genre_name):
    headers = ['Anime Title', 'Year Aired', 'Rating', 'Status', 'Number of Episode', 'Genre', 'Source']

    path = '/Users/macbookair/Documents/Projects/Web-Scraping-Projects/myanimelist/data/'
    file_name = f'{genre_name}.csv'
    
    if os.path.exists(path + file_name) == False:
        df = pd.DataFrame(data, columns=headers)
        df.to_csv(path + file_name, index=False)
    else:
        df = pd.DataFrame(data)
        df.to_csv(path + file_name, mode="a", header=False, index=False)

def generate_anime_dataset(url_old, genre_name):

    page_num = get_number_of_pages(url_old)

    for num in range(1, page_num+1):
        url = url_old + f"?page={num}"
        response = requests.get(url).text
        page = BeautifulSoup(response, 'html.parser')

        anime_category = page.find_all('div', class_= re.compile('anime-category'))
        
        table = []

        print("---------------------------")
        print("Page Number : ", num)

        for category in anime_category:
            
            name = get_title(category)
            item = get_info(category)

            name.extend([item[1], item[3]])

            genre = get_genre(category)

            name.append(genre)

            source = get_source(category)

            name.append(source)

            table.append(name)

        print("Create a table for page : ", num)
        
        write_to_csv(table, genre_name)

        print("Table succesfully created")
        print("---------------------------")

def genre_link(genre_search):

    main_url = '/anime.php'
    general_url = 'https://myanimelist.net'
    url = general_url + main_url

    response = requests.get(url).text
    page = BeautifulSoup(response, 'html.parser')

    genre_anime = page.find_all(class_ = 'genre-list al')

    href = {}
    for gen in genre_anime:
        href_dummy = gen.a['href']
        if 'genre' in href_dummy:
            genre_name = gen.a.string.split(" ")[0]
            href[genre_name] = href_dummy

    genre = genre_search

    new_url = general_url + href[genre]

    return new_url        

genre = input("What genre do you want to scrape ? ")
url = genre_link(genre)

generate_anime_dataset(url, genre)