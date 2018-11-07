import unittest

from CS534SE.unibrowser.scraping.tweetextractor import get_tweets, store_tweets, MongoClientClass


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

        # unit test for delete
        # TRUE:success; FALSE: failure to delete
        # self.assertEqual(mongo_client_instance.delete(collection='freefood'),TRUE)  

        # unit test for insert
        # 1: success, 0: failure
        self.assertEqual(mongo_client_instance.insert(collection='freefood', documents=store_tweets(get_tweets('@okstatefood'))),1)  

if __name__ == '__main__':
    unittest.main()