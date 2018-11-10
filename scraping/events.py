
# Sets the execution path
import sys
import os
sys.path.insert(0, os.path.realpath('./'))

import feedparser
from database.mongoclientclass import MongoClientClass

campusLife = "https://today.oregonstate.edu/releases/feed/campus-life"
eventsUrl = "https://events.oregonstate.edu/calendar.xml"

def extractRSSFeed():
    events = feedparser.parse(eventsUrl)
    eventsList = events.entries
    # Removing unnecessary fields
    for event in eventsList:
        del(event["links"])
        del(event["summary"])
        del(event["id"])
        del(event["published"])
        del(event["summary_detail"])
        del(event["title_detail"])
        del(event["guidislink"])
        del(event["updated"])
        del(event["updated_parsed"])
    return eventsList

def saveToMongo(jsonList, COLLECTION_NAME):
    try:
        mongo_client_instance = MongoClientClass(host='localhost', port=27017, db = 'unibrowser')
        mongo_client_instance.insert(collection = COLLECTION_NAME, documents = jsonList)
    except Exception as e:
        print(e)
        print("inside save_event_data: 0 (exception)")
        return 0
    print("inside save_event_data: 1 (success)")
    return 1

if __name__== "__main__":

    eventJsonList = extractRSSFeed()
    saveToMongo(eventJsonList, "events")
