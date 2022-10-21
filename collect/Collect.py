from collect.Finder import Finder
from collect.JobPost import JobPostCollect
from connection.JobPost import JobPostConnection

def generatePasskeyIfNotExists():
  return JobPostCollect(JobPostConnection())

def searchJobs(keyword, location, maxElement):
  finder = Finder("linkedin", "https://www.linkedin.com/jobs/search")

  try:
    finder.write_keyword(keyword)
    finder.write_location(location)

    # create connection to csv file
    job_post_connection = JobPostConnection()
    job_post_connection.load_file()
    
    # create job collector class
    job_collect = JobPostCollect(job_post_connection)

    # collect data
    job_collect.collect_jobs(maxElement)

    # save data in file and send to database
    job_post_connection.save().save_on_database()
    del finder

  except KeyboardInterrupt:
    del finder
