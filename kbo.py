#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import time
from bs4 import BeautifulSoup
import os
import re
import datetime
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
    return value.lstrip().rstrip()

def bce(driver):
    #driver.get('https://kbopub.economie.fgov.be/kbopub/zoeknummerform.html?lang=fr')
    #search = driver.find_element_by_id('nummer')
    #search.send_keys("0454784696")
    nbce = "0454784696"
    #search = driver.find_element_by_id('actionLu')
    #search.click()
    #table_id = driver.find_element_by_id('table')
    #rows = table_id.find_elements_by_xpath('.//tr')
    #l = ["Statut:", "Situation juridique:", "Date de début:", "Dénomination:", "Adresse du siège:", "Forme légale:", "Date de fin de l'année comptable", "Gérant", "Administrateur"]
    out = {}
    url = 'https://kbopub.economie.fgov.be/kbopub/zoeknummerform.html?nummer=%s&actionLu=Recherche&lang=fr' % nbce
    soup = BeautifulSoup(requests.get(url).content, features="html.parser")
    for row in soup.findAll('tr'):
        #print(row)
        cols = row.findAll("td")
        if len(cols) >=2 :
            field = cols[0].text
            value = cols[1].text
            if "Statut" in field:
                out['statut'] = parse(value)
            elif "Situation" in field :
                value = value.split('Depuis')[0]
                out['situation_juridique'] = parse(value)
            elif "Date de début" in field:
                mois = {'janvier':'1', 'février':'2', 'mars':'3', 'avril':'4', 'mai':'5', 'juin':'6', 'juillet':'7', 'aout':'8', 'août':'8', 'septembre':'9', 
                        'octobre':'10', 'novembre':'11', 'décembre':'12', 'decembre':'12'}
                s = parse(value).split(' ')
                date = datetime.date(int(s[2]), int(mois[s[1]]),int(s[0]))
                out['date_debut'] = date
            elif "Dénomination" in field:
                value = value.split('Dén')[0]
                out['denomination'] = parse(value)
            elif "Adresse du siège" in field:
                adr = value.split('<br>')[0].split('\n')
                res = adr[1].split('\xa0')
                out['adresse'] = parse(res[0])
                if len(res) == 2:
                    out['adresse_num'] = parse(res[1])
                res = adr[2].split('\xa0')
                out['adresse_cp'] = parse(res[0])
                if len(res) == 2:
                    out['adresse_ville'] = parse(res[1])
            elif "Forme" in field:
                value = value.split('Depuis')[0]
                out['forme_legale'] = parse(value)
            elif "Gérant" in field or "Administrateur" in field :
                print(parse(field))
                print(parse(value))
            elif "Date de fin de l'année comptable" in field:
                out['date_fin_annee_comptable'] = parse(value)
    print(out)
dir = os.path.dirname(os.path.abspath(__file__))
#driver = webdriver.Chrome(os.path.join(dir,'chromedriver'))
# authentification(driver)
bce(None)
#time.sleep(10)
#driver.close()
#driver.quit()
