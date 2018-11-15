"""
Unit tests for the Events API
"""
from typing import List
import api.events as events
import unittest
import datetime


class TestProfessorsApi(unittest.TestCase):
    def generate_data(self, num: int) -> List[events.Event]:
        data = []
        for _ in range(num):
            data.append(
                events.Event(
                    title="Unit Testing",
                    date=datetime.datetime.now(),
                    link="http://facebook.com",
                    image_url="http://images.google.com",
                    tags=[
                        'tag1',
                        'tag2']))
        return data

    def test_insert(self):
        data = self.generate_data(1)[0]
        assert events.insert(data)

    def test_insert_many(self):
        data = self.generate_data(5)
        assert events.insert_many(data)

    def test_clear(self):
        assert events.clear()


if __name__ == "__main__":
    unittest.main()
