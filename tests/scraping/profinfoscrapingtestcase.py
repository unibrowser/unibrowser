import unittest
from scraping.profinfoscraping import scrape_prof_data, get_html


class testingscraping(unittest.TestCase):
    def test_instance_working(self):
        url = "http://eecs.oregonstate.edu/people/faculty-directory"
        soup = get_html(url)
        self.assertTrue(len(soup.getText()) > 0)


if __name__ == '__main__':
    unittest.main()
