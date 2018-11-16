"""
Free Food Unibrowser API
"""
from typing import List
from database.dao import UnibrowserDAO
import datetime

__collection: str = 'freefood'
__host: str = 'localhost'
__port: int = 27017


class FreeFoodInfo(object):
    """
    Represents information about available free food
    """

    def __init__(self, title: str = None, date: datetime.datetime = None,
                 description: str = None, location: str = None, link: str = None, media_url: str = None):
        self.title = title
        self.date = date
        self.description = description
        self.location = location
        self.link = link
        self.media_url = media_url

    def to_object(self) -> object:
        """
        :returns: the JSON object representation of the FreeFoodInfo
        """
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


def insert(info: FreeFoodInfo) -> bool:
    """
    Inserts a single FreeFoodInfo object in Unibrowser's persistent storage.
    :param info: the FreeFoodInfo to insert
    :returns: true if the insert succeeds, false otherwise
    """
    mongodb = UnibrowserDAO(host=__host, port=__port)
    result = mongodb.insert(collection=__collection, documents=[info.to_object()])
    return result == 1


def insert_many(infos: List[FreeFoodInfo]) -> bool:
    """
    Inserts multiple FreeFoodInfo objects in Unibrowser's persistent storage.
    :param infos: the list of FreeFoodInfo objects to insert
    :returns: true if the insert succeeds, false otherwise
    """
    mongodb = UnibrowserDAO(host=__host, port=__port)
    result = mongodb.insert(collection=__collection, documents=map(FreeFoodInfo.to_object, infos))
    return result == 1


def clear() -> bool:
    """
    Completely removes all FreeFoodInfo information from persistent storage.
    :returns: true if the operation succeeds, false otherwise
    """
    mongodb = UnibrowserDAO(host=__host, port=__port)
    results = mongodb.delete(collection=__collection)
    return results >= 0
