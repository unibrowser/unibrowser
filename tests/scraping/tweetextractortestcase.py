import unittest
import sys
import os
sys.path.insert(0, os.path.realpath('./scraping'))
from tweetextractor import get_tweets, store_tweets, MongoClientClass,extract_date

class extract_tweet_test(unittest.TestCase):
    def test_tweet_object(self):
        # unit test for get_tweets()
        tweet_object = get_tweets('@okstatefood')
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
        self.assertEqual(mongo_client_instance.insert(collection='freefood', documents=store_tweets(get_tweets('@okstatefood'))),1)  

    def test_extract_date(self):
		# unit test to test the date function
	    date_fetched=extract_date("Today's date is 07-SEP-2018")
	    self.assertEqual(date_fetched,"2018-SEP-07")


if __name__ == '__main__':
    unittest.main()