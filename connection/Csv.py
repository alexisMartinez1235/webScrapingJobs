import csv
import pandas as pd
import os
# from dataclasses import dataclass
import abc

from pymongo.results import (
    InsertOneResult,
)
from database.Database import Database

prodCsvDir = "collect/csv/"
testCsvDir = "tests/csv/"

class CsvConnection:

  def __init__(self, csv_file: str, headerList: list, inTesting: bool):
    self.csv_file = csv_file
    self.headerList = headerList
    self.inTesting = inTesting

    self.csvDir = prodCsvDir    
    if inTesting:
      self.csvDir = testCsvDir
    # self.load_file()
  
  def load_file(self):
    # create if not exists
    if not os.path.isfile(self.csvDir + self.csv_file):
      pd.DataFrame(columns=self.headerList).to_csv(self.csvDir + self.csv_file, index=False, sep="|")
    self.df = pd.read_csv(self.csvDir + self.csv_file, sep="|")
  
  
  def append(self, data):
    
    for key in data:
      if isinstance(data[key], str):
        data[key] = data[key].replace("|", ".")

    self.df = self.df.append(data, ignore_index=True)
    self.data = data
    # self.df.to_csv(csvDir + self.csv_file, index=False, mode='w')
    return data
  
  def clear(self):
    self.df = self.df.head(0)
    return self
  
  def save(self):
    self.df.to_csv(self.csvDir + self.csv_file, index=False, mode='w', sep="|")
    return self
    
  @abc.abstractmethod
  def save_on_database(self, collection: str="test") -> InsertOneResult:
    return Database().get_collection(collection).insert_one(self.data.copy())