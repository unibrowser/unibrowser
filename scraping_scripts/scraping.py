import requests
from bs4 import BeautifulSoup
import lxml

root = 'http://eecs.oregonstate.edu/people/faculty-directory'

def scrapefn():
    '''
    This functn will scrape Professor's info and print it.
    '''
    r = requests.get(root)
    soup = BeautifulSoup(r.content, 'lxml')
    tr_list = soup.find('div', id='block-system-main').find('tbody').find_all('tr')
    print ('Number of products: {}'.format(len(tr_list)))
    for tr in tr_list:
        td_list = tr.find_all('td')
        
        image=td_list[0].find('img')
        a = td_list[1].find('a')
        research_interests = td_list[2].get_text()
        contact_info = td_list[3].get_text()
        
        # a = tr.find('a')
        # info = tr.get_text()

        prof_name = a.get_text()
        prof_url = root + a['href']
        prof_image_url = image['src']

        print ('\nProfessor name: ', prof_name)
        print ('Photo: ', prof_image_url)
        print ('Address & Contact Info:', contact_info)
        print ('Professor page url: ', prof_url)
        

if __name__ == '__main__':
    scrapefn()
