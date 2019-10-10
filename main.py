#!/Users/pshop/.local/share/virtualenvs/wiki_tree-NHCRphTb/bin/python

import logging
from pprint import pprint
import json
import re
from bs4 import BeautifulSoup

import requests

EN_WIKI_BASE = 'https://en.wikipedia.org'
EN_WIKI_MAIN = '/wiki/Main_Page'

def get_link_value(html_link_container):
    """
    :param html_link_container: string with at least one href attribute
    :return: string content of the first href
    """
    try:
        return re.search('(?<=href=")(.*)(?=" )', html_link_container)[0]
    except:
        logging.critical('No link found')
        return None

def get_random_link():
    """
    get the link that returns random article
    :return: str relative link
    """
    r = requests.get(EN_WIKI_BASE + EN_WIKI_MAIN)
    if r.status_code != 200:
        return logging.critical('Can\'t reach wikipedia main page')
    if r.encoding != 'UTF-8':
        r.encoding = 'UTF-8'
    page_soup = BeautifulSoup(r.text, 'html.parser')
    random_link = page_soup.find(id='n-randompage')
    return get_link_value(random_link.__str__())

def get_random_article():
    """
    :return: str article content
    """
    rand_article_link = get_random_link()
    try:
        r = requests.get(EN_WIKI_BASE+rand_article_link)
    except:
        logging.critical("can't reach random page")
    if r.encoding != 'UTF-8':
        r.encoding = 'UTF-8'
    random_article_soup = BeautifulSoup(r.text, 'html.parser')
    print(type(random_article_soup))
    article_content = random_article_soup.find(id='content')



if __name__ == '__main__':
    get_random_article()