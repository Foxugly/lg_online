from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get('http://www.google.com')
search = driver.find_element_by_name('q')
search.send_keys("google search through python")
search.send_keys(Keys.RETURN)
time.sleep(10)
driver.quit()