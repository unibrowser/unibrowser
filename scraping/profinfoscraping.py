# Sets the execution path
import sys
import os
sys.path.insert(0, os.path.realpath('./'))

import json
import requests
from bs4 import BeautifulSoup

from database.mongoclientclass import MongoClientClass


def get_html(url):
    '''
    This functn will scrape Professor's info and print it.
    '''
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    return soup


def scrape_prof_data(soup, data_structure):
    soup_prof_list = soup.select(data_structure['list']['select'])
    prof_list = []
    for soup_prof in soup_prof_list:
        prof = {
            'name': soup_prof.select(data_structure['name']['select'])[0].getText().strip(),
            'research': soup_prof.select(data_structure['research']['select'])[0].getText().strip(),
            'contact': soup_prof.select(data_structure['contact']['select'])[0].getText().strip()
        }
        prof_list.append(prof)
    return prof_list


def save_prof_data(professors):
    mongo_client_instance = MongoClientClass(host='localhost', port=27017, db='unibrowser')
    mongo_client_instance.insert(collection='professor', documents=professors)


if __name__ == '__main__':
    with open('config/prof_input_structure.json', 'r') as f:
        jsonList = json.load(f)

    prof_list = []
    for jsonObject in jsonList:
        cur_soup = get_html(jsonObject['url'])
        prof_list.extend(scrape_prof_data(cur_soup, jsonObject['data']))
    # print(json.dumps(prof_list, indent=4))
    save_prof_data(prof_list)
