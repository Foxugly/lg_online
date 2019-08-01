#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def fid(driver, user, password):
    driver.get('https://lieutenantguillaume.fid-manager.be/')
    driver.find_element_by_id('email').send_keys(user)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_id('submit').click()
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="pageMenu"]/ul/li[2]/span').click()
    driver.find_element_by_xpath('//*[@id="clientAddMenuItem"]/a').click()
    # nom complet
    driver.find_element_by_xpath('//*[@id="ngdialog1"]/div[2]/div/div[2]/div[1]/div/table/tbody/tr[1]/td[2]/input')\
        .send_keys("name")
    # numéro BCE
    driver.find_element_by_xpath('//*[@id="ngdialog1"]/div[2]/div/div[2]/div[1]/div/table/tbody/tr[2]/td[2]/input')\
        .send_keys("TVA")
    # NN
    driver.find_element_by_xpath('//*[@id="ngdialog1"]/div[2]/div/div[2]/div[1]/div/table/tbody/tr[4]/td[2]/input')\
        .send_keys("NN")
    # Langue
    dict_lang = {'fr': 'Fra', 'nl': 'Ned', 'en': 'Eng'}
    driver.find_element_by_xpath('//*[@id="ClientProposalLng"]').send_keys(dict_lang["fr"]).click()
    # Forme juridique
    driver.find_element_by_xpath('//*[@id="ClientProposalType"]').send_keys("Forme juridique")
    # Responsable
    driver.find_element_by_xpath('//*[@id="ClientProposalResponsible"]').send_keys("Responsable")
    # Associé
    driver.find_element_by_xpath('//*[@id="ClientProposalAssociate"]').send_keys("Associé")
    # Assistant
    driver.find_element_by_xpath('//*[@id="ClientProposalAssistant"]').send_keys("Assistant")
    # adresse
    #ligne 1
    driver.find_element_by_xpath('//*[@id="ngdialog4"]/div[2]/div/div[2]/div[1]/div/table/tbody/tr[10]/td/fieldset/div[1]/input[1]')\
        .send_keys("Ligne 1")
    # ville
    driver.find_element_by_xpath('//*[@id="ngdialog4"]/div[2]/div/div[2]/div[1]/div/table/tbody/tr[10]/td/fieldset/div[4]/input[1]')\
        .send_keys("ville")
    # cp
    driver.find_element_by_xpath('//*[@id="ngdialog4"]/div[2]/div/div[2]/div[1]/div/table/tbody/tr[10]/td/fieldset/div[4]/input[2]')\
        .send_keys("cp")
    # pays
    driver.find_element_by_xpath('//*[@id="ClientProposalAddressCountry"]').send_keys("BE").click()
    # checkboxes
    # déclarations TVA
    driver.find_element_by_xpath('//*[@id="ngdialog4"]/div[2]/div/div[2]/div[1]/div/table/tbody/tr[11]/td[2]/div/div').click()
    # Listing annuels
    driver.find_element_by_xpath('//*[@id="ngdialog4"]/div[2]/div/div[2]/div[1]/div/table/tbody/tr[12]/td[2]/div/div').click()
    # cloture des sociétés
    driver.find_element_by_xpath('//*[@id="ngdialog4"]/div[2]/div/div[2]/div[1]/div/table/tbody/tr[13]/td[2]/div/div').click()
    # IPP
    driver.find_element_by_xpath('//*[@id="ngdialog4"]/div[2]/div/div[2]/div[1]/div/table/tbody/tr[14]/td[2]/div/div').click()
    # PP
    driver.find_element_by_xpath('//*[@id="ngdialog4"]/div[2]/div/div[2]/div[1]/div/table/tbody/tr[15]/td[2]/div/div').click()
    # planning périodique
    driver.find_element_by_xpath('//*[@id="ngdialog4"]/div[2]/div/div[2]/div[1]/div/table/tbody/tr[16]/td[2]/div/div').click()
    # devoir d'information UBO
    driver.find_element_by_xpath('//*[@id="ngdialog4"]/div[2]/div/div[2]/div[1]/div/table/tbody/tr[17]/td[2]/div/div').click()
    # registre UBO
    driver.find_element_by_xpath('//*[@id="ngdialog4"]/div[2]/div/div[2]/div[1]/div/table/tbody/tr[18]/td[2]/div/div').click()
    # Etats financiers
    driver.find_element_by_xpath('//*[@id="ngdialog4"]/div[2]/div/div[2]/div[1]/div/table/tbody/tr[19]/td[2]/div/div').click()
    # driver.find_element_by_xpath('//*[@id="ngdialog4"]/div[2]/div/div[2]/div[1]/div/div/div/a[1]').click()
    time.sleep(10)


if __name__ == "__main__":
    driver = webdriver.Chrome()
    user = input("Fid user : ")
    password = input("password : ")
    fid(driver, user, password)
    driver.close()
    driver.quit()
