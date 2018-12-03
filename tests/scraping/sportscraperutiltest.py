import unittest

import sys
from scraping.sportscraperutils import getSchool, loadJsonFromUrl, getListFromJsonArrayWIthKey
from scraping.sportscraper_new import getLinksToSports
class testingscraping(unittest.TestCase):

    def test_load_json_from_url(self):
        link = "https://api.pac-12.com/v3/schools"
        self.assertTrue(loadJsonFromUrl(link)["schools"] is not None)
 
    def test_get_school(self):
        jsonSchools = loadJsonFromUrl("https://api.pac-12.com/v3/schools")
        collegeName = "Oregon State"
        school = getSchool(collegeName, -1, jsonSchools)
        # print(school["name"], "n", collegeName)
        self.assertEqual(school["name"].lower(), collegeName.lower())

    def test_get_list_from_json_array_with_key(self):
        jsonSchools = loadJsonFromUrl("https://api.pac-12.com/v3/schools")
        collegeName = "Oregon State"
        school = getSchool(collegeName, -1, jsonSchools)
        # print(school)
        sportsNameList, sportsLinkLists, sportIdList, sportTitleList = getLinksToSports(school)
        sportPageJson = loadJsonFromUrl(sportsLinkLists[0])
        eventIdsList = getListFromJsonArrayWIthKey("id", sportPageJson["events"])
        self.assertTrue(len(eventIdsList) > 0)

if __name__ == '__main__':
    unittest.main()