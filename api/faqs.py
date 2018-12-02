"""
FAQ Unibrowser API
"""
from typing import List
from database.dao import UnibrowserDAO

__collection: str = 'faqs'
__host: str = 'localhost'
__port: int = 27017


class Faq(object):
    """
    Represents a question/answer pair
    """

    def __init__(self, title: str = None, link: str = None, tags: List[str] = None, answer: str = None):
        self.title = title
        self.link = link
        self.tags = tags
        self.answer = answer

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


def insert(faq: Faq) -> bool:
    """
    Inserts a single FAQ object in Unibrowser's persistent storage.
    :param faq: the FAQ to insert
    :returns: true if the insert succeeds, false otherwise
    """
    mongodb = UnibrowserDAO(host=__host, port=__port)
    result = mongodb.insert(collection=__collection, documents=[faq.to_object()])
    return result == 1


def insert_many(faqs: List[Faq]) -> bool:
    """
    Inserts multiple FAQ objects in Unibrowser's persistent storage.
    :param faqs: the list of FAQs to insert
    :returns: true if the insert succeeds, false otherwise
    """
    mongodb = UnibrowserDAO(host=__host, port=__port)
    result = mongodb.insert(collection=__collection, documents=map(Faq.to_object, faqs))
    return result == 1


def clear() -> bool:
    """
    Completely removes all FAQ information from persistent storage.
    :returns: true if the operation succeeds, false otherwise
    """
    mongodb = UnibrowserDAO(host=__host, port=__port)
    results = mongodb.delete(collection=__collection)
    return results >= 0
