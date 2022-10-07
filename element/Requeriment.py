from element.CsvElement import CsvElement

class Requeriment(CsvElement):
  def __init__(self, name: str) -> None:
    
    CsvElement.__init__(self, "Requeriment.csv", ["name"])
    self.name = name
    self.relatedWithList = []
  
  def relatedWith(self, requeriment):
    self.relatedWithList.append(requeriment)
  