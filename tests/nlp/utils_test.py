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

    def test_get_faq_data(self):
        """
        Tests if the data is being fetched from the database.
        """
        faqs = get_faq_data('faqs')
        self.assertTrue(len(faqs) > 0)

    def test_lemmatize_text(self):
        """
        Tests if the lemmatize_dict function works as expected.
        """
        sentences = ["testing funny dogs", "doing natural language processing", "working on computer processing"]
        lemmatize_text_dict = get_lemmatize_dict(sentences)
        self.assertTrue(len(lemmatize_text_dict.items()) > 0)

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

    def test_save_results(self):
        thres = 0.5
        lemma_dict = \
            {
                'cat': ['cats', 'cat'],
                'dog': ['dogs', 'dog']
            }
        lemma_slot, clusters = get_word_clusters(lemma_dict, thres)
        res = save_faq_slots(lemma_slot, clusters)
        self.assertTrue(res == 1)


if __name__ == '__main__':
    """
    Runs all the unit tests defined above.
    """
    unittest.main()
