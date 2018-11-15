"""
Unibrowser Events API
"""
from typing import List
import datetime
from config import EVENT_CONFIG
from database.mongoclientclass import MongoClientClass


class Event(object):
    """
    Represents a searchable event in the Unibrowser database
    """

    def __init__(self, title: str = None, date: datetime.datetime = None,
                 link: str = None, image_url: str = None, tags: List[str] = None):
        self.title = title
        self.date = date
        self.link = link
        self.image_url = image_url
        self.tags = tags

    def to_object(self) -> object:
        """
        :returns: the JSON object representation of the event
        """
        # TODO: this will be tricker probably, since we have a 'datetime' object
        return self.__dict__


def insert(event: Event) -> bool:
    """
    Inserts a new event into the Unibrowser's persistent storage.
    :param event: the event to insert
    :returns: true if the event was successfully added, false otherwise
    """
    mongodb = MongoClientClass()
    result = mongodb.insert(collection=EVENT_CONFIG['db_collection'], documents=[event.to_object()])
    return result == 1


def insert_many(events: List[Event]) -> bool:
    """
    Inserts multiple event objects into the Unibrowser's persistent storage.
    :param events: a list of event objects to insert into the storage
    :returns: true if the list of events was successfully inserted, false otherwise
    """
    mongodb = MongoClientClass()
    result = mongodb.insert(collection=EVENT_CONFIG['db_collection'], documents=map(Event.to_object, events))
    return result == 1


def clear() -> bool:
    """
    Completely removes all event information from persistent storage.
    :returns: true if the operation succeeds, false otherwise
    """
    mongodb = MongoClientClass()
    result = mongodb.delete(collection=EVENT_CONFIG['db_collection'])
    return result >= 0
