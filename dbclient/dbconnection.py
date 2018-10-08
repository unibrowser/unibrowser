# connection.py
from pymongo import MongoClient


class DbConnection:
    """
    Contains dbclient related functions.
    """
    HOST = 'localhost'
    PORT = 27017
    DB = "test"

    def __init__(self, host=None, port=None, db=None):
        if host is None:
            host = self.HOST
        if port is None:
            port = self.PORT
        if db is None:
            db = self.DB

        try:
            client = MongoClient(host, port)
            self.db = client[db]
        except:
            print("Error occured in getting a client or collection")

    def add_data(self, collection):
        """
        Adds data to the collection
        :param collection: collection of items
        :return:
        """
        if isinstance(collection, list):
            self.db.examples.insert_many(collection)
        else:
            self.db.examples.insert_one(collection)

    def get_all(self):
        """
        Gets all the informations
        :return: list of items
        """
        examples = self.db.examples
        cursor = examples.find({})
        return list(cursor)


if __name__ == '__main__':
    connection = DbConnection()
    collection = {
        'name': 'example 1',
        'id': '1'
    }
    connection.add_data(collection)
    entries = connection.get_all()
    for entry in entries:
        print(entry)
