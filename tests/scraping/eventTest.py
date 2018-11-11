import unittest
import sys
import os
from scraping.events import extractRSSFeed, saveToMongo
from bson import ObjectId
from database.mongoclientclass import MongoClientClass


class eventTesting(unittest.TestCase):
    def testRSS(self):
        # unit test for extractRSSFeed()
        events = extractRSSFeed()
        print(events[1])
        self.assertTrue(len(events) > 0)

    def test_mongo_insert(self):
        mongo_client_instance = MongoClientClass()
        # unit test for insert
        # 1: success, 0: failure
        self.assertEqual(mongo_client_instance.insert(collection='events',
            documents=[{
                "_id": ObjectId("5be74773bb5c748668868409"),
                "title": "Nov 12, 2018: Contemplative Studies Mindfulness Practice Group at Westminster House",
                "geo_lat": "44.5688",
                "geo_long": "-123.277418",
                "published_parsed": [2018, 11, 13, 2, 30, 0, 1, 317, 0],
                "link": "https://events.oregonstate.edu/event/contemplative_studies_mindfulness_practice_group",
                "media_content": [{"medium": "image", "url": "https://d3e1o4bcbhmj8g.cloudfront.net/photos/679786/huge/b59ac8bae7d67da25022d5479f1b61ab2af926c9.jpg"}],
                "tags": [{"term": "Gathering", "scheme": None, "label": None}]
            }]),
                         1)


if __name__ == '__main__':
    unittest.main()
