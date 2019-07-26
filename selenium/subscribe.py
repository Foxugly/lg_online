#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import string


def random(size):
    s = string.lowercase + string.digits
    return''.join(random.sample(s, size))


def subscribe(driver, user, password):
    driver.get('http://www.mylieutenantguillaume.com')
    search = driver.find_element_by_name('subscribe')
    search.click()
    driver.find_element_by_name('email').send_keys(user)
    driver.find_element_by_name('first_name').send_keys("John")
    driver.find_element_by_name('last_name').send_keys("Smith")
    driver.find_element_by_name('password1').send_keys(password)
    driver.find_element_by_name('password2').send_keys(password)
    time.sleep(10)
    driver.find_element_by_name('submit').click()
    driver.get('http://www.yopmail.com/')
    driver.find_element_by_name('login').send_keys(user.split('@')[0]).send_keys(Keys.RETURN)
    driver.switch_to.frame("ifmail")
    driver.find_element_by_partial_link_text('lieutenantguillaume').click()
    driver.find_element_by_name('username').send_keys(user)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_name('submit').click()


if __name__ == "__main__":
    driver = webdriver.Chrome()
    user = "test_mlg_acc_%s@yopmail.com" % random(6)
    password = random(10)
    print("user : %s" % user)
    print("password : %s" % password)
    subscribe(driver, user, password)
    driver.close()
    driver.quit()
