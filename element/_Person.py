# from Requeriment import Requeriment
from element.CsvElement import CsvElement

class Person(CsvElement):
  def __init__(self, predictedAge: int):
    CsvElement.__init__(self, "Person.csv")
    
    self.predictedAge = predictedAge
    self.requeriments = []
  
  def predictRequeriments(self):
    pass