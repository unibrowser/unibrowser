# mongoclienttestcase.py
import unittest

from database.mongoclientclass import MongoClientClass


class MongoClientTestCase(unittest.TestCase):
    def setUp(self):
        self.mongoClientInstance = MongoClientClass()

    def tearDown(self):
        self.mongoClientInstance = None

    def test_instance_working(self):
        sample_document = {
            'name': 'example 1',
            'id': '1'
        }

        # test case for insert
        res = self.mongoClientInstance.insert(documents=[sample_document])
        self.assertEqual(1, res, "Error inserting documents")

        # test case for find
        document = self.mongoClientInstance.find(options={'id': '1'})
        self.assertEqual(1, len(document), "Got more than one document when only one document is expected")
        self.assertDictEqual(sample_document, document[0], "Obtained document do not match the input")

        res = self.mongoClientInstance.delete(options={'id': '1'})
        self.assertEqual(1, res, "Deleted %d documents instead of 1 document" % res)


if __name__ == '__main__':
    # run mongoclientclass.py to clear the testing database
    unittest.main()
