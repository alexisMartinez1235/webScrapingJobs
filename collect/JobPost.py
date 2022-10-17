import functools
from datetime import date
from collect.Finder import Finder, skip_create_account_with_limit
from element._Company import Company
from element.JobPost import JobPost
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import ActionChains

import random
import time

def autoscroll(func):
  @functools.wraps(func)
  def wrapper(self, *args):
    print("Calling autoscrool{}".format(func.__name__))
    val=0
    action, jobListUl, jobList, itemNum, y_size_post_element, err_scroll = args
    try:
      Finder.__new__(Finder).scroll_to_item_list(action, jobListUl, y_size_post_element, itemNum, err_scroll)
      val = func(self, *args)
    except Exception as err:
      Finder.__new__(Finder).scroll_to_item_list(action, jobListUl, y_size_post_element, itemNum - 1, err_scroll)
      Finder.__new__(Finder).scroll_to_item_list(action, jobListUl, y_size_post_element, itemNum, err_scroll)

      val = func(self, *args)

    return val
  return wrapper

class JobPostCollect:
  
  @skip_create_account_with_limit(3, False)
  def get_jobpost_list(self):
    jobListUl = Finder.__new__(Finder).driver.find_elements(By.TAG_NAME, "ul")[6]
    # jobListUl.screenshot(self.get_screenshot_path("job_list_ul.png"))
    
    return jobListUl

  @skip_create_account_with_limit(3)
  @autoscroll
  def select_jobpost(self, action, jobListUl, jobList, itemNum: int, y_size_post_element: int, err_scroll: int) -> JobPost:
    jobList[itemNum].click()
    time.sleep(1)

    jobPost = Finder.__new__(Finder).driver.find_element(By.CLASS_NAME, Finder.__new__(Finder).json["job_post_classname"])
    jobPost.send_keys(Keys.NUMPAD7)

    titleElement = jobPost.find_element(By.TAG_NAME, "h2")
    time.sleep(1)
    
    jobPost.find_element(
        By.XPATH,
        Finder.__new__(Finder).json["show_more_xpath"]
    ).click()
    descriptionElement = jobPost.find_element(By.CLASS_NAME, Finder.__new__(Finder).json["description_classname"])
    time.sleep(1)

    return JobPost({
        "company": None,
        "title": titleElement.text,
        "description": descriptionElement.text,
        "salary": None,
        "dateInit": None,
        "dateEnd": None,
        "location": None,
      })

  @skip_create_account_with_limit(3)
  def get_jobs(self, y_size_post_element = 180, max=4, err_num=10) -> 'list[JobPost]':
    jobListUl = self.get_jobpost_list()

    action = ActionChains(Finder.__new__(Finder).driver)

    jobList = []
    for i in range(0, max):
      jobListElements = jobListUl.find_elements(By.TAG_NAME, "li")
      time.sleep(2)

      jobList.append(self.select_jobpost(action, jobListUl, jobListElements, i, y_size_post_element, err_num))
  
    return jobList