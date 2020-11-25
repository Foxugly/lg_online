#!/usr/bin/env python3
import time

from selenium import webdriver


def yuki(driver, user, password):
    driver.get('https://www.yukiworks.be/docs/login.aspx?Central=1&Language=fr')
    driver.find_element_by_id('Email').send_keys(user)
    driver.find_element_by_id('Password').send_keys(password)
    driver.find_element_by_id('btnLogin').click()
    driver.get('https://yukicentral.yukiworks.nl/docs/Accountantdomains.aspx')
    driver.find_element_by_id('btnNew').click()
    driver.find_element_by_name('Administration').send_keys("adm")
    driver.find_element_by_name('Domain').send_keys("dom")
    dict_lang = {'fr': 'fr', 'nl': 'nl_be', 'en': 'en'}
    driver.find_element_by_name('DefaultLanguage').send_keys(dict_lang["fr"])
    driver.find_element_by_id('UserEmail').send_keys("usrmail")
    driver.find_element_by_id('UserFullName').send_keys("usrfullname")
    driver.find_element_by_name('CreateUserLogin').click()
    # driver.find_element_by_id('btnCreate').click()
    time.sleep(10)


if __name__ == "__main__":
    d = webdriver.Chrome()
    u = input("yuki user : ")
    p = input("password : ")
    yuki(d, u, p)
    d.close()
    d.quit()
