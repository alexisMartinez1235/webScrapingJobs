import functools
from datetime import date
from collect.Finder import Finder, skip_create_account_with_limit
from connection._Company import Company
from connection.JobPost import JobPostConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import ActionChains
from cryptocode import encrypt, decrypt
import os
import secrets

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
      print(err)
      Finder.__new__(Finder).scroll_to_item_list(action, jobListUl, y_size_post_element, itemNum - 1, err_scroll)
      Finder.__new__(Finder).scroll_to_item_list(action, jobListUl, y_size_post_element, itemNum, err_scroll)

      val = func(self, *args)
    return val
  return wrapper

class JobPostCollect:
  
  def __init__(self, job_post_element: JobPostConnection) -> None:
    self.pass_file = "collect/passkey.txt"
    self.job_post_element = job_post_element
    # create passfile if not exits
    if not os.path.isfile(self.pass_file):
      with open(self.pass_file, "w+") as text_file:
        text_file.write(secrets.token_urlsafe(32))
    else:        
      print("passkey already exists")

    self.pass_key = open(self.pass_file, "r").read()  

  @skip_create_account_with_limit(3, False)
  def get_jobpost_list(self):
    jobListUl = Finder.__new__(Finder).driver.find_elements(By.TAG_NAME, "ul")[6]
    # jobListUl.screenshot(self.get_screenshot_path("job_list_ul.png"))
    
    return jobListUl

  @skip_create_account_with_limit(3)
  @autoscroll
  def select_jobpost(self, action, jobListUl, jobList, itemNum: int, y_size_post_element: int, err_scroll: int) -> dict:
    jobPost_element = jobList[itemNum]
    jobPost_element.click()

    id_jobpost = Finder.__new__(Finder).json["id_jobpost"]
    div_entity = jobPost_element.find_element(By.XPATH, "//*[@{}]".format(id_jobpost))
    id_jobpost_text = div_entity.get_attribute(id_jobpost)
    
    time.sleep(1)
    
    job_post = Finder.__new__(Finder).driver.find_element(By.CLASS_NAME, Finder.__new__(Finder).json["job_post_classname"])
    job_post.send_keys(Keys.NUMPAD7)

    id_enterprise_element = job_post.find_element(By.CLASS_NAME, Finder.__new__(Finder).json["id_enterprise"])
    location_element = job_post.find_element(By.CLASS_NAME, Finder.__new__(Finder).json["class_name_location"])
    title_element = job_post.find_element(By.TAG_NAME, "h2")
    aplication_count_element = job_post.find_element(By.CLASS_NAME, Finder.__new__(Finder).json["job_post_applicant_count_classname"])
    since_element = job_post.find_element(By.CLASS_NAME, Finder.__new__(Finder).json["job_post_since_classname"])

    time.sleep(1)
    
    job_post.find_element(
        By.XPATH,
        Finder.__new__(Finder).json["show_more_xpath"]
    ).click()

    description_element = job_post.find_element(By.CLASS_NAME, Finder.__new__(Finder).json["description_classname"])
    time.sleep(1)

    return self.job_post_element.append({
        "id_jobpost": encrypt(id_jobpost_text, self.pass_key), # doesnt work fine
        "id_company": encrypt(id_enterprise_element.text, self.pass_key),
        "title": title_element.text,
        "description": description_element.text,
        "salary": None,
        "since": since_element.text,
        "application_count": aplication_count_element.text,
        "date": time.time(),
        "location": location_element.text,
      })

  @skip_create_account_with_limit(3)
  def collect_jobs(self, max, y_size_post_element: int = 180, err_num=10) -> 'list[dict]':
    jobListUl = self.get_jobpost_list()

    action = ActionChains(Finder.__new__(Finder).driver)

    jobList = []
    i = 0
    while max is None or i < max:
      try:
        jobListElements = jobListUl.find_elements(By.TAG_NAME, "li")
        time.sleep(2)

        jobList.append(self.select_jobpost(action, jobListUl, jobListElements, i, y_size_post_element, err_num))
        i+=1
      except Exception as err:
        print(err)
        print("Ending")
        break
  
    return jobList