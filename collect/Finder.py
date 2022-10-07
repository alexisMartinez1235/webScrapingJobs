import functools
import random

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

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

screenshotDir = "collect/screenshot/"

def logger(func):
  @functools.wraps(func)
  def wrapper(self, *args): #, **kwargs):
    print("Calling {}".format(func.__name__))
    val = func(self, *args) # , **kwargs)
    return val
  return wrapper

def skip_create_account_with_limit(numRetries, takeScreenshot=True):
  def skip_create_account(func):
    @logger
    @functools.wraps(func)
    def wrapper(self, *args): #, **kwargs):
      val = 0
      for _countEntries in range(0, numRetries):
        time.sleep(1)

        try:
          val = func(self, *args) #, **kwargs)
          elementCreateAccountList = self.driver.find_elements(
            By.XPATH,
            open("collect/xpathSignin.txt","r").read()
          )

          if len(elementCreateAccountList) > 0:
            print("create account filter")

            if takeScreenshot:
              self.driver.save_screenshot(self.get_screenshot_path("logs/create_account_message.png"))
            
            self.driver.back()
            val = func(self, *args) # , **kwargs)  
          
          if takeScreenshot:
            self.driver.save_screenshot(self.get_screenshot_path("logs/screenshot_{}.png".format(self.screenshot_id)))
          
          self.screenshot_id+=1
          return val

        except NoSuchElementException as elementNotFound:
          print(elementNotFound.msg)
        except WebDriverException as sessionCrashed:
          print("session crashed")
          print(sessionCrashed.msg)

        except Exception as err:
          print(err)
      else:
        return Exception("you have reached the maximum number of retries")

    return wrapper
  return skip_create_account

class Finder(object):
  _instance = None
  screenshot_id: int
  driver: WebDriver
  chrome_options: Options

  def __new__(cls):
    if cls._instance is None:
      print('Creating new instance')
      # cls._instance = Finder()
      cls._instance = super(Finder, cls).__new__(cls)
    return cls._instance
  
  def __init__(self) -> None:
    self.screenshot_id=1
        
    self.chrome_options = webdriver.ChromeOptions()
    # self.chrome_options.add_argument('--headless')
    # self.chrome_options.add_argument('--no-sandbox') 
    
    self.driver = webdriver.Remote(
      "http://chromedriver:4444/wd/hub",
      DesiredCapabilities.CHROME,
      options=self.chrome_options,
    )
    self.driver.maximize_window()
    self.driver.implicitly_wait(10)

    self.driver.get("https://www.linkedin.com/jobs/search")

  @skip_create_account_with_limit(3, False)
  def write_keyword(self, keyword):
    searchKeyword = self.driver.find_element(By.NAME, "keywords")
    searchKeyword.clear()
    searchKeyword.send_keys(keyword)
    searchKeyword.send_keys(Keys.ARROW_LEFT)

    # self.waitElement(By.ID, "keywords-1").click()
    self.driver.find_element(By.ID, "keywords-1").click()
  
  @skip_create_account_with_limit(3, False)
  def write_location(self, location):
    # Enter Your location
    locationKeyword = self.driver.find_element(By.NAME, "location")
    locationKeyword.clear()
    locationKeyword.send_keys(location)
    locationKeyword.send_keys(Keys.ARROW_LEFT)

    # self.driver.find_element(By.ID, "locations-1").click()

    locationKeyword.send_keys(Keys.ARROW_DOWN)
    locationKeyword.send_keys(Keys.ENTER)

  def scroll_to_item_list(self, action, html_list, y_size_post_element: int, itemNum: int, err_scroll: int):
    action.move_to_element(html_list).perform()
    scriptScroll ="window.scrollTo(0,{})".format(random.gauss(y_size_post_element * itemNum, err_scroll))
    self.driver.execute_script(scriptScroll)
  
  def get_screenshot_path(self, file_name="search.png"):
    return screenshotDir + file_name

  def __del__(self):
    self.driver.quit()

if __name__ == "__main__":
  finder = Finder()
