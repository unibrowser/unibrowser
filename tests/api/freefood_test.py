"""
Unit tests for the FAQ API
"""
from typing import List
import api.freefood as freefood
import unittest
import datetime


class TestFaqApi(unittest.TestCase):
    def generate_data(self, num: int) -> List[freefood.FreeFoodInfo]:
        data = []
        for _ in range(num):
            data.append(freefood.FreeFoodInfo(
                title="Free food",
                date=datetime.datetime.now(),
                description="Free food! Come and get it!",
                location="Kelley Atrium",
                link="http://oregonstate.edu"
            ))
        return data

    def test_insert(self):
        data = self.generate_data(1)[0]
        assert freefood.insert(data)

    def test_insert_many(self):
        data = self.generate_data(5)
        assert freefood.insert_many(data)

    def test_clear(self):
        assert freefood.clear()


if __name__ == "__main__":
    unittest.main()
