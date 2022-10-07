
from datetime import date
from element._Company import Company
from element.Requeriment import Requeriment
from element.CsvElement import CsvElement

class JobPost(CsvElement): # Company # date # int
  def __init__(self, data: dict, inTesting: bool = False):
    CsvElement.__init__(self, data, "JobPost.csv", [
      "company",
      "title",
      "description",
      "salary",
      "dateInit",
      "dateEnd",
    ], inTesting)
    self.requeriments = []
  
  def predictRequeriments(self, requeriments: Requeriment):
      self.requeriments = requeriments
