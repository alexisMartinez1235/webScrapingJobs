import unittest
from database.Database import Database
import logging
from bson.json_util import dumps, loads

class Test_Database(unittest.TestCase):
  def test_database_connection(self):
    database = Database()
    example = {
      "message": "hello world"
    }
    jobPostCollection = database.get_collection('test')
    response_insert = jobPostCollection.insert_one(example.copy())
    savedDocument = jobPostCollection.find({
      "_id": response_insert.inserted_id,
    }, {
      "_id": 0,
      "message": 1,
    })
    savedDocument = loads(dumps(savedDocument))
    self.assertEqual(savedDocument[0], example)


if __name__ == '__main__':
  unittest.main()