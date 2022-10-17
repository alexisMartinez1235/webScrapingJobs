
from datetime import date
from element._Company import Company
from element.Requeriment import Requeriment
from element.CsvElement import CsvElement
from database.Database import Database

class JobPost(CsvElement): # Company # date # int
  def __init__(self, data: dict, inTesting: bool = False):
    CsvElement.__init__(self, data, "JobPost.csv", [
      "company",
      "title",
      "description",
      "salary",
      "dateInit",
      "dateEnd",
      "location",
    ], inTesting)
    self.data = data
    self.requeriments = []
  
  def predictRequeriments(self, requeriments: Requeriment):
      self.requeriments = requeriments

  def save_on_database(self, collection:str = "JobPost"):
     return super().save_on_database(collection)
  