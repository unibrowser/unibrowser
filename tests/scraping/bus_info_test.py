import sys
import os
sys.path.insert(0, os.path.realpath('./'))

import json
import unittest
from scraping.bus_info import scrape_row_data, save_loc_data
from config.test import BUS_CONFIG

from scraping.scrape_utils import get_html


class testingScraping(unittest.TestCase):
    def test_instance_working(self):
        lat_lng = BUS_CONFIG['lat_lng_info_file']
        with open(lat_lng, 'r') as f:
            lat_lng_config = json.load(f)
        bus_name = "1"
        url = "https://www.corvallisoregon.gov/cts/page/cts-route-1"

        # unit test for scrape_loc_data()
        location_info = {}
        cur_soup = get_html(url)
        scrape_row_data(cur_soup, bus_name, location_info, lat_lng_config)
        self.assertTrue(len(location_info.items()) > 0)

        loc_info = []
        for loc_lat_lng, details in location_info.items():
            loc_info.append({
                'lat_lng': loc_lat_lng,
                'details': details
            })
        self.assertTrue(len(loc_info) > 0)

        # unit test for save_loc_data()
        self.assertEqual(save_loc_data(loc_info), 1)  # 1:success; 0: failure to save


if __name__ == '__main__':
    unittest.main()
