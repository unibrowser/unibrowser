import sys
import os
import json
import re
sys.path.insert(0, os.path.realpath('./'))

import unittest
from scraping.profinfoscraping import scrape_prof_data, get_html, save_prof_data


class testingscraping(unittest.TestCase):
    def test_instance_working(self):
        question_key = "questions"
        answer_key = "answers"
        isQuestion = re.compile(r"questions")
        isAnswer = re.compile(r"answers")
        self.assertNotEqual(isQuestion, None)
        self.assertNotEqual(isAnswer, None)

if __name__ == '__main__':
    unittest.main()