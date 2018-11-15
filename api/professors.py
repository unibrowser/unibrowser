"""
Unibrowser Professors API
"""
from typing import List
from database.mongoclientclass import MongoClientClass
from config import PROFESSOR_CONFIG


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


def insert(prof: Professor) -> bool:
    """
    Inserts a single professor object in Unibrowser's persistent storage.
    :param p: the professor to insert
    :returns: true if the insert succeeds, false otherwise
    """
    mongodb = MongoClientClass()
    result = mongodb.insert(collection=PROFESSOR_CONFIG['db_collection'], documents=[prof.to_object()])
    return result == 1


def insert_many(profs: List[Professor]) -> bool:
    """
    Inserts multiple professor objects in Unibrowser's persistent storage.
    :param p: the list of professors to insert
    :returns: true if the insert succeeds, false otherwise
    """
    mongodb = MongoClientClass()
    result = mongodb.insert(collection=PROFESSOR_CONFIG['db_collection'], documents=map(Professor.to_object, profs))
    return result == 1


def clear() -> bool:
    """
    Completely removes all professor information from persistent storage.
    :returns: true if the operation succeeds, false otherwise
    """
    mongodb = MongoClientClass()
    result = mongodb.delete(collection=PROFESSOR_CONFIG['db_collection'])
    return result >= 0
