import sys
import os
sys.path.insert(0, os.path.realpath('./'))
import requests
import logging
import pymongo
from bs4 import BeautifulSoup
import lxml

from database.mongoclientclass import MongoClientClass

root = 'http://eecs.oregonstate.edu/people/faculty-directory'

def scrapefn():
    '''
    This functn will scrape Professor's info and print it.
    '''
    r = requests.get(root)
    soup = BeautifulSoup(r.content, 'lxml')
    tr_list = soup.find('div', id='block-system-main').find('tbody').find_all('tr')
    print ('Number of products: {}'.format(len(tr_list)))
    sample_profs = []
    for tr in tr_list:
        td_list = tr.find_all('td')
        
        image=td_list[0].find('img')
        a = td_list[1].find('a')
        research_interests = td_list[2].get_text()
        contact_info = td_list[3].get_text()
        

        prof_name = a.get_text()
        prof_url = root + a['href']
        prof_image_url = image['src']

        #print ('\nProfessor name: ', prof_name)
        #print ('Photo: ', prof_image_url)
        #print ('Address & Contact Info:', contact_info)
        #print ('Professor page url: ', prof_url)

        sample_professor = {
                'prof_name': prof_name,
                'photo': prof_image_url,
                'Address & Contact Info':contact_info,
                'Professor page url':prof_url
        }
        sample_profs.append(sample_professor)

    mongoClientInstance = MongoClientClass()
    
    mongoClientInstance.insert(documents=sample_profs)
    entries = mongoClientInstance.find()
    for entry in entries:
        print(entry)
        

if __name__ == '__main__':
    scrapefn()
