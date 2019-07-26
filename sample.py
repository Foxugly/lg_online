#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os


dir = os.path.dirname(os.path.abspath('__file__'))
driver = webdriver.Chrome()
driver.get('http://www.mylieutenantguillaume.com')
search = driver.find_element_by_name('subscribe')
search.click()
search = driver.find_element_by_name('email')
search.send_keys("test_mlg_acc@yopmail.com")
search = driver.find_element_by_name('first_name')
search.send_keys("John")
search = driver.find_element_by_name('last_name')
search.send_keys("Smith")
search = driver.find_element_by_name('password1')
search.send_keys("azerty123")
search = driver.find_element_by_name('password2')
search.send_keys("azerty123")
time.sleep(10)
search = driver.find_element_by_name('submit')
search.click()
driver.get('http://www.yopmail.com/')
search = driver.find_element_by_name('login')
search.send_keys("test_mlg_acc")
search.send_keys(Keys.RETURN)
search = driver.find_element_by_id('mailmillieu')
search = driver.find_elements(By.ID, 'mailmillieu')
search.send_keys()
driver.close()
driver.quit()
