import tweepy
from pymongo import MongoClient
from pymongo.results import InsertManyResult
import sys
import os
sys.path.insert(0, os.path.realpath('./config'))
import freefood_config
import datefinder
import datetime
from datetime import timedelta

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
    return tweet_info

# Store the selected fields from the tweets in JSON format
def store_tweets(tweet_info):
    store_tweet=[]
    # for each tweet, extracting the required info.
    for tweet in tweet_info:
        # Fetch the event date from the tweet text.
        event_date = extract_date(tweet.full_text)

        if event_date == '00-00-0000':
            event_date=tweet.created_at.strftime("%Y-%m-%d")

        if isinstance(event_date, str):
            event_date = datetime.datetime.strptime(event_date, "%Y-%m-%d") #changing event_date into date type
        
        event_date_trun = datetime.date(event_date.year, event_date.month, event_date.day)

        if event_date_trun >= datetime.datetime.today().date():
            
            # Store tweet information in a dictionary
            tweet_dict=dict()

            # Store the event date
            tweet_dict["event_date"]=event_date
            
            # Fetch the media link
            media = tweet.entities.get('media', [])
            if(len(media) > 0):
                tweet_dict["url"]=media[0]['media_url']
            else:
                tweet_dict["url"]=""

            # Tweet id
            tweet_dict["id"]=tweet.id_str
            
            # Extracting the text of the tweet
            tweet_dict["description"]=tweet.full_text
            # tweet_info["text"]=tweet.text.encode('utf8')
            
            tweet_dict["location"]="OSU"
            
            # Store tweet in the dictionary
            store_tweet.append(tweet_dict)
    return store_tweet

# Function to extract date from the text
def extract_date(tweet_text):
    event_date = '00-00-0000'
    matches = datefinder.find_dates(tweet_text)
    for match in matches:
        event_date = match.strftime('%Y-%m-%d')

    # if date not found in the text, look for keywords
    if event_date == '00-00-0000':
        today_list = freefood_config.DATE_SELECT['today_list']
        tom_list = freefood_config.DATE_SELECT['today_list']
        for word in today_list:
                if word in tweet_text.lower():
                        event_date = datetime.datetime.today()
        if event_date == '00-00-0000':
                for word in tom_list:
                        if word in tweet_text.lower():
                                event_date = datetime.datetime.today() + timedelta(days=1)
    return event_date

if __name__ == '__main__':
    try:
        # Delete existing documents from the collection freefood
        mongo_client_instance = MongoClientClass(host=freefood_config.DATABASE_CONFIGS['host'], port=freefood_config.DATABASE_CONFIGS['port'], db=freefood_config.DATABASE_CONFIGS['dbname'])
        res=mongo_client_instance.delete(collection='freefood')
         
        for username in freefood_config.TWITTER_INFO['username']:
            print(username)
            # Twitter handle
            tweet_obj=get_tweets(username)    
            
            print("No of tweets fetched so far: ",len(tweet_obj))

            # Store the tweets in json file.
            extracted_docs=store_tweets(tweet_obj)

            if len(extracted_docs) != 0:
                # Store data in MongoDB
                res=mongo_client_instance.insert(collection='freefood', documents=extracted_docs)
            else:
                print("No tweets found.")
    except:
        print('Error Occured.')
        raise