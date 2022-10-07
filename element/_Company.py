
from element.CsvElement import CsvElement


class Company(CsvElement):
  def __init__(self, data: dict, name: str, description: str):
    CsvElement.__init__(self, data, "Company.csv", ["name", "description"], False)
    self.name = name
    self.description = description