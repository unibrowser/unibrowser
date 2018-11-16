"""
Bus Information Unibrowser API
"""
from typing import List
from database.dao import UnibrowserDAO

__collection: str = 'businfo'
__host: str = 'localhost'
__port: int = 27017


class BusInfo(object):
    """
    Represents a question/answer pair
    """

    def __init__(self, lat_long = None, details = None):
        self.lat_long = lat_long
        self.details = details

    def to_object(self) -> object:
        """
        :returns: the JSON object representation of the FAQ
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


def insert(info: BusInfo) -> bool:
    """
    Inserts a single BusInfo object in Unibrowser's persistent storage.
    :param faq: the BusInfo to insert
    :returns: true if the insert succeeds, false otherwise
    """
    mongodb = UnibrowserDAO(host=__host, port=__port)
    result = mongodb.insert(collection=__collection, documents=[info.to_object()])
    return result == 1


def insert_many(infos: List[BusInfo]) -> bool:
    """
    Inserts multiple BusInfo objects in Unibrowser's persistent storage.
    :param faqs: the list of BusInfo objects to insert
    :returns: true if the insert succeeds, false otherwise
    """
    mongodb = UnibrowserDAO(host=__host, port=__port)
    result = mongodb.insert(collection=__collection, documents=map(BusInfo.to_object, infos))
    return result == 1


def clear() -> bool:
    """
    Completely removes all BusInfo information from persistent storage.
    :returns: true if the operation succeeds, false otherwise
    """
    mongodb = UnibrowserDAO(host=__host, port=__port)
    results = mongodb.delete(collection=__collection)
    return results >= 0
