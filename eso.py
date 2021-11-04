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
sleep_delay = .1

def yesno(fc, ans):
    print("Checking yes/no '" + fc + "'")
    if not exists('//*[@field-config="' + fc + '"]//button[@class="btn radio-btn selected"]'):
        cl('//*[@field-config="' + fc + '"]//span[text()="' + ans + '"]')

def cl(xpath, tmo=default_timeout):
    global sleep_granularity
    global sleep_delay 

    sleep(sleep_delay)    
    print("Clicking on for " + xpath)
    for n in range(int(tmo/sleep_granularity)):
        try:
            e = driver.find_element_by_xpath(xpath)
            e.click()
            return
        except Exception as e:
            print("Click on " + xpath)
            print(e)
            sleep(sleep_granularity)


def sk(xpath, keys, tmo = default_timeout):
    global sleep_granularity
    global sleep_delay 

    sleep(sleep_delay)    
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

def waitfor(xpath, tmo=default_timeout):
    print("Waiting for " + xpath)
    for n in range(int(tmo/sleep_granularity)):
        try:
            e = driver.find_element_by_xpath(xpath)
            return True
        except Exception as e:
            print(e)
            sleep(sleep_granularity)
    return False

# single-select tweaked for EMS page, with horrible translate() hack for case insensitivity
def ssEms(id, text, tmo=default_timeout):
    print("Checking single-select '" + id + "' => '" + text + "'")
    already = True

    # check if single-select box is empty
    if exists('//*[@field-config="' + id + '"]//div[@class="display-value"]'):
        e = driver.find_element_by_xpath('//*[@field-config="' + id + '"]//div[@class="display-value"]')
        if e.text == "":
            print ("Empty display value on single-select")
            already = False

    # check if single-select box is quick-pick, with buttons showing (ie: nothing selected)
    if exists('//*[@field-config="' + id + '"]/div/div[@class=""]/div[@class="quick-picks"]/button'):
        print ("Visible pick buttons")
        cl('//*[@field-config="' + id + '"]//button', 2)     # click one button to select any value
        already = False

    if already:
        print ("Already filled, skipping")
    else:
        print ("single-select '" + id + "' found blank, setting value to '" + text + "'")
        cl('//*[@field-config="' + id + '"]', 2)      # click again to bring up the search pick menu 
        
        sk('//input[@ng-model="searchString"]', text, tmo)
        #sleep(1)
        if (exists("//eso-single-select-panel")): 
            cl('//eso-single-select-panel//li//div//mark[contains(' + 
                'translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),' +
                'translate("' + text + '", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"))]', tmo)
            cl('//eso-single-select-shelf//button[text()="OK"]', tmo=.5) 
        else: 
            cl('//eso-multi-select-panel//li//div//mark[contains(' + 
                'translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),' +
                'translate("' + text + '", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"))]', tmo)
            cl('//eso-multi-select-shelf//button[text()="OK"]', tmo=.5) 

        


def ss(id, text, tmo=default_timeout):
    xp = '//*[@field-ref="' + id + '"]'
    cl(xp, tmo)
    sk('//input[@ng-model="searchString"]', text, tmo)

