import unittest
import sys
import os
sys.path.insert(0, os.path.realpath('./scraping'))
from tweetextractor import get_tweets, store_tweets, MongoClientClass, extract_date

class extract_tweet_test(unittest.TestCase):
    def test_tweet_object(self):
        # unit test for get_tweets()
        tweet_object = get_tweets('@okstatefood')
        print(tweet_object[1])
        self.assertTrue(len(tweet_object)>0)        
    
    # unit test for store_tweets() 
    def test_tweet_extract(self):
        # unit test for get_tweets()
        tweets = store_tweets(get_tweets('@okstatefood'))
        self.assertTrue(len(tweets)>0)

    def test_mongo_insert(self):
        mongo_client_instance = MongoClientClass(host='localhost', port=27017, db='unibrowser') 
        # unit test for insert
        # 1: success, 0: failure
        self.assertEqual(mongo_client_instance.insert(collection='freefood', documents=[{'id': '1059919297479405573', 'url': 'https://twitter.com/statuses/1059919297479405573', 'screen_name': 'eatfreeOSU', 'media_url': '', 'description': 'Watch the midterm elections, discuss politics, and eat some free Qdoba! 7:30-9:00pm tonight at the APPC.', 'location': 'OSU'}]),1)  

if __name__ == '__main__':
    unittest.main()