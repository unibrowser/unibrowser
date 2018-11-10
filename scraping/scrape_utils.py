# Sets the execution path
import sys
import os
sys.path.insert(0, os.path.realpath('./'))

import requests

from bs4 import BeautifulSoup


def get_html(url):
    '''
    Download a page and load the corresponding soup.
    :param url: Url of the page to fetch.
    :return: Soup of the page.
    '''
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    return soup

