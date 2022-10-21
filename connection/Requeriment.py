from connection.Csv import CsvConnection

class Requeriment(CsvConnection):
  def __init__(self, name: str) -> None:
    
    CsvConnection.__init__(self, "Requeriment.csv", ["name"], False)
    self.name = name
    self.relatedWithList = []
  
  def relatedWith(self, requeriment):
    self.relatedWithList.append(requeriment)
  