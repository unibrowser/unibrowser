import tweepy
import api.freefood as freefood_api
import datefinder
import datetime
import sys
from datetime import timedelta
from config import TWITTER_CONFIG, FREE_FOOD_CONFIG, DATABASE_CONFIG

freefood_api.configure(dbhost=DATABASE_CONFIG['host'], dbport=DATABASE_CONFIG['port'])

# Twitter API credentials
consumer_key = TWITTER_CONFIG['consumer_key']
consumer_secret = TWITTER_CONFIG['consumer_secret']
access_key = TWITTER_CONFIG['access_key']
access_secret = TWITTER_CONFIG['access_secret']

# Authorization to consumer key and consumer secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# Access to user's access key and access secret
auth.set_access_token(access_key, access_secret)

# Calling tweepy API
api = tweepy.API(auth)

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
        oldest = tweet_info[-1].id - 1

        while len(tweet) > 0:
            tweet = api.user_timeline(screen_name=user_account, tweet_mode='extended',
                                      count=number_of_tweets, wait_on_rate_limit=True, max_id=oldest)
            tweet_info.extend(tweet)
            oldest = tweet_info[-1].id - 1

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
        try:
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
                    # Store the required fields
                    info = freefood_api.FreeFoodInfo()
                    info.title = tweet.user.screen_name
                    info.date = event_date
                    info.link = "https://twitter.com/statuses/" + tweet.id_str  # URL
                    info.location = "OSU"
                    info.description = tweet.full_text
                    media = tweet.entities.get('media', [])
                    if(len(media) > 0):
                        info.media_url = media[0]['media_url']
                    #tweet_dict["id"] = tweet.id_str
                    store_tweet.append(info)
        except BaseException as e:
            print("Caught error while extracting data", e, file=sys.stderr)
            pass
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
        freefood_api.clear()

        for username in FREE_FOOD_CONFIG['username']:
            print(username)

            tweet_obj = get_tweets(username)

            extracted_docs = store_tweets(tweet_obj)

            if len(extracted_docs) != 0:
                freefood_api.insert_many(extracted_docs)
            else:
                print("No tweets found.")

    except BaseException:
        print('Error Occured.')
        raise
