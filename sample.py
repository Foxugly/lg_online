#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

dir = os.path.dirname(os.path.abspath(__file__))
driver = webdriver.Chrome(os.path.join(dir,'chromedriver'))
driver.get('http://www.google.com')
search = driver.find_element_by_name('q')
search.send_keys("google search through python")
search.send_keys(Keys.RETURN)
time.sleep(10)
driver.close()
driver.quit()
