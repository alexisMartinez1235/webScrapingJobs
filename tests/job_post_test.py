import unittest
from element.JobPost import JobPost

class Test_JobPost(unittest.TestCase):
  example = {
    "company": None,
    "title": "title example",
    "description": "description text, |.",
    "salary": None,
    "dateInit": None,
    "dateEnd": None,
    "location": None,
  }
  def test_create_job_example(self):
   
    jobPostTest = JobPost(Test_JobPost.example, True)
    jobPostTest.append().save()
    self.assertGreaterEqual(len(jobPostTest.df), 1)
    return jobPostTest
  
  def test_save_on_database(self):
    jobPostTest = JobPost(Test_JobPost.example, True)
    jobPostTest.append().save().save_on_database("test")

  def test_clear_df(self):
    jobPostTest = self.test_create_job_example()
    jobPostTest.clear().save()
    self.assertEqual(len(jobPostTest.df), 0)

if __name__ == '__main__':
  unittest.main()