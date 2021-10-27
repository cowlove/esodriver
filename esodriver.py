#!/usr/bin/python3
from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from sys import argv
import re



def create_driver_session(session_id, executor_url):
    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
    # Save the original function, so we can revert our patch
    org_command_execute = RemoteWebDriver.execute
    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)

    # Patch the function before creating the driver object
    RemoteWebDriver.execute = new_command_execute
    new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id

    # Replace the patched function with original function
    RemoteWebDriver.execute = org_command_execute
    return new_driver

if len(argv) < 3 :
    driver = webdriver.Firefox()
    driver.get("https://www.esosuite.net/")
    url = driver.command_executor._url  
    session_id = driver.session_id      
    print(url + " " + session_id + "\n")
    if len(argv) == 2:
        while 1:
            sleep(1)
else:
    executor_url = argv[1]
    session_id = argv[2]
    driver = create_driver_session(session_id, executor_url)

wait = WebDriverWait(driver, 10)    


def sk(xpath, keys):
    for n in range(50):
        try:
            e = driver.find_element_by_xpath(xpath)
            e.clear()
            #e.send_keys(Keys.HOME)
            print(keys)
            e.send_keys(keys)
            return
        except Exception as e:
            print(xpath)
            print(e)
            sleep(.2)


def exists(xpath):
    return len(driver.find_elements_by_xpath(xpath)) > 0 


def cl(xpath):
    for n in range(50):
        try:
            e = driver.find_element_by_xpath(xpath)
            e.click()
            return
        except Exception as e:
            print(xpath)
            print(e)
            sleep(.2)

while 1:
    ps = str(driver.page_source)


    try:    
        driver.find_element_by_name("username").click()
        driver.find_element_by_name("username").send_keys("jevans")
        #driver.find_element_by_name("password").sendkeys("jevans2")
        #driver.find_element_by_name("agency").sendkeys("tukwilafd")
    except Exception as e:
        0 #        print(e)

    try:
        driver.find_element_by_xpath('//shelf-panel//button[text()="OK"]').click()
    except:
        0

    if 0:
        for unit in range(1, 3):
            cl('(//grid-cell[@class="unit-info-cell"])[' + str(unit) + ']')

            cl('//eso-single-select[@field-ref="UNITRESPONDINGFROMID"]')
            sk('//input[@ng-model="searchString"]', "in\n")
            cl('//edit-unit-report-toast//button[text()="OK"]')

        break

    if 1:
        cl('//label[text()="Basic"]')

        cl('//eso-single-select[@field-ref="INCIDENTTYPEID"]')
        sk('//input[@ng-model="searchString"]', "3211\n")

        cl('//eso-yes-no[@field-ref="WORKINGFIRE"]//button[@data-val="false"]')

        if exists('//eso-single-select[@field-ref="COVID19FACTORID"]//button[text()="No"]'):
            cl('//eso-single-select[@field-ref="COVID19FACTORID"]//button[text()="No"]')
        else: 
            cl('//eso-single-select[@field-ref="COVID19FACTORID"]')
            sk('//input[@ng-model="searchString"]', "3\n")
    
        sk('//eso-text[@field-ref="ALARMS"]//input', "1\n")
    
        cl('//eso-single-select[@field-ref="STATIONID"]')
        sk('//input[@ng-model="searchString"]', "54\n")

        cl('//eso-single-select[@field-ref="ACTIONTAKEN1"]')
        sk('//input[@ng-model="searchString"]', "32\n")

        cl('//eso-single-select[@field-ref="AIDGIVENORRECEIVEDID"]')
        sk('//input[@ng-model="searchString"]', "n\n")

        cl('//eso-single-select[@field-ref="LOCATIONTYPEID"]')
        sk('//input[@ng-model="searchString"]', "address\n")

        cl('//eso-address-summary[@field-label="\'Address\'"]')
        sk('//eso-zip-input//input', [Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE, 
            "98168\n"])
        cl('//shelf-panel//button[text()="OK"]')

        cl('//eso-single-select[@field-ref="PROPERTYUSEID"]')
        sk('//input[@ng-model="searchString"]', "000\n")

        sk('//eso-text[@field-ref="REPORTWRITERASSIGNMENT"]//input', "officer\n")
        
        cl('//eso-single-select[@field-ref="OFFICERINCHARGEAGENCYPERSONID"]')
        sk('//input[@ng-model="searchString"]', "EVANS\n")

        cl('//eso-date[@field-ref="OFFICERINCHARGEDATE"]')
        sk('//eso-masked-input//input', [Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE, 
            "10272021\n"])
    
        cl('//eso-date[@field-ref="REPORTWRITERDATE"]')
        sk('//eso-masked-input//input', [Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE, 
                "10272021\n"])
    
        sk('//eso-text[@field-ref="NARRATIVEREMARKS"]//textarea[@type="text"]', "See EMS report.\n")
        sleep(1)
        cl('//label[text()="Basic"]')

        cl('//label[text()="Unit Reports"]')
        cl('//grid-cell[@class="unit-info-cell"]')
        cl('//edit-unit-report-toast//button[text()="OK"]')

        for unit in range(1, 3):
            ugrid = '(//grid-cell[@class="unit-info-cell"])[' + str(unit) + ']'
            if exists(ugrid):
                cl(ugrid)
                
                cl('//eso-single-select[@field-ref="UNITRESPONDINGFROMID"]')
                sk('//input[@ng-model="searchString"]', "in\n")
            
                cl('//eso-single-select[@field-ref="UNITPRIORITYID"]')
                sk('//input[@ng-model="searchString"]', "emer\n")
            
                cl('//eso-single-select[@field-ref="UNITACTIONTAKEN1"]')
                sk('//input[@ng-model="searchString"]', "32\n")

                cl('//edit-unit-report-toast//button[text()="OK"]')

        cl('//label[text()="Validation Issues"]')



        break
        #e = driver.find_element_by_xpath('//eso-single-select[@field-ref="INCIDENTTYPEID"]')
        #e.click()   
        #e = driver.find_element_by_xpath('//input[@ng-model="searchString"]')
        #e.send_keys("3211\n")
    #except Exception as e:
        print(e)

    
    sleep(1)

