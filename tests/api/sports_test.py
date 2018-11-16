"""
Unit tests for the FAQ API
"""
from typing import List
import api.sports as sports
import unittest


class TestFaqApi(unittest.TestCase):
    def generate_data(self, num: int) -> List[sports.SportInfo]:
        data = []
        for _ in range(num):
            data.append(sports.SportInfo())
        return data

    def test_insert(self):
        data = self.generate_data(1)[0]
        assert sports.insert(data)

    def test_insert_many(self):
        data = self.generate_data(5)
        assert sports.insert_many(data)

    def test_clear(self):
        assert sports.clear()


if __name__ == "__main__":
    unittest.main()
