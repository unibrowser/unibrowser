"""
FAQ Unibrowser API
"""
from typing import List
from config import FAQ_CONFIG
from database.mongoclientclass import MongoClientClass


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


def insert(faq: Faq) -> bool:
    """
    Inserts a single FAQ object in Unibrowser's persistent storage.
    :param faq: the FAQ to insert
    :returns: true if the insert succeeds, false otherwise
    """
    mongodb = MongoClientClass()
    result = mongodb.insert(collection=FAQ_CONFIG['db_collection'], documents=[faq.to_object()])
    return result == 1


def insert_many(faqs: List[Faq]) -> bool:
    """
    Inserts multiple FAQ objects in Unibrowser's persistent storage.
    :param faqs: the list of FAQs to insert
    :returns: true if the insert succeeds, false otherwise
    """
    mongodb = MongoClientClass()
    result = mongodb.insert(collection=FAQ_CONFIG['db_collection'], documents=map(Faq.to_object, faqs))
    return result == 1


def clear() -> bool:
    """
    Completely removes all FAQ information from persistent storage.
    :returns: true if the operation succeeds, false otherwise
    """
    mongodb = MongoClientClass()
    results = mongodb.delete(collection=FAQ_CONFIG['db_collection'])
    return results >= 0
