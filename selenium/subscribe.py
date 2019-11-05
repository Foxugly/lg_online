#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import string


def rand(size):
    return''.join(random.sample(string.ascii_lowercase + string.digits, size))


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
    d = webdriver.Chrome()
    u = "test_mlg_acc_%s@yopmail.com" % rand(6)
    p = rand(10)
    print("user : %s" % u)
    print("password : %s" % p)
    subscribe(d, u, p)
    d.close()
    d.quit()
