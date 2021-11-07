#!/usr/bin/env python
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import pandas as pd
import lxml
import re
import pdb

csvfile = 'BonaIngredients.csv'
theaders = pd.DataFrame({'product page URL':[],
                         'product name':[] ,
                         'product code':[] ,
                         'ingredient':[] ,
                         'function':[] ,
                         'CAS#':[]})
theaders.to_csv(csvfile,header=True,index=False)


def page_soup(url):
    url = url
    # using this approach because the site sends 403 forbidden 
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    page_soup = soup(webpage, "lxml")
    return page_soup


def prod_urls(page_soup,class_):
    page_soup = page_soup
    prod_links = page_soup.find(class_=class_).find_all('a')
    prod_urls = []
    for prod in prod_links:
        prod_urls.append(prod.get('href'))
    prod_urls = list(set(prod_urls))
    scrape_list = []
    for url in prod_urls:
        scrape_list.append("https://us.bona.com" + url)
    return scrape_list


def get_accordians(url_page,url):
    product_name = url_page.find('h1').text.strip()
    product_code = ""
    accordian_items = url_page.find_all(class_="accordion__item")
    ingredients = []
    ingredients_df = pd.DataFrame()
    for item in accordian_items:
        accordian_title = item.find(class_="accordion__title").text.strip()
        accordian_content = item.find(class_="accordion__content").find_all('p')
        ingre_row = []
        ingre_row.append(url)
        ingre_row.append(product_name)
        ingre_row.append(product_code)
        ingre_row.append(accordian_title)
        for content in accordian_content:
            desc = content.text
            desc = desc.replace("\xa0","").replace("CAS Number:","").strip()
            ingre_row.append(desc)
        ingredients.append(ingre_row)
        ingredients_df = pd.DataFrame(ingredients)
        ingredients_df.to_csv(csvfile, mode = 'a', header=False, index=False)
    

# def get_ingredient_function(description):
#     desc_no_newline = description.replace('\n'," ")
#     if desc_no_newline.find("is a "):
#         start = desc_no_newline.find("is a ") + 5
#         end = desc_no_newline.find(".") + 1
#         return desc_no_newline[start:end]
#     elif desc_no_newline.find("acts as a"):
#         start = desc_no_newline.find("acts as a ") + 10
#         end = desc_no_newline.find(".")
#         return desc_no_newline[start:end]
#     else:
#         return description
    

    
main_url = 'https://us.bona.com/products.html'
page = page_soup(main_url)
prod_type_url = prod_urls(page,"product-line__products clearfix")

for url in prod_type_url:
    url_page = page_soup(url)
    get_accordians(url_page,url)

