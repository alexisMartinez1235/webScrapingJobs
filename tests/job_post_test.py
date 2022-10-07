import unittest
from element.JobPost import JobPost
import logging

class Test_JobPost(unittest.TestCase):
  def test_create_job_example(self):
    example = {
      "company": None,
      "title": "title example",
      "description": "description text.",
      "salary": None,
      "dateInit": None,
      "dateEnd": None,
    }
    jobPostTest = JobPost(example, True)
    jobPostTest.append().save()
    
    self.assertGreaterEqual(len(jobPostTest.df), 1)
    return jobPostTest

  def test_clear_df(self):
    jobPostTest = self.test_create_job_example()
    jobPostTest.clear()
    jobPostTest.save()

    self.assertEqual(len(jobPostTest.df), 0)

if __name__ == '__main__':
  unittest.main()