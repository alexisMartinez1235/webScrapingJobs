import functools
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.remote.webelement import WebElement

# from bs4 import BeautifulSoup
import os
import time

screenshotDir = "webScrapingJobs/collect/screenshot/"

def logger(func):
  @functools.wraps(func)
  def wrapper(self, *args, **kwargs):
    print("Calling {}".format(func.__name__))
    val = func(self, *args, **kwargs)
    return val
  return wrapper

def skip_create_account(func):
  @logger
  @functools.wraps(func)
  def wrapper(self, *args, **kwargs):
    val = 0
    finder = Finder.instance()

    try:
      val = func(self, *args, **kwargs)
    except NoSuchElementException as elementNotFound:
      print(elementNotFound.msg)
      time.sleep(2)
      wrapper(self, *args, **kwargs)
      
    except WebDriverException as sessionCrashed:
      print("session crashed")
      print(sessionCrashed.msg)
      time.sleep(2)

      wrapper(self, *args, **kwargs)
    except Exception as err:
      print(err)
    
    elementCreateAccountList = finder.driver.find_elements(
      By.XPATH,
      open("webScrapingJobs/collect/xpathSignin.txt","r").read()
    )

    if len(elementCreateAccountList) > 0:
      print("create account filter")

      finder.driver.save_screenshot(finder.get_screenshot_path("logs/create_account_message.png"))
      finder.driver.back()
      val = func(self, *args, **kwargs)  
    
    finder.driver.save_screenshot(finder.get_screenshot_path("logs/screenshot_{}.png".format(finder.logID)))
    finder.logID+=1

    return val
    
  return wrapper

class Finder:
  _instance = None

  @classmethod
  def instance(cls):
      if cls._instance is None:
          print('Creating new instance')
          cls._instance = Finder()
      return cls._instance
  
  def __init__(self) -> None:
    self.logID=1
    self.driver = webdriver.Remote(
      "http://chromedriver:4444/wd/hub", DesiredCapabilities.CHROME
    )
    self.driver.maximize_window()
    self.driver.implicitly_wait(10)

    self.driver.get("https://www.linkedin.com/jobs/search")

  @skip_create_account
  def write_keyword(self, keyword):
    searchKeyword = self.driver.find_element(By.NAME, "keywords")
    searchKeyword.clear()
    searchKeyword.send_keys(keyword)
    searchKeyword.send_keys(Keys.ARROW_LEFT)

    # self.waitElement(By.ID, "keywords-1").click()
    self.driver.find_element(By.ID, "keywords-1").click()
  
  @skip_create_account
  def write_location(self, location):
    # Enter Your location
    locationKeyword = self.driver.find_element(By.NAME, "location")
    locationKeyword.clear()
    locationKeyword.send_keys(location)
    locationKeyword.send_keys(Keys.ARROW_LEFT)

    # self.driver.find_element(By.ID, "locations-1").click()

    locationKeyword.send_keys(Keys.ARROW_DOWN)
    locationKeyword.send_keys(Keys.ENTER)

  def get_screenshot_path(self, file_name="search.png"):
    return screenshotDir + file_name

  def __del__(self):
    Finder.instance().driver.quit()

if __name__ == "__main__":
  finder = Finder()
