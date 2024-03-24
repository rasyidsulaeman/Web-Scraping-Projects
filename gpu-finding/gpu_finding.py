from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

search_items = input("What GPU product do you want to search? ")

def get_page_num(search_items):
    url = f'https://www.newegg.ca/p/pl?d={search_items}&N=4131'
    page = requests.get(url).text 
    doc = BeautifulSoup(page, "html.parser")

    page_num = doc.find(class_="list-tool-pagination-text").strong
    num = int(str(page_num).split("/")[-2].split(">")[-1][:-1])
    return url, num

def company(item, item_title):
    company = item.find(class_="item-branding has-brand-store")
    if company == None or company.a == None or company.a.img == None:
        company_name = item_title.split(" ",1)[0]
    else:
        company_name = company.a.img.get("title")
    return company_name

def rating(item):
    rating = item.find(class_="item-rating")
    if rating == None:
        rating_item = 0
    else:
        rating_item = rating.get("title").split(" + ")[-1]
    
    return rating_item

def get_price(item):
    price_item = item.find(class_="price-current")
    if price_item.strong == None:
        return "0"
    else:
        return price_item.strong.string
   
def create_table(product):
    data = []
    header = product[0].keys()
    for index in range(len(product)):
        data.append(product[index].values())

    path = '/Users/macbookair/Documents/Projects/GPU finding - web scrape/data/'
    file_name = 'gpu_dataset.csv'

    if os.path.exists(path + file_name) == False:
        df = pd.DataFrame(data, columns=header)
        df.to_csv(path + file_name, index=False)
    else:
        df = pd.DataFrame(data)
        df.to_csv(path + file_name, mode="a", header=False, index=False)

def create_product_table(url_old, num):

    for i in range(1,num+1):
        url = url_old + f"&page={i}"
        page = requests.get(url).text 
        doc = BeautifulSoup(page, "html.parser")

        items = doc.find(class_="item-cells-wrap border-cells short-video-box items-grid-view four-cells expulsion-one-cell")

        product = {}

        print("---------------------------")
        print("Page Number : ", i)

        for index, item in enumerate(items):
            container = item.find(class_='item-container')
            item_title = container.a.img.get("title")
            href = container.a.get("href")
            price = get_price(item)
            company_name = company(item, item_title)
            rating_item = rating(item)
        
            product[index] = {"item-name" : item_title, 
                            "price ($)" : int(price.replace(",","")), 
                            "company" : company_name,
                            "rating" : rating_item,
                            "link" : href}
        
        print("Create a table for page : ", i)
        create_table(product)
        print("Table succesfully created")
        print("---------------------------")

url, num = get_page_num(search_items)
create_product_table(url, num)