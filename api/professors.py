"""
Unibrowser Professors API
"""
from typing import List
from database.dao import UnibrowserDAO

__collection = 'professor'
__host = 'localhost'
__port = 27017

class Professor(object):
    """
    Represents a professor that is searchable in the Unibrowser database
    """

    def __init__(self, name=None, research=None, contact=None):
        self.name = name
        self.research = research
        self.contact = contact

    def to_object(self) -> object:
        """
        :returns: the JSON object representation of the professor
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


def insert(prof: Professor) -> bool:
    """
    Inserts a single professor object in Unibrowser's persistent storage.
    :param p: the professor to insert
    :returns: true if the insert succeeds, false otherwise
    """
    mongodb = UnibrowserDAO(host=__host, port=__port)
    result = mongodb.insert(collection=__collection, documents=[prof.to_object()])
    return result == 1


def insert_many(profs: List[Professor]) -> bool:
    """
    Inserts multiple professor objects in Unibrowser's persistent storage.
    :param p: the list of professors to insert
    :returns: true if the insert succeeds, false otherwise
    """
    mongodb = UnibrowserDAO(host=__host, port=__port)
    result = mongodb.insert(collection=__collection, documents=map(Professor.to_object, profs))
    return result == 1


def clear() -> bool:
    """
    Completely removes all professor information from persistent storage.
    :returns: true if the operation succeeds, false otherwise
    """
    mongodb = UnibrowserDAO(host=__host, port=__port)
    result = mongodb.delete(collection=__collection)
    return result >= 0
