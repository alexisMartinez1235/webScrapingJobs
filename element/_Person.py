# from Requeriment import Requeriment
from element.CsvElement import CsvElement

class Person(CsvElement):
  def __init__(self, data: dict):
    CsvElement.__init__(self, data, "Person.csv", ["predictedAge"], False)
    
    self.requeriments = []
  
  def predictRequeriments(self):
    pass