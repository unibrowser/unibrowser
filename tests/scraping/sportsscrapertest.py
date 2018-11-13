import unittest
from scraping.sportsscraper import getDivs, getMatchDetails, getMatchMeta

class testingscraping(unittest.TestCase):
    def test_instance_working(self):
        #This particular faq page has 8 question & answers
        
        url = "https://pac-12.com/oregon-state-mens-basketball/schedule/20180801-20190731"
        divs = getDivs(url)
        print("Running Test for getDivs")
        self.assertTrue(len(divs) > 0)

        data = {}
        getMatchDetails(divs[0], data)
        print("Running Test for getMatchDetails")
        self.assertTrue(data['home'] is not None)

        
          
        getMatchMeta(divs[0], data)
        print("Running Test for getMatchMeta")
        self.assertTrue(data['details'] is not None)

    
        
if __name__ == '__main__':
    unittest.main()