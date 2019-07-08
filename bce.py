#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import re

#driver.execute_script("arguments[0].click();", search)


def authentification(driver):
    driver.get('https://www.yukiworks.be/docs/Login.aspx?Central=1&Language=fr')
    mail = "md@lieutenantguillaume.com"
    search = driver.find_element_by_id('Email')
    search.send_keys(mail)
    search = driver.find_element_by_id('Password')
    search.send_keys("1234")
    search = driver.find_element_by_id('btnLogin')
    search.click()

def parse(value):
    value = value.replace('\t',' ')
    value = value.replace('\n','')
    value = re.sub(' +', ' ', value)
    value = re.compile(r'<[^>]+>').sub('', value)
    return value.lstrip()

def bce(driver):
    driver.get('https://kbopub.economie.fgov.be/kbopub/zoeknummerform.html?lang=fr')
    search = driver.find_element_by_id('nummer')
    search.send_keys("0454784696")
    search = driver.find_element_by_id('actionLu')
    search.click()
    table_id = driver.find_element_by_id('table')
    rows = table_id.find_elements_by_xpath('.//tr')
    l = ["Statut:", "Situation juridique:", "Date de début:", "Dénomination:", "Adresse du siège:", "Forme légale:", "Date de fin de l'année comptable", "Gérant", "Administrateur"]
    for row in rows:
        cols = row.find_elements_by_xpath("td")
        if len(cols) >=2 :
            field = cols[0].get_attribute('innerHTML')
            value = cols[1].get_attribute('innerHTML')
            if "Statut" in field:
                print("Statut")
                print(parse(value))
            elif "Situation" in field :
                print("Situation juridique")
                value = value.split('<br>')[0]
                print(parse(value))
            elif "Date de début" in field:
                print("Date de début")
                print(parse(value))
            elif "Dénomination" in field:
                print("Dénomination")
                value = value.split('<br>')[0]
                print(parse(value))
            elif "Adresse du siège" in field:
                print("Adresse du siège")
                res = value.split('<br>')[0]
                print(parse(res))
                res = value.split('<br>')[1]
                print(parse(res))
            elif "Forme" in field:
                print("Forme légale")
                value = value.split('<br>')[0]
                print(parse(value))
            elif "Gérant" in field or "Administrateur" in field :
                print(parse(field))
                print(parse(value))
            elif "Date de fin de l'année comptable" in field:
                print("Date de fin de l'année comptable")
                print(parse(value))

dir = os.path.dirname(os.path.abspath(__file__))
driver = webdriver.Chrome(os.path.join(dir,'chromedriver'))
# authentification(driver)
bce(driver)
time.sleep(10)
driver.close()
driver.quit()
