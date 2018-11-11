# mongoclientclass.py
from pymongo import MongoClient
from pymongo.results import InsertManyResult
from config import DATABASE_CONFIG


class MongoClientClass:
    """
    Contains database related functions.
    """
    HOST = DATABASE_CONFIG['host']
    PORT = DATABASE_CONFIG['port']
    DB = DATABASE_CONFIG['dbname']
    COLLECTION = 'examples'

    def __init__(self, host=None, port=None, db=None):
        if host is None:
            host = self.HOST
        if port is None:
            port = self.PORT
        if db is None:
            db = self.DB

        client = MongoClient(host, port)
        self.db = client[db]

    def insert(self, collection=None, documents=[]):
        """
        Inserts given documents in the related collection
        :param collection: collection in the database
        :param documents: documents to be inserted
        :return: 1 if insert is successful otherwise 0
        """
        if collection is None:
            collection = self.COLLECTION

        res = self.db[collection].insert_many(documents)

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
            collection = self.COLLECTION

        db_collection = self.db[collection]
        cursor = db_collection.find(options)
        return list(cursor)

    def delete(self, collection=None, options={}):
        """
        Delete the filtered elements based on options from the given collection.
        :param collection: name of the collection
        :param options: filter query
        :return: count of the deleted items
        """
        if collection is None:
            collection = self.COLLECTION

        db_collection = self.db[collection]
        result = db_collection.delete_many(options)
        return result.deleted_count


if __name__ == '__main__':
    mongoClientInstance = MongoClientClass()
    sample_document = {
        'name': 'example 1',
        'id': '1'
    }
    mongoClientInstance.insert(documents=[sample_document])
    entries = mongoClientInstance.find()
    for entry in entries:
        print(entry)
    res = mongoClientInstance.delete(options={'id': '1'})
    print("Deleted %d items from the collection" % res)
