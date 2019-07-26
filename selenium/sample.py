#!/usr/bin/env python3

from selenium import webdriver
from .subscribe import subscribe, random


if __name__ == "__main__":
    driver = webdriver.Chrome()
    user = "test_mlg_acc_%s@yopmail.com" % random(6)
    password = random(10)
    print("user : %s" % user)
    print("password : %s" % password)
    subscribe(driver, user, password)
    driver.close()
    driver.quit()
