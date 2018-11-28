# system path
import sys
import os
# unit testing
import unittest
# internal modules
from nlp.utils import get_word_clusters

# Sets the execution path
sys.path.insert(0, os.path.realpath('./'))


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


if __name__ == '__main__':
    """
    Runs all the unit tests defined above.
    """
    unittest.main()
