from sys import argv
from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
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

def begin():
    global driver
    if len(argv) < 3 :
        driver = webdriver.Firefox()
        driver.get("https://www.esosuite.net/")
        url = driver.command_executor._url  
        session_id = driver.session_id      
        print(argv[0] + " " + url + " " + session_id + "\n")
        if len(argv) == 2:
            while 1:
                sleep(1)
    else:
        executor_url = argv[1]
        session_id = argv[2]
        driver = create_driver_session(session_id, executor_url)

    wait = WebDriverWait(driver, 10)    
    return driver

sleep_granularity = .2
default_timeout = 10.0
def sk(xpath, keys, tmo = default_timeout):
    for n in range(int(tmo/sleep_granularity)):
        try:
            e = driver.find_element_by_xpath(xpath)
            e.clear()
            #print(keys)
            e.send_keys(keys)
            return
        except Exception as e:
            print(xpath)
            print(e)
            sleep(sleep_granularity)

def exists(xpath):
    return len(driver.find_elements_by_xpath(xpath)) > 0 

# single-select tweaked for EMS page, with horrible translate() hack for case insensitivity
def ssEms(id, text, tmo=default_timeout):

    if exists('//*[@field-config="' + id + '"]/div/div[@class="eso-hide"]/div[@class="quick-picks"]'):
        print("single-select '" + id + "' already picked")
        return

    print ("single-select '" + id + "' found blank, setting value to '" + text + "'")
    xp = '//*[@field-config="' + id + '"]'
    cl(xp, tmo)     # click once to select any value
    cl(xp, .2)      # click again to bring up the search pick menu 
    sk('//input[@ng-model="searchString"]', text, tmo)
    #sleep(1)
    cl('//eso-single-select-panel//li//div//mark[contains(' + 
        'translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),' +
        'translate("' + text + '", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"))]', tmo)
    #cl('//eso-single-select-panel//li//div//mark[text()="' + text + '"]')


def ss(id, text, tmo=default_timeout):
    xp = '//*[@field-ref="' + id + '"]'
    cl(xp, tmo)
    sk('//input[@ng-model="searchString"]', text, tmo)

def cl(xpath, tmo=default_timeout):
    for n in range(int(tmo/sleep_granularity)):
        try:
            e = driver.find_element_by_xpath(xpath)
            e.click()
            return
        except Exception as e:
            print(xpath)
            print(e)
            sleep(sleep_granularity)

def waitfor(xpath, tmo=default_timeout):
    for n in range(int(tmo/sleep_granularity)):
        try:
            e = driver.find_element_by_xpath(xpath)
            return
        except Exception as e:
            print(xpath)
            print(e)
            sleep(sleep_granularity)
