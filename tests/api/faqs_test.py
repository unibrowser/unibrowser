"""
Unit tests for the FAQ API
"""
from typing import List
import api.faqs as faqs
import unittest


class TestFaqApi(unittest.TestCase):
    def generate_data(self, num: int) -> List[faqs.Faq]:
        data = []
        for _ in range(num):
            data.append(faqs.Faq(
                title='How do I run a test?',
                link='http://www.google.com',
                tags=[
                    'test1',
                    'test2'],
                answer='You use pytest!'))
        return data

    def test_insert(self):
        data = self.generate_data(1)[0]
        assert faqs.insert(data)

    def test_insert_many(self):
        data = self.generate_data(5)
        assert faqs.insert_many(data)

    def test_clear(self):
        assert faqs.clear()


if __name__ == "__main__":
    unittest.main()
