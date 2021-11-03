#!/usr/bin/python3
from time import sleep
import re
import eso
from eso import *
from datetime import date
from tkinter import *
from tkinter import simpledialog

class MyDialog(simpledialog.Dialog):
    def __init__(self, master):
        self.okPressed = False
        simpledialog.Dialog.__init__(self, master,title="ESO Crusher")

    def body(self, master):
        Label(master, text="Name   :").grid(row=0)
        Label(master, text="Station:").grid(row=1)

        self.name = StringVar(root, value='EVANS')
        self.station = StringVar(root, value='54')
        self.e1 = Entry(master,textvariable=self.name)
        self.e2 = Entry(master,textvariable=self.station)
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1 # initial focus

    def apply(self):
        self.okPressed = True

date=date.today().strftime("%m%d%Y")
driver = eso.begin()

def fireReport():
    global d
    global date
    global driver 
    cl('//shelf-panel//button[text()="OK"]', tmo=1) 
    cl('//label[text()="Basic"]')

    # simple ones
    ss("INCIDENTTYPEID", "3211\n");
    ss("STATIONID", d.station.get() + "\n")
    ss("ACTIONTAKEN1", "32\n")
    ss("AIDGIVENORRECEIVEDID", "n\n")
    ss("LOCATIONTYPEID", "address\n")
    ss("PROPERTYUSEID", "000\n")
    ss("OFFICERINCHARGEAGENCYPERSONID", d.name.get() + "\n")
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
    cl('//grid-cell[@class="unit-info-cell"]',tmo=20.0)
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



def emsReport():
    global d
    global date
    global driver

    cl('//shelf-panel//button[text()="OK"]', tmo=.5) 
    cl('//shelf-panel//button[text()="OK"]', tmo=.5) 
    cl('//li[@class="incident incident-bg"]')
    sleep(1)
    
    # TODO: figure ou how to tell if eso-single-select is already filled in 
    ssEms("incident.response.runTypeId", "911")
    ssEms("incident.response.priorityId", "Emer")
    ssEms("incident.response.stationId", d.station.get())
    ssEms("incident.response.respondingFromZoneID", "In")
    ssEms("incident.response.requestedByItemID", "Patient")

    # Still working on xpath syntax 
    #cl('//eso-radio-list[@field-config="incident.response.isFirstUnitOnSceneID"]//*[text()="Yes"]')

    # Set PPE for people 
    for unit in range(1, 5):
        x = '(//incident-crew//grid-row//div[@class="name"])[' + str(unit) + ']'
        if (exists(x)):
            cl(x)
            cl('//eso-multi-select[@field-config="incident.crew.personalProtectiveEquipment"]')
            waitfor('//li//div[text()="Eye Protection"]')
            for ppe in ["Eye Protection", "Gloves", "Mask-N95"]: 
                x = '//li//div[text()="' + ppe + '"]/../..//check-mark[@class="check-white-bg"]';
                if (exists(x)):
                    cl(x)
            cl('//shelf-panel//button[text()="OK"]') 
            cl('//shelf-panel//button[text()="OK"]') 
        
    
    if 0:  # Experiental stuff messing with Validate button 
        cl('//button[@class="validate check-circle-white-bg"]')
        waitfor('//shelf-panel//button[text()="OK"]') 
        sleep(5)
        if exists('//strong[text()="At Patient"]'):
            print ("AT PATIENT")

    # Handle missing "at-patient" time 
    if (exists('//span[text()="At Patient"]/../span[text()="- -"]')):
        e = driver.find_element_by_xpath('(//span[text()="On Scene"]/../span)[2]')
        # Add 3 minutes to "On Scene" time 
        t = e.text.split(':')
        t[1] = str(int(t[1]) + 3)
        if int(t[1]) >= 60:
            t[0] = str(int(t[0]) + 1)
        newTime = "".join(t)
        cl('//button[text()="Set Times"]')
        sk('//time-entry[@label="At Patient"]//eso-masked-input//input', newTime + "\n")


    cl('//li[@class="patient patient-bg"]')
    sleep(1)
    ssEms("patient.demographics.ethnicityId", "Not")

    cl('//li[@class="narrative narrative-bg"]')
    sleep(1)
    ssEms("narrative.clinicalImpression.medicalTraumaId", "Trauma")



    # Handle signatures tab 
    cl('//li[@class="signatures signatures-bg"]')
    sleep(1)
    cl('//div[text()="Provider Signatures"]')
    if exists('//div[@class="signing-area signature signed-bg"]'):
        print("ALREADY SIGNED")
    else:
        print("NOT SIGNED")
        ssEms("signatures.standardSignatures.providerSignatures.leadProviderId", "EV")
        cl('//eso-signature-pad//canvas')

        canvas = driver.find_element_by_xpath('//div[@class="signing-area-container"]')
        #//eso-signature-pad//canvas')
        drawing = ActionChains(driver)\
            .move_to_element_with_offset(canvas, 120, -382) \
            .click_and_hold() \
            .move_by_offset(100, -100) \
            .move_by_offset(100, +100) \
            .release()

        drawing.perform()
        cl('//eso-signature-dialog//button[text()="OK"]') 
    cl('//shelf-panel//button[text()="OK"]') 
    


while True:
    root = Tk()
    root.withdraw()
    d = MyDialog(root)
    if not d.okPressed: 
        exit()

    #ps = str(driver.page_source)

    if exists("//current-patient"):
        emsReport()
    elif exists("//exposure-summary"):
        fireReport()

    exit()

