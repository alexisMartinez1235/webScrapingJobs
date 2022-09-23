import csv

csvDir = "webScrapingJobs/collect/csv/"

class CsvElement:
  def __init__(self, csv_file):
    self.csv_file= csv_file

  def save_in_csv(self, data: list):
    with open(csvDir + self.csv_file, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(data)