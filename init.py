# from collect.Finder import Finder
from collect.JobPost import JobPostCollect
# from connection.JobPost import JobPost
from collect.Collect import generatePasskeyIfNotExists, searchJobs

if __name__ == "__main__":
  # generatePasskeyIfNotExists()
  searchJobs("backend", "Montevideo, Montevideo, Uruguay", maxElement=4)
