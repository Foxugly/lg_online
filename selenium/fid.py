#!/usr/bin/env python3
from selenium import webdriver
import time


def fid(driver, user, password):
    driver.get('')
    driver.find_element_by_id('').send_keys(user)
    driver.find_element_by_id('').send_keys(password)
    driver.find_element_by_id('').click()
    time.sleep(10)


if __name__ == "__main__":
    driver = webdriver.Chrome()
    user = input("Fid user : ")
    password = input("password : ")
    fid(driver, user, password)
    driver.close()
    driver.quit()
