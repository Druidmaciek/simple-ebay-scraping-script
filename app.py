""" Script for scraping ebay products given product url """
from collections import namedtuple
from datetime import date
from typing import List

from bs4 import BeautifulSoup
import pandas as pd
import requests

Item = namedtuple("Item", "url img_url name price")


def scrape_ebay(url: str):
    soup = make_request(url)
    items = parse_page_items(soup)
    file_name = save_to_csv(items, 'ebay')
    print(f'{len(items)} items saved to {file_name}')


def parse_page_items(soup) -> List[Item]:
    results = soup.find('ul', {'class': 'srp-results'})
    items = results.find_all('li', {'class': 's-item'})
    return [parse_item(x) for x in items]


def parse_item(soup) -> Item:
    url = soup.find('a')['href']
    img_url = soup.find('img', {'class': 's-item__image-img'})['src']
    name = soup.find('h3', {'class': 's-item__title'}).text.strip()
    price = soup.find('span', {'class': 's-item__price'}).text.strip()
    return Item(url, img_url, name, price)


def save_to_csv(data, file_name):
    file_name = f'{file_name}_{date.today()}.csv'
    df = pd.DataFrame(data)
    df.to_csv(file_name, index=None)
    return file_name


def make_request(url: str):
    response = requests.get(url)
    response.raise_for_status()  # Raises an exception if request gives status code like 503, 404, 502 etc.
    return BeautifulSoup(response.content, "html.parser")


if __name__ == '__main__':
    scrape_ebay(input('ebay url:').strip())
