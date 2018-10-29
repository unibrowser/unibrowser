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


def get_name(cur_soup_prof, name_key):
    prof_name_list = cur_soup_prof.select(name_key['select'])
    prof_full_name_list = []
    for prof_name in prof_name_list:
        prof_full_name_list = [prof_name.getText().strip()] + prof_full_name_list
    return " ".join(prof_full_name_list)


def get_research(cur_soup_prof, research_key):
    if 'value' in research_key:
        return research_key['value']
    return cur_soup_prof.select(research_key['select'])[0].getText().strip()


def scrape_prof_data(soup, data_structure):
    soup_prof_list = soup.select(data_structure['list']['select'])
    cur_prof_list = []
    for soup_prof in soup_prof_list:
        prof = {
            'name': get_name(soup_prof, data_structure['name']),
            'research': get_research(soup_prof, data_structure['research']),
            'contact': soup_prof.select(data_structure['contact']['select'])[0].getText().strip()
        }
        cur_prof_list.append(prof)
    return cur_prof_list


def save_prof_data(professors):
    try: 
        mongo_client_instance = MongoClientClass(host='localhost', port=27017, db='unibrowser')
        mongo_client_instance.insert(collection='professor', documents=professors)
    except Exception as e:
        print(e)
        print("inside save_prof_data: 0 (exception)")
        return 0
    print("inside save_prof_data: 1 (success)")
    return 1


if __name__ == '__main__':
    # links to be scraped:
    # 1. https://fa.oregonstate.edu/ambc/directory - Agricultural Sciences and Marine Sciences Business Center
    # 2. https://anrs.oregonstate.edu/ - Animal and Rangeland
    with open('config/prof_input_structure.json', 'r') as f:
        jsonList = json.load(f)

    prof_list = []
    for jsonObject in jsonList:
        cur_soup = get_html(jsonObject['url'])
        prof_list.extend(scrape_prof_data(cur_soup, jsonObject['data']))
    # print(json.dumps(prof_list, indent=4))
    save_prof_data(prof_list)
