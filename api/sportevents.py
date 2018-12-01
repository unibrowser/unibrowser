"""
Sports Unibrowser API
"""
import json
from typing import List
from database.dao import UnibrowserDAO
import datetime
__collection: str = 'sportsevent'
__host: str = 'localhost'
__port: int = 27017

class Team:
    """
    Represents team information about a match eg: home & away
    """
    def __init__(self, logo_url: str = None, name: str = None, score: str = None):
        self.logo_url = logo_url
        self.name = name
        self.score = score
    
    def to_object(self) -> object:
        """
        :returns: the JSON object representation of the SportInfo
        """
        return self.__dict__

    def jsonable(self):
        return self.__dict__

class SportEvent(object):
    """
    Represents information about a sport event pair
    """

    def __init__(self, sport: str = None, sport_id: int = None, sport_tags: List[str] = None, event_id: str = None, date: datetime.date = None, details: str = None, tickets: str = None, location: str = None, alt_title: str = None, home: Team = None, away: Team = None):
        self.sport = sport
        self.sport_tags = sport_tags
        self.event_id = event_id
        self.date = date
        self.sport_id = sport_id
        self.details = details
        self.tickets = tickets
        self.location = location
        self.alt_title = alt_title
        self.home = home
        self.away = away

    def to_object(self) -> object:
        """
        :returns: the JSON object representation of the SportInfo
        """
        
        return json.dumps(self, default=ComplexHandler)

    def jsonable(self):
        return self.__dict__


def ComplexHandler(Obj):
    if hasattr(Obj, 'jsonable'):
        return Obj.jsonable()

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


def insert(event: SportEvent) -> bool:
    """
    Inserts a single SportInfo object in Unibrowser's persistent storage.
    :param info: the SportInfo to insert
    :returns: true if the insert succeeds, false otherwise
    """
    mongodb = UnibrowserDAO(host=__host, port=__port)
    result = mongodb.insert(collection=__collection, documents=[event.to_object()])
    return result == 1


def insert_many(events : List[dict]) -> bool:
    """
    Inserts multiple SportInfo objects in Unibrowser's persistent storage.
    :param infos: the list of SportInfo objects to insert
    :returns: true if the insert succeeds, false otherwise
    """
    mongodb = UnibrowserDAO(host=__host, port=__port)
    result = mongodb.insert(collection=__collection, documents=events)
    return result == 1


def clear() -> bool:
    """
    Completely removes all SportInfo information from persistent storage.
    :returns: true if the operation succeeds, false otherwise
    """
    mongodb = UnibrowserDAO(host=__host, port=__port)
    results = mongodb.delete(collection=__collection)
    return results >= 0
