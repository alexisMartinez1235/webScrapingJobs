from datetime import date
from collect.Finder import Finder, skip_create_account
from element._Company import Company
from element.JobPost import JobPost
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import ActionChains
import random

class JobPostCollect():
 
  def __init__(self) -> None:
    pass
  
  @skip_create_account
  def get_jobpost_list(self) -> list:
    jobListUl = Finder.instance().driver.find_elements(By.TAG_NAME, "ul")[6]
    jobListUl.screenshot(Finder.instance().get_screenshot_path("job_list_ul.png"))
    jobList = jobListUl.find_elements(By.TAG_NAME, "li")
    return [ jobList, jobListUl ]  
  
  @skip_create_account
  def select_jobpost(self, jobList, number: int) -> JobPost:
    jobList[number].click()
    jobPost = Finder.instance().driver.find_element(By.CLASS_NAME, "two-pane-serp-page__detail-view")
    titleElement = jobPost.find_element(By.TAG_NAME, "h2")
    jobPost.find_element(
        By.XPATH,
        "//*[contains(text(), 'Show more')]"
    ).click()
    descriptionElement = jobPost.find_element(By.CLASS_NAME, "show-more-less-html__markup")

    return JobPost(
        None,
        titleElement.text,
        descriptionElement.text,
        None,
        None,
        None
      )

  @skip_create_account
  def get_jobs(self, y_size_post_element = 180, max=4, err_num=10) -> 'list[JobPost]':
    jobListItem, jobListUl = self.get_jobpost_list()
    action = ActionChains(Finder.instance().driver)

    jobList = []
    for i in range(0, max):
      jobList.append(self.select_jobpost(jobListItem, i))
      action.move_to_element(jobListUl).perform()
      # action.scroll_by_amount(0, y_size_post_element)
      Finder.instance().driver.execute_script("window.scrollTo(0,{})".format(random.gauss(y_size_post_element * i, err_num)))

    return jobList