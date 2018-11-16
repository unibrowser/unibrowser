from pymongo import MongoClient
from pymongo.results import InsertManyResult


class UnibrowserDAO(object):

    # Default Mongo DB configuration for the database access object
    __dbname: str = 'unibrowser'
    __host: str = 'localhost'
    __port: int = 27017
    __collection: str = 'test'

    # We could have a pool of available database client connections as well, but we don't want to over-engineer
    # the helper module
    __client = None

    def __init__(self, host: str = None, port: int = None, dbname: str = None, collection: str = None):
        if host is not None:
            self.__host = host
        if port is not None:
            self.__port = port
        if dbname is not None:
            self.__dbname = dbname
        if collection is not None:
            self.__collection = collection
        self.__client = MongoClient(self.__host, self.__port)[self.__dbname]

    def insert(self, collection=None, documents=[]):
        """
        Inserts given documents in the related collection
        :param collection: collection in the database
        :param documents: documents to be inserted
        :return: 1 if insert is successful otherwise 0
        """
        if collection is None:
            collection = self.__collection

        res = self.__client[collection].insert_many(documents)

        if isinstance(res, InsertManyResult):
            return 1
        return 0

    def find(self, collection=None, options={}):
        """
        Finds all documents in the given collection.
        :param collection: collection in the database
        :param options: filter query
        :return: document list
        """
        if collection is None:
            collection = self.__collection
        cursor = self.__client[collection].find(options)
        return list(cursor)

    def delete(self, collection=None, options={}):
        """
        Delete the filtered elements based on options from the given collection.
        :param collection: name of the collection
        :param options: filter query
        :return: count of the deleted items
        """
        if collection is None:
            collection = self.__collection
        result = self.__client[collection].delete_many(options)
        return result.deleted_count
