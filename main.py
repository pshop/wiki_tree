#!/Users/pshop/.local/share/virtualenvs/wiki_tree-NHCRphTb/bin/python

import logging
from pprint import pprint
import json
import re
import os
from bs4 import BeautifulSoup

import requests

EN_WIKI_BASE = 'https://en.wikipedia.org/wiki/'
EN_WIKI_MAIN = '/wiki/Main_Page'


class WikiLinksGetter:

    def __init__(self, wiki_page_path, wiki_base_url=EN_WIKI_BASE,):
        self.wiki_base_url = wiki_base_url
        self.wiki_page_path = wiki_page_path
        self.set_of_links = set()

    def get_article_content(self):
        """
        :return: str article_content
        """
        try:
            r = requests.get(self.wiki_base_url + self.wiki_page_path)
        except:
            logging.critical("can't reach random page")
            return None

        if r.encoding != 'UTF-8':
            r.encoding = 'UTF-8'

        random_article_soup = BeautifulSoup(r.text, 'html.parser')
        article_content = random_article_soup.find(id='content')
        return article_content.__str__()

    def set_set_of_links(self):
        soup = BeautifulSoup(self.get_article_content(), 'html.parser')
        for link in soup.find_all('a'):
            link = link.get('href').__str__()
            if ':' not in link and '#' not in link and '//' not in link and '/w/' not in link:
                self.set_of_links.add(link.replace('/wiki/',''))


class TreeFiller:
    
    def __init__(self, begin_link, last_link):
        self.begin_link = begin_link
        self.last_link = last_link
        self.all_links = [self.begin_link]
        self.paths = {
                    '_from': '',
                    self.begin_link: {}}

    def fill_tree(self, link_to_parse=self.begin_link, _from=''):
        wiki_links = WikiLinksGetter(wiki_page_path=link_to_parse)
        wiki_links.set_set_of_links()
        self.paths[link_to_parse]['_from'] = _from

        for link in wiki_links.set_of_links:
            if link not in self.all_links:
                self.all_links.append(link)
                self.paths[link_to_parse][link] = dict()
    


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


def save_article(article_content, erase=False):
    html_file = os.path.join('/tmp', 'article.html')
    if not os.path.isfile(html_file) or erase:
        with open(html_file, 'w')as f:
            f.write(article_content)
    with open(html_file) as f:
        return f.read()


# TODO Extract the text content of an article
# No images, no refs, no menus...
def parse_article(article_content):
    article_soup = BeautifulSoup(article_content, 'html.parser')

    for table in article_soup.find_all('table', {'class':'infobox'}):
        table.decompose()
    [a.decompose() for a in article_soup.find_all('a', {'class':'mw-jump-link'})]
    [a.decompose() for a in article_soup.find_all('a', {'class':'image'})]
    article_soup.find('div', id='catlinks').decompose()


    html_test =os.path.join('/tmp', 'test.html')
    with open(html_test, 'w') as f:
        f.write(article_soup.__str__())
