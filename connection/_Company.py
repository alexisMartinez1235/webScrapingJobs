
from connection.Csv import CsvConnection

print()

class Company(CsvConnection):
  def __init__(self, name: str, description: str):
    CsvConnection.__init__(self, "Company.csv", ["name", "description"], False)
    self.name = name
    self.description = description