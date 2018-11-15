"""
Unit tests for the Professors API
"""
from typing import List
import api.professors as profs
import unittest
import pytest
import pymongo
from config import DATABASE_CONFIG, PROFESSOR_CONFIG


class TestProfessorsApi(unittest.TestCase):
    def generate_data(self, num: int) -> List[profs.Professor]:
        data = []
        for _ in range(num):
            data.append(profs.Professor(name="John Smith", research="Computer Science", contact="email@example.com"))
        return data

    def test_insert(self):
        data = self.generate_data(1)[0]
        assert profs.insert(data)

    def test_insert_many(self):
        data = self.generate_data(5)
        assert profs.insert_many(data)

    def test_clear(self):
        data = self.generate_data(5)
        # TODO: find a better way to unit test this...this isn't really "unit testing"...
        mongo = pymongo.MongoClient(DATABASE_CONFIG['host'], DATABASE_CONFIG['port'])
        mongo[DATABASE_CONFIG['dbname']][PROFESSOR_CONFIG['db_collection']
                                         ].insert_many(map(profs.Professor.to_object, data))
        assert profs.clear()


if __name__ == "__main__":
    unittest.main()
