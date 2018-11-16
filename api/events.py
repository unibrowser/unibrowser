"""
Unibrowser Events API
"""
from typing import List
import datetime
from database.dao import UnibrowserDAO

__collection: str = 'events'
__host: str = 'localhost'
__port: int = 27017


class Event(object):
    """
    Represents a searchable event in the Unibrowser database
    """

    def __init__(self, title: str = None, date: datetime.datetime = None, lat: float = None, lng: float = None,
                 link: str = None, image_url: str = None, tags: List[str] = None):
        self.title = title
        self.date = date
        self.lat = lat
        self.long = lng
        self.link = link
        self.image_url = image_url
        self.tags = tags

    def to_object(self) -> object:
        """
        :returns: the JSON object representation of the event
        """
        # TODO: this will be tricker probably, since we have a 'datetime' object
        return self.__dict__


def configure(dbhost: str = None, dbport: int = None):
    """
    Allows the user of the API to configure it to target a specific database instance. Otherwise will default to the
    Mongo DB running at localhost:27017
    :param dbhost: the host address of the database
    :param dbport: the host port the database is listening on
    """
    if dbhost is not None:
        __host = dbhost
    if dbport is not None:
        __port = dbport


def insert(event: Event) -> bool:
    """
    Inserts a new event into the Unibrowser's persistent storage.
    :param event: the event to insert
    :returns: true if the event was successfully added, false otherwise
    """
    mongodb = UnibrowserDAO(host=__host, port=__port)
    result = mongodb.insert(collection=__collection, documents=[event.to_object()])
    return result == 1


def insert_many(events: List[Event]) -> bool:
    """
    Inserts multiple event objects into the Unibrowser's persistent storage.
    :param events: a list of event objects to insert into the storage
    :returns: true if the list of events was successfully inserted, false otherwise
    """
    mongodb = UnibrowserDAO(host=__host, port=__port)
    result = mongodb.insert(collection=__collection, documents=map(Event.to_object, events))
    return result == 1


def clear() -> bool:
    """
    Completely removes all event information from persistent storage.
    :returns: true if the operation succeeds, false otherwise
    """
    mongodb = UnibrowserDAO(host=__host, port=__port)
    result = mongodb.delete(collection=__collection)
    return result >= 0
