#!/usr/bin/python3
from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import re
import eso
from eso import *

user="EVANS"
date="10272021"

driver = eso.begin()

ps = str(driver.page_source)

try:
    driver.find_element_by_xpath('//shelf-panel//button[text()="OK"]').click()
except:
    0

cl('//label[text()="Basic"]')

# simple ones
ss("INCIDENTTYPEID", "3211\n");
ss("STATIONID", "54\n")
ss("ACTIONTAKEN1", "32\n")
ss("AIDGIVENORRECEIVEDID", "n\n")
ss("LOCATIONTYPEID", "address\n")
ss("PROPERTYUSEID", "000\n")
ss("OFFICERINCHARGEAGENCYPERSONID", user + "\n")
cl('//eso-yes-no[@field-ref="WORKINGFIRE"]//button[@data-val="false"]')
sk('//eso-text[@field-ref="ALARMS"]//input', "1\n")
sk('//eso-text[@field-ref="REPORTWRITERASSIGNMENT"]//input', "officer\n")

# complicated ones 
if exists('//eso-single-select[@field-ref="COVID19FACTORID"]//button[text()="No"]'):
    cl('//eso-single-select[@field-ref="COVID19FACTORID"]//button[text()="No"]')
else: 
    cl('//eso-single-select[@field-ref="COVID19FACTORID"]')
    sk('//input[@ng-model="searchString"]', "3\n")

cl('//eso-address-summary[@field-label="\'Address\'"]')
sk('//eso-zip-input//input', [Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE, 
    "98168\n"])
cl('//shelf-panel//button[text()="OK"]')


cl('//eso-date[@field-ref="OFFICERINCHARGEDATE"]')
sk('//eso-masked-input//input', [Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE, 
    date + "\n"])

cl('//eso-date[@field-ref="REPORTWRITERDATE"]')
sk('//eso-masked-input//input', [Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE, 
        date + "\n"])

sk('//eso-text[@field-ref="NARRATIVEREMARKS"]//textarea[@type="text"]', "See EMS report.\n")
sleep(1)
cl('//label[text()="Basic"]')

# Click on unit reports tab, wait for it to load 
cl('//label[text()="Unit Reports"]')
cl('//grid-cell[@class="unit-info-cell"]')
cl('//edit-unit-report-toast//button[text()="OK"]')

for unit in range(1, 5):
    ugrid = '(//grid-cell[@class="unit-info-cell"])[' + str(unit) + ']'
    if exists(ugrid):
        cl(ugrid)
        ss("UNITRESPONDINGFROMID", "in\n")
        ss("UNITPRIORITYID", "emer\n")
        ss("UNITACTIONTAKEN1", "32\n")
        cl('//edit-unit-report-toast//button[text()="OK"]')

cl('//label[text()="Validation Issues"]')

