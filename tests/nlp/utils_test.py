# system path
import sys
import os
# unit testing
import unittest

# Sets the execution path
sys.path.insert(0, os.path.realpath('./'))

# internal modulesunit
from nlp.utils import get_word_clusters, lemmatize_text

class TestUtils(unittest.TestCase):
    """
    Class containing all the unit tests for the utility functions.
    """
    def test_get_word_clusters(self):
        """
        Tests if the get_word_clusters function works as expected.
        """
        thres = 0.5
        lemma_dict = \
            {
                'cat': ['cats', 'cat'],
                'dog': ['dogs', 'dog']
            }
        lemma_slot, clusters = get_word_clusters(lemma_dict, thres)
        self.assertTrue(len(lemma_slot.items()) == len(lemma_dict.items()))
        self.assertTrue(len(clusters) > 0)


    def test_lemmatize_text(self):
        """
        Tests if the lemmatize_text function works as expected.
        """
        noun_phrases = \
            ["funny dogs","natural language processing","computer processing"]
        lemma_text = lemmatize_text(noun_phrases)
        self.assertTrue(lemma_text.__contains__("dogs"))
        self.assertTrue(lemma_text.__contains__("processing"))
        self.assertFalse(lemma_text.__contains__("cat"))
        self.assertTrue(len(lemma_text) > 0)

if __name__ == '__main__':
    """
    Runs all the unit tests defined above.
    """
    unittest.main()
