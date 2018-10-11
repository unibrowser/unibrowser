import unittest
from scraping.profinfoscraping import scrapefn, get_html


class testingscraping(unittest.TestCase):
    def test_instance_working(self):
        self.assertTrue(isinstance(5, int))
        tr_list = get_html()
        self.assertTrue(isinstance(tr_list, list))
        self.assertTrue(len(tr_list) > 0)


if __name__ == '__main__':
    unittest.main()
