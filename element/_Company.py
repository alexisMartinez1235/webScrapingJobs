
from element.CsvElement import CsvElement


class Company(CsvElement):
  def __init__(self, name: str, description: str):
    CsvElement.__init__(self, "Company.csv")
    self.name = name
    self.description = description