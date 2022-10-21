import unittest
from connection.JobPost import JobPostConnection

class Test_JobPost(unittest.TestCase):
  example = {
    "company": None,
    "title": "title example",
    "description": "description text, |. ,\n\n lorem lorem\n lorem lorem",
    "salary": None,
    "dateInit": None,
    "dateEnd": None,
    "location": None,
  }
  def test_create_job_example(self):
   
    jobPostTest = JobPostConnection(True)
    jobPostTest.load_file()
    
    beforeLenJobPostTest = len(jobPostTest.df)

    jobPostTest.append(Test_JobPost.example)
    jobPostTest.save()
    self.assertGreaterEqual(len(jobPostTest.df), beforeLenJobPostTest + 1)
    return jobPostTest
  
  def test_save_on_database(self):
    jobPostTest = JobPostConnection(True)
    jobPostTest.append(Test_JobPost.example)
    jobPostTest.save().save_on_database("test")

  def test_clear_df(self):
    jobPostTest = self.test_create_job_example()
    jobPostTest.clear().save()
    self.assertEqual(len(jobPostTest.df), 0)

if __name__ == '__main__':
  unittest.main()