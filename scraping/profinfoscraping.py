# Sets the execution path
import os
import json
import requests
from bs4 import BeautifulSoup
import api.professors as profs_api
from config import PROFESSOR_CONFIG, DATABASE_CONFIG

profs_api.configure(dbhost=DATABASE_CONFIG['host'], dbport=DATABASE_CONFIG['port'])


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
    cur_research = cur_soup_prof.select(research_key['select'])
    if len(cur_research) > 0:
        return cur_research[0].getText().strip()
    return " "


def get_contact(cur_soup_prof, contact_key):
    cur_contact = cur_soup_prof.select(contact_key['select'])
    if len(cur_contact) > 0:
        return cur_contact[0].getText().strip()
    return " "


def scrape_prof_data(soup, data_structure):
    cur_prof_list = []
    soup_prof_list = soup.select(data_structure['list']['select'])
    for soup_prof in soup_prof_list:
        try:
            prof = profs_api.Professor()
            prof.name = get_name(soup_prof, data_structure['name'])
            prof.research = get_research(soup_prof, data_structure['research'])
            prof.contact = get_contact(soup_prof, data_structure['contact'])
            cur_prof_list.append(prof)
        except Exception as e:
            print("Exception occured for ", data_structure)
            print(e)
    return cur_prof_list


def save_prof_data(professors):
    try: 
        profs_api.insert_many(professors)
    except Exception as e:
        print(e)
        # print("inside save_prof_data: 0 (exception)")
        return 0
    # print("inside save_prof_data: 1 (success)")
    return 1


if __name__ == '__main__':
    # links to be scraped:
    # 1. https://fa.oregonstate.edu/ambc/directory - Agricultural Sciences and Marine Sciences Business Center
    # 2. https://anrs.oregonstate.edu/ - Animal and Rangeland
    # 3. https://biochem.science.oregonstate.edu/content/faculty - Biochemistry and Biophysics
    # 4. https://agsci.oregonstate.edu/bioenergy-education/people - Bioenergy Education
    # 5. https://bee.oregonstate.edu/biological-and-ecological-engineering/advisors -Biological & Ecological Engineering
    # 6. https://bpp.oregonstate.edu/faculty - Botany & Plant Pathology
    # 7. https://fw.oregonstate.edu/fisheries-and-wildlife/directory/faculty - Department of Fisheries and Wildlife
    # 8. https://ib.oregonstate.edu/directory/faculty - Department of Integrative Biology
    # 9. http://ceoas.oregonstate.edu/people/ - College of Earth, Ocean, and Atmospheric Sciences
    structure = PROFESSOR_CONFIG['structure']
    with open(structure, 'r') as f:
        jsonList = json.load(f)

    prof_list = []
    for jsonObject in jsonList:
        cur_soup = get_html(jsonObject['url'])
        prof_list.extend(scrape_prof_data(cur_soup, jsonObject['data']))
    # print(json.dumps(prof_list, indent=4))
    save_prof_data(prof_list)
