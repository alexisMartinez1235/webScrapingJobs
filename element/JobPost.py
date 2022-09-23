
from datetime import date
from element._Company import Company
from element.Requeriment import Requeriment
from element.CsvElement import CsvElement

class JobPost(CsvElement): # Company # date # int
  def __init__(self, company: object, title: str, description: str, salary: object, dateInit: object, dateEnd: object):
    CsvElement.__init__(self, "JobPost.csv")
    
    self.company = company
    self.title = title
    self.description = description
    self.salary = salary
    self.dateInit = dateInit
    self.dateEnd = dateEnd
    self.requeriments = []
  
  def predictRequeriments(self, requeriments: Requeriment):
      self.requeriments = requeriments
    