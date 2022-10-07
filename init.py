from collect.Finder import Finder
from collect.JobPost import JobPostCollect
from element.JobPost import JobPost

finder = Finder()
finder.write_keyword("backend")
finder.write_location("Montevideo, Montevideo, Uruguay")

jobCollect = JobPostCollect()
jobs: 'list[JobPost]'= jobCollect.get_jobs()
for job in jobs:
  job.append().save()
  

del finder
