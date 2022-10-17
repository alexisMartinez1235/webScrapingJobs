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

class CsvElement:
  data: dict
  csv_file: str
  headerList: list
  inTesting: bool

  def __init__(self, data: dict, csv_file: str, headerList: list, inTesting: bool):
    self.data = data
    self.csv_file = csv_file
    self.headerList = headerList
    self.inTesting = inTesting

    self.csvDir = prodCsvDir
    
    if inTesting:
      self.csvDir = testCsvDir

    # create if not exists
    if not os.path.isfile(self.csvDir + csv_file):
      pd.DataFrame(columns=headerList).to_csv(self.csvDir + csv_file, index=False, sep="|")
    self.df = pd.read_csv(self.csvDir + csv_file, sep="|")

  def append(self):
    
    for key in self.data:
      if isinstance(self.data[key], str):
        self.data[key] = self.data[key].replace("|", ".")

    self.df = self.df.append(self.data, ignore_index=True)
    # self.df.to_csv(csvDir + self.csv_file, index=False, mode='w')
    return self

  def clear(self):
    self.df = self.df.head(0)
    return self

  def save(self):
    self.df.to_csv(self.csvDir + self.csv_file, index=False, mode='w', sep="|")
    return self
    
  @abc.abstractmethod
  def save_on_database(self, collection: str="test") -> InsertOneResult:
    return Database().get_collection(collection).insert_one(self.data.copy())