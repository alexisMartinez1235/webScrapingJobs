# from Requeriment import Requeriment
from connection.Csv import CsvConnection

class Person(CsvConnection):
  def __init__(self):
    CsvConnection.__init__(self, "Person.csv", ["predictedAge"], False)

    self.requeriments = []
  
  def predictRequeriments(self):
    pass