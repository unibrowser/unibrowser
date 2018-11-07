import tweepy
from pymongo import MongoClient
from pymongo.results import InsertManyResult
import sys
import os
sys.path.insert(0, os.path.realpath('./'))
import freefood_config

# Twitter API credentials
consumer_key = freefood_config.API_CREDENTIALS['consumer_key']
consumer_secret = freefood_config.API_CREDENTIALS['consumer_secret']
access_key = freefood_config.API_CREDENTIALS['access_key']
access_secret = freefood_config.API_CREDENTIALS['access_secret']

# Authorization to consumer key and consumer secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# Access to user's access key and access secret
auth.set_access_token(access_key, access_secret)

# Calling tweepy API
api = tweepy.API(auth)

# Class with Database functions 
class MongoClientClass:

    def __init__(self, host, port, db):
        client = MongoClient(host, port)

        # If the database does not exists, it will be created.
        self.db = client[db]
    
    # Function to delete the documents
    def delete(self, collection):
        result=self.db[collection].delete_many({})
        print('Documents deleted from the collection: ', result.deleted_count)
        return result.acknowledged        

    # Function to insert multiple documents
    def insert(self, collection, documents):
        result = self.db[collection].insert_many(documents)
        if isinstance(result, InsertManyResult):
            return 1
        return 0

# Extract tweets
def get_tweets(user_account):
    # Number of tweets to be extracted
    number_of_tweets = freefood_config.TWITTER_INFO['max_tweets']
    # Declaring an empty list to store tweepy tweet information
    tweet_info = []

    # Making request to fetch the most recent tweets
    try:
        tweet=api.user_timeline(screen_name=user_account, tweet_mode='extended', count=number_of_tweets, wait_on_rate_limit=True)

        # save the recent tweet information in the list
        tweet_info.extend(tweet)

        # Create a variable to hold the most oldest tweet id fetched.
        oldest=tweet_info[-1].id-1

        # Keep grabbing tweets until no tweets are left to grab
        while len(tweet) > 0:
            
            # Fetch the next tweet
            tweet=api.user_timeline(screen_name=user_account, tweet_mode='extended', count=number_of_tweets, wait_on_rate_limit=True, max_id=oldest)

            # Save the tweet information in the list.
            tweet_info.extend(tweet)

            # Update the latest id to hold the next expected tweet id
            oldest=tweet_info[-1].id-1

    except tweepy.TweepError as e:
        print(e.api_code)
        print(e.reason)
        print(e.args[0][0]['code'])
    return tweet_info

# Store the selected fields from the tweets in JSON format
def store_tweets(tweet_info):
    
    store_tweet=[]
    # for each tweet, extracting the required info.
    for tweet in tweet_info:
        # Store tweet information in a dictionary
        tweet_info=dict()

        # Tweet id
        tweet_info["id"]=tweet.id_str
        
        # Extracting the text of the tweet
        tweet_info["text"]=tweet.full_text
        # tweet_info["text"]=tweet.text.encode('utf8')

        # date and time for the tweet
        tweet_info["created_at"]=tweet.created_at.strftime("%Y-%m-%d %H:%M:%S")
        
        store_tweet.append(tweet_info)
        
    return store_tweet
    
if __name__ == '__main__':
    # Twitter handle
    tweet_obj=get_tweets(freefood_config.TWITTER_INFO['username'])    
    
    print("No of tweets fetched so far: ",len(tweet_obj))

    # Store the tweets in json file.
    extracted_docs=store_tweets(tweet_obj)

    # Store data in MongoDB
    mongo_client_instance = MongoClientClass(host=freefood_config.DATABASE_CONFIGS['host'], port=freefood_config.DATABASE_CONFIGS['port'], db=freefood_config.DATABASE_CONFIGS['dbname'])
    res=mongo_client_instance.delete(collection='freefood')
    res=mongo_client_instance.insert(collection='freefood', documents=extracted_docs)