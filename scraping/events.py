import os
import feedparser
import api.events as events_api
import datetime
from config import DATABASE_CONFIG

campusLife = "https://today.oregonstate.edu/releases/feed/campus-life"
eventsUrl = "https://events.oregonstate.edu/calendar.xml"

# Configure the API to use the correct database
events_api.configure(dbhost=DATABASE_CONFIG['host'], dbport=DATABASE_CONFIG['port'])


def extractRSSFeed():
    events_raw = feedparser.parse(eventsUrl)
    events_list = events_raw.entries
    events = []
    # Removing unnecessary fields
    for event in events_list:
        date_raw = event["published_parsed"]
        date = datetime.datetime(date_raw[0], date_raw[1], date_raw[2])
        e = events_api.Event()
        e.title = event["title"]
        e.date = date
        try:
            e.lat = float(event["geo_lat"])
            e.long = float(event["geo_long"])
        except BaseException:
            pass
        e.link = event["link"]
        e.image_url = event["media_content"][0]["url"]
        e.tags = []
        events.append(e)
    return events


def saveToMongo(events_list):
    try:
        events_api.insert_many(events_list)
    except Exception as e:
        print(e)
        print("inside save_event_data: 0 (exception)")
        return 0
    print("inside save_event_data: 1 (success)")
    return 1


if __name__ == "__main__":

    events_list = extractRSSFeed()
    saveToMongo(events_list)
