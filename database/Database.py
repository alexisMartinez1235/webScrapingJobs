import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.collection import Collection
import os

databaseName = str(os.getenv("MONGO_INITDB_DATABASE"))
rootUser = str(os.getenv("MONGO_INITDB_ROOT_USERNAME"))
passwordFile = str(os.getenv("MONGO_INITDB_ROOT_PASSWORD_FILE"))
password = open(passwordFile, "r").read().splitlines()[0]

class Database(object):
  _instance=None
  URI: str = "mongodb://{}:{}@mongo:27017/?authMechanism=DEFAULT".format(rootUser, password)
  client: MongoClient 

  def __new__(cls):
    if cls._instance is None:
      print('Creating new instance')
      cls._instance = super(Database, cls).__new__(cls)
    return cls._instance

  def __init__(self):
    self.client = MongoClient(self.URI)
    self.database = self.client[databaseName]
    
  def get_collection(self, collection: str) -> Collection:
    return self.database[collection]
  
  