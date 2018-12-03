import unittest
import sys
# sys.path.append('../')

from scraping.sportscraper_new import getLinksToSports

# sys.path.append('../..')

from sportscraperutils import getSchool, loadJsonFromUrl

class testingscraping(unittest.TestCase):

    def test_get_links_to_sport(self):
        jsonSchools = loadJsonFromUrl("https://api.pac-12.com/v3/schools")
        jsonSchools = loadJsonFromUrl("https://api.pac-12.com/v3/schools")
        collegeName = "Oregon State"
        school = getSchool(collegeName, -1, jsonSchools)
        sportsNameList, sportsLinkLists, sportIdList, sportTitleList = getLinksToSports(school)
        self.assertTrue(len(sportsNameList) > 0)




if __name__ == '__main__':
    unittest.main()