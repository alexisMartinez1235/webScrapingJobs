
from datetime import date
from connection._Company import Company
from connection.Requeriment import Requeriment
from connection.Csv import CsvConnection
from database.Database import Database

class JobPostConnection(CsvConnection): # Company # date # int
  def __init__(self, inTesting: bool = False):
    CsvConnection.__init__(self, "JobPost.csv", [
      "id_jobpost",
      "id_company",
      "title",
      "description",
      "salary",
      "since",
      "application_count",
      "date",
      "location"
    ], inTesting)
    self.requeriments = []
  
  def predictRequeriments(self, requeriments: Requeriment):
      self.requeriments = requeriments

  def save_on_database(self, collection:str = "JobPost"):
    try:
      return super().save_on_database(collection)
    except Exception as err:
      print(err)