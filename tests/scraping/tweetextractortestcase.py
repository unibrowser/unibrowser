import unittest
import sys
import os
from scraping.tweetextractor import get_tweets, store_tweets, extract_date
from database.dao import UnibrowserDAO
from config import DATABASE_CONFIG


class extract_tweet_test(unittest.TestCase):
    def test_tweet_object(self):
        # unit test for get_tweets()
        tweet_object = get_tweets('@okstatefood')
        print(tweet_object[1])
        self.assertTrue(len(tweet_object) > 0)

    # unit test for store_tweets()
    def test_tweet_extract(self):
        # unit test for get_tweets()
        tweets = store_tweets(get_tweets('@okstatefood'))
        self.assertTrue(len(tweets) > 0)

    def test_mongo_insert(self):
        mongo_client_instance = UnibrowserDAO(
            host=DATABASE_CONFIG['host'], port=DATABASE_CONFIG['port'], dbname=DATABASE_CONFIG['dbname'])
        # unit test for insert
        # 1: success, 0: failure
        self.assertEqual(mongo_client_instance.insert(collection='freefood', documents=[{'id': '1059919297479405573', 'url': 'https://twitter.com/statuses/1059919297479405573', 'screen_name': 'eatfreeOSU',
                                                                                         'media_url': '', 'description': 'Watch the midterm elections, discuss politics, and eat some free Qdoba! 7:30-9:00pm tonight at the APPC.', 'location': 'OSU'}]), 1)


if __name__ == '__main__':
    unittest.main()
