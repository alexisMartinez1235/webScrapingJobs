from collect.Finder import Finder
from collect.JobPost import JobPostCollect
from element.JobPost import JobPost

finder = Finder("linkedin", "https://www.linkedin.com/jobs/search")

try:
  
  finder.write_keyword("backend")
  finder.write_location("Montevideo, Montevideo, Uruguay")

  jobCollect = JobPostCollect()
  jobs: 'list[JobPost]'= jobCollect.get_jobs()
  for job in jobs:
    job.append().save().save_on_database()
  
  del finder

except KeyboardInterrupt:
  del finder

