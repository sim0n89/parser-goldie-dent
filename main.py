import math
from fake_useragent import UserAgent
import requests
import logging
from pprint import pprint
import re
from bs4 import BeautifulSoup
import json
from multiprocessing import Pool
from random import choice
from time import sleep
from random import uniform
from mysql.connector import MySQLConnection, Error
import mysql.connector
import dbHandlers


logging.basicConfig(
    level=logging.DEBUG,
    filename = "mylog.log",
    format = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
    )
logger = logging.getLogger(__name__)

def get_html(url, params=None):
    useragent = {'User-Agent': ua.random}
    proxy = {'http': 'http://' + choice(proxies)}
    r = requests.get(url.strip(), params=params, headers=useragent, proxies=proxy)

    return r.text


def get_all_brands(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        brands = soup.find('section', class_='manufacturer__list').find_all('a', class_='manufacturer__link')
        links = []

        for brand in brands:
            link = HOST + brand.get('href')
            links.append(link)
        return links
    except Exception as e:
        print(e)


ua = UserAgent()
print(ua.random)

proxies = open('proxies.txt').read().split('\n')
HOST = 'https://goldident.ru'
linksfile = 'links.txt'




def get_products(brand):

    logger.info("Parsing new brand" + brand)
    html = get_html(brand)
    soup = BeautifulSoup(html, 'html.parser')
    try:
        page_numbers = soup.find('div', class_='bx-pagination-container').find('ul')
        max_number = int(page_numbers.find_all('li')[-2].text.strip())
        print (max_number)
    except:
        max_number = 1
    links = ''
    if max_number > 1:
        for x in range(1, max_number + 1):
            url = brand + '?PAGEN_1=' + str(x)
            logger.info("parsing links on page " + url)

            html = get_html(url)
            soup = BeautifulSoup(html, 'html.parser')
            try:
                products = soup.find_all('div', class_='product-card-wrapper')
                for product in products:
                    a = product.find('a', class_='product-card__link-img').get('href')
                    links = links + a + '\n'

            except Exception as e:
                logger.error('Error ' + e)


    if max_number == 1:
        try:
            products = soup.find_all('div', class_='product-card-wrapper')
            for product in products:
                a = product.find('a', class_='product-card__link-img').get('href')
                links = links + a + '\n'
        except Exception as e:
            logger.error('Error ' + e)
    return links


def get_product_data(html):
    # print(html)
    soup = BeautifulSoup(html, 'html.parser')
    product={}
    details = soup.find('div', 'product-details')
    try:
        product['name'] = soup.find('div', class_='catalog-top__title').find('h1').text.strip()
    except:
        product['name']=''

    try:
        product['price'] = int("".join(filter(str.isdecimal,soup.find('div', id='price').text.strip())))
    except:
        product['price']= ''


    try:
        product['special_price'] = int("".join(filter(str.isdecimal,soup.find('div', id='oldPrice').text.strip())))
    except:
        product['special_price']= ''

    try:

        product['images'] = HOST + soup.find('div', id='main-image').find('a').get('href')

    except:
        product['images'] = ''

    # try:
    #     stock = details.find('span', class_='product-stock-status')
    #     if stock:
    #         product['stock'] = 10
    # except:
    #     product['stock'] = 0


    try:
        categories = soup.find('ol', class_='breadcrumb').find_all('li')
        categories.pop(0)
        categories.pop(-1)
        product['category'] = ''
        for category in categories:
            cat = category.find('span', itemprop="name").text
            product['category'] = product['category'] + cat + '|'

    except:
        product['category'] =''


    try:
        product['desc']= soup.find('div', id='nav-description').find('div', class_='col').text.strip().replace('\n', '<br>').replace('\r', '').replace('\t', '').replace('\xa0', ' ')
    except:
        product['desc'] = ''

    try:
        atributes = soup.find('div', id='nav-characteristic').find('table').find('tbody').find_all('tr')
        product['atrs'] = ''
        product['brend'] = ''
        product['sku'] = ''
        for atribute in atributes:

            atr_name = atribute.find_all('td')[0].text
            atr_value = atribute.find_all('td')[1].text
            if atr_name == 'Производитель':
                product['brend'] = atr_value
            if atr_name == 'Артикул':
                product['sku'] = atr_value
                continue
            product['atrs'] = product['atrs'] + atr_name + ':' + atr_value + '|'

    except:
        pass

    try:
        main_properties = soup.find('div', class_='main-properties').find_all('dt')
        for prop in main_properties:

            value = prop.find_next('dd').text
            if prop.text == 'Код товара':
                product['model'] = value
            if prop.text == 'Артикул':
                product['sku'] = value
            if prop.text == 'Наличие на складе':
                product['stock'] = value.replace('\n', '')
    except:
        pass

    return product


def make_all(link):
    html = get_html(HOST + link)
    print(link)
    data = get_product_data(html)
    pprint(data)
    dbHandlers.add_product(data)


def main():
    # url = 'https://goldident.ru/manufacturer/'
    # brands = get_all_brands(get_html(url))
    # products = ''
    # for brand in brands:
    #     products = products + get_products(brand)
    # with open(linksfile, "w") as file:
    #     file.write(products)
    all_links = open(linksfile).readlines()
    with Pool(3) as p:
        p.map(make_all, all_links)


if __name__ == '__main__':
   main()


