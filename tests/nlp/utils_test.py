# system path
import sys
import os
# unit testing
import unittest

# Sets the execution path
sys.path.insert(0, os.path.realpath('./'))

# internal modulesunit
from nlp.utils import get_faq_data, get_lemmatize_dict, get_word_clusters, save_faq_slots


class TestUtils(unittest.TestCase):
    """
    Class containing all the unit tests for the utility functions.
    """

    def test_utils(self):
        """
        Tests if the data is being fetched from the database.
        """
        faqs = get_faq_data('faq')
        self.assertTrue(len(faqs) > 0)

        lemma_text_dict = get_lemmatize_dict(faqs)
        self.assertTrue(len(lemma_text_dict.items()) > 0)

        thres = 0.8
        lemma_slot, clusters = get_word_clusters(lemma_text_dict, thres)
        self.assertTrue(len(lemma_slot.items()) == len(lemma_text_dict.items()))
        self.assertTrue(len(clusters) > 0)

        res = save_faq_slots(lemma_slot, clusters)
        self.assertTrue(res == 1)


if __name__ == '__main__':
    """
    Runs all the unit tests defined above.
    """
    unittest.main()
