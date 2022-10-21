import unittest
from database.Database import Database
from bson.json_util import dumps, loads

from connection.Csv import CsvConnection

class Test_Database(unittest.TestCase):
  def test_database_connection(self):
    exampleElement = CsvConnection("test.csv", ["message"], True)
    exampleElement.append({
      "message": "hello world"
    })

    jobPostCollection = Database().get_collection('test')
    response_insert = exampleElement.save().save_on_database()

    savedDocument = jobPostCollection.find({
      "_id": response_insert.inserted_id,
    }, {
      "_id": 0,
      "message": 1,
    })
    savedDocument = loads(dumps(savedDocument))
    self.assertEqual(savedDocument[0], exampleElement.data)

    return exampleElement

  def test_clear_df(self):
    exampleElement = self.test_database_connection()
    exampleElement.clear()

    _delete_response = Database().get_collection('test').delete_many({})

    self.assertEqual(len(exampleElement.df), 0)

if __name__ == '__main__':
  unittest.main()