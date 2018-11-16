"""
Unit tests for the Bus Info API
"""
from typing import List
import api.businfo as businfo
import unittest
import datetime


class TestProfessorsApi(unittest.TestCase):
    def generate_data(self, num: int) -> List[businfo.BusInfo]:
        data = []
        for _ in range(num):
            data.append(
                businfo.BusInfo(lat_long="12,12", details={})
            )
        return data

    def test_insert(self):
        data = self.generate_data(1)[0]
        assert businfo.insert(data)

    def test_insert_many(self):
        data = self.generate_data(5)
        assert businfo.insert_many(data)

    def test_clear(self):
        assert businfo.clear()


if __name__ == "__main__":
    unittest.main()
