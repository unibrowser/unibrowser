import unittest
from scraping.sportscraper_new import loadJsonFromUrl

class testingscraping(unittest.TestCase):
    def test_load_json_from_url(self):
        link = "https://api.pac-12.com/v3/schools"
        self.assertTrue(loadJsonFromUrl(link)["schools"] is not None)



if __name__ == '__main__':
    unittest.main()