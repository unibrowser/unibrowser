import tweepy
from pymongo import MongoClient
from pymongo.results import InsertManyResult
from pymongo.errors import BulkWriteError
import sys
import os
import datefinder
import datetime
from datetime import timedelta
from config import TWITTER_CONFIG, FREE_FOOD_CONFIG, DATABASE_CONFIG

# Twitter API credentials
consumer_key = TWITTER_CONFIG['consumer_key']
consumer_secret = TWITTER_CONFIG['consumer_secret']
access_key = TWITTER_CONFIG['access_key']
access_secret = TWITTER_CONFIG['access_secret']
print(consumer_key)

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
        self.db = client[db]

    # Function to delete the documents
    def delete(self, collection):
        result = self.db[collection].delete_many({})
        print('Documents deleted from the collection: ', result.deleted_count)
        return result.acknowledged

    # Function to insert multiple documents
    def insert(self, collection, documents):
        try:
            result = self.db[collection].insert_many(documents)
            if isinstance(result, InsertManyResult):
                return 1
            return 0
        except BulkWriteError as exc:
            print(exc.details)
            exit()

# Extract tweets


def get_tweets(user_account):
    number_of_tweets = FREE_FOOD_CONFIG['max_tweets']
    tweet_info = []

    # Making request to fetch the most recent tweets
    try:
        dt = datetime.datetime.now().date()
        year, week, dow = dt.isocalendar()
        tweet = api.user_timeline(screen_name=user_account, tweet_mode='extended',
                                  count=number_of_tweets, wait_on_rate_limit=True)

        tweet_info.extend(tweet)
        oldest = tweet_info[-1].id-1

        while len(tweet) > 0:
            tweet = api.user_timeline(screen_name=user_account, tweet_mode='extended',
                                      count=number_of_tweets, wait_on_rate_limit=True, max_id=oldest)
            tweet_info.extend(tweet)
            oldest = tweet_info[-1].id-1

    except tweepy.TweepError as e:
        print(e.api_code)
        print(e.reason)
    return tweet_info

# Store the selected fields from the tweets in JSON format


def store_tweets(tweet_info):
    store_tweet = []
    dt = datetime.datetime.now().date()
    year, week, dow = dt.isocalendar()
    # for each tweet, extracting the required info.
    for tweet in tweet_info:
        if tweet.created_at.date() >= (dt - timedelta(dow)):
            # Fetch the event date from the tweet text.
            event_date = extract_date(tweet)

            if event_date == '00-00-0000':
                event_date = tweet.created_at.strftime("%Y-%m-%d")

            if isinstance(event_date, str):
                event_date = datetime.datetime.strptime(
                    event_date, "%Y-%m-%d")  # changing event_date into date type

            event_date_trun = datetime.date(
                event_date.year, event_date.month, event_date.day)

            if event_date_trun >= datetime.datetime.today().date():
                tweet_dict = dict()   # Store tweet information in a dictionary

                # Store the required fields
                tweet_dict["event_date"] = event_date
                tweet_dict["id"] = tweet.id_str
                tweet_url = "https://twitter.com/statuses/"+tweet.id_str  # URL
                tweet_dict["url"] = tweet_url
                tweet_dict["screen_name"] = tweet.user.screen_name
                media = tweet.entities.get('media', [])
                if(len(media) > 0):
                    tweet_dict["media_url"] = media[0]['media_url']
                else:
                    tweet_dict["media_url"] = ""

                tweet_dict["description"] = tweet.full_text
                tweet_dict["location"] = "OSU"
                store_tweet.append(tweet_dict)
    print("no of tweets fetched: ", len(store_tweet))
    return store_tweet

# Function to extract date from the text


def extract_date(tweet):
    event_date = '00-00-0000'
    matches = datefinder.find_dates(tweet.full_text)
    for match in matches:
        event_date = match.strftime('%Y-%m-%d')

    # if date not found in the text, look for keywords
    if event_date == '00-00-0000':
        today_list = FREE_FOOD_CONFIG['date_select']['today_list']
        tom_list = FREE_FOOD_CONFIG['date_select']['tomorrow_list']
        for word in today_list:
            if word in tweet.full_text.lower():
                event_date = tweet.created_at.strftime("%Y-%m-%d")
        if event_date == '00-00-0000':
            for word in tom_list:
                if word in tweet.full_text.lower():
                    event_date = (tweet.created_at + timedelta(days=1)).strftime(
                        "%Y-%m-%d") 
    return event_date

# Function to check if the keywords are present in the text
# def check_text(tweet_text):
#     keywords_list = freefood_config.TWITTER_INFO['keywords']
#     for word in keywords_list:
#         if word in tweet_text.lower():
#             return 1
#     print(tweet_text)
#     return 0


if __name__ == '__main__':
    try:
        # Delete existing documents from the collection freefood
        mongo_client_instance = MongoClientClass(
            host=DATABASE_CONFIG['host'], port=DATABASE_CONFIG['port'], db=DATABASE_CONFIG['dbname'])
        res = mongo_client_instance.delete(collection='freefood')

        for username in FREE_FOOD_CONFIG['username']:
            print(username)

            tweet_obj = get_tweets(username)

            extracted_docs = store_tweets(tweet_obj)

            if len(extracted_docs) != 0:
                res = mongo_client_instance.insert(
                    collection='freefood', documents=extracted_docs)
            else:
                print("No tweets found.")

    except:
        print('Error Occured.')
        raise
