import sys
import os
import json
sys.path.insert(0, os.path.realpath('./'))

import unittest
from scraping.profinfoscraping import scrape_prof_data, get_html, save_prof_data


class testingscraping(unittest.TestCase):
    def test_instance_working(self):
        url = "http://eecs.oregonstate.edu/people/faculty-directory"
        with open('config/prof_input_structure.json', 'r') as f:
            jsonList = json.load(f)
            jsonObject = jsonList[0]

        # unit test get_html()
        cur_soup = get_html(jsonObject['url'])
        self.assertTrue(len(cur_soup.getText()) > 0)

        # unit test for scrape_prof_data()
        prof_list = scrape_prof_data(cur_soup, jsonObject['data'])
        self.assertTrue(len(prof_list)>0)        
        
        # unit test for save_prof_data() 
        self.assertEqual(save_prof_data(prof_list),1)  # 1:success; 0: failure to save


if __name__ == '__main__':
    unittest.main()
