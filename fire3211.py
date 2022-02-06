#!/usr/bin/python3
from time import sleep
import re
from tkinter.ttk import Combobox
import eso
from eso import *
from datetime import date
from tkinter import *
from tkinter import simpledialog

class MyDialog(simpledialog.Dialog):
    def __init__(self, master):
        self.okPressed = False
        simpledialog.Dialog.__init__(self, master,title="ESO Crusher")

    # returns (stringvar, entry) for the Entry 
    def addCheckbox(self, master, label, default):
        v = IntVar(root, value=default)
        Label(master, text=label).grid(sticky="w", column = 0, row = self.row)
        Checkbutton(master,variable=v, onvalue=1, offvalue=0).grid(sticky="w", column=1,row=self.row)
        self.row += 1
        return v


    def addTextEntry(self, master, prompt, default):
        sv = StringVar(root, value=default)
        Label(master, text=prompt).grid(sticky="w", column = 0, row = self.row)
        e = Entry(master,  textvar=sv)
        e.grid(sticky="w", column = 1, row = self.row)
        self.row += 1
        return (e, sv)


    def setCrib(self): 
        s = self.cb['values'][self.cb.current()].split('/')
        
        self.crib1.delete(0, END)
        self.crib1.insert(0, s[0])
        self.crib1.setvar()

        self.crib2.delete(0, END)
        self.crib2.insert(0, s[1])
        self.crib1.setvar()

        self.crib3.delete(0, END)
        self.crib3.insert(0, s[2])
        self.crib1.setvar()

    def body(self, master):
        #self.labels = Frame(master).pack()
        #self.entries = Frame(master).pack()
        self.row = 0;

        (dummy, self.name) = self.addTextEntry(master, "FF Name", "evans")
        (dummy, self.station) = self.addTextEntry(master, "Station", "54")
        (dummy, self.zip) = self.addTextEntry(master, "Zip", "98168")
        (self.crib1, self.pi) = self.addTextEntry(master, "Primary Impression", "alter")
        (self.crib2, self.ssc) = self.addTextEntry(master, "S&S Category", "cognit")
        (self.crib3, self.ssd) = self.addTextEntry(master, "S&S Detail", "intox")
        (dummy, self.hospital) = self.addTextEntry(master, "Hospital", "vall")
        self.male = self.addCheckbox(master, 'Male', 1)
        self.firstUnit = self.addCheckbox(master, 'First Unit', 1)
        
        
        Label(master).grid(column = 0, row=self.row)    
        self.row += 1

        cb = Combobox(master)
        cb['values'] = ('alt/cog/intox', 'face/inj/face', 'no complaint/no/no', 'shortness/resp/short')
        cb.current(0)
        cb.grid(column=0, row   =self.row) 
        self.cb = cb
        Button(master, text="SET", command=self.setCrib).grid(column = 1, row=self.row)
        self.setCrib()
        self.row += 1




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
        d.zip.get() + "\n"])
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



def waitforClick(x):
   waitfor(x)
   cl(x)


def emsReport():
    global d
    global date
    global driver


 
    # Click out of any shelf trays that happen to be up 
    cl('//shelf-panel//button[text()="OK"]', tmo=.5) 
    cl('//shelf-panel//button[text()="OK"]', tmo=.5) 

    ###################################################33
    # INCIDENT tab
    cl('//li[@class="incident incident-bg"]')
     

    waitforClick('//button[text()="CAD Import"]')
    waitforClick('//button[text()="Update data"]')
    waitforClick('//button[text()="Refresh with new data"]')

    ssEms("incident.response.runTypeId", "911")
    ssEms("incident.response.priorityId", "Emer")
    ssEms("incident.response.stationId", d.station.get())
    ssEms("incident.response.respondingFromZoneID", "In")
    ssEms("incident.response.requestedByItemID", "Patient")

    if (len(d.hospital.get()) > 0): 
        ssEms("incident.response.dispositionItemID", "Pt Care T")
        ssEms("incident.disposition.dispositionItemID", "Patient Treated, Trans")
        ssEms("incident.disposition.transportMethodID", "Ambulance")
        ssEms("incident.disposition.transportDueToItemIDs", "Patient")
        ssEms("incident.disposition.transferredToLocationTypeID", "Ground")
        ssEms("incident.disposition.transferredToLocationID", "Tri")
        ssEms("incident.destination.predefinedAddress.predefinedLocationID", d.hospital.get())
    else:
        ssEms("incident.response.dispositionItemID", "No Treatment")

    ssEms("incident.scene.manualAddress.locationTypeID", "Home")

    yesno("incident.response.isFirstUnitOnSceneID", "Yes" if d.firstUnit.get() else "No")
    yesno("incident.scene.massCasualty", "No")

	# Pick 98168 zip code 
    if (exists('//button[@class="btn icon-btn search-bg"]')):
        cl('//button[@class="btn icon-btn search-bg"]')
        cl('//td[text()="' + d.zip.get() + '"]')
    

#<button class="btn icon-btn search-bg" ng-class="{ searching: searching, 'search-bg': !isInternational, 'search-gray-bg': isInternational }" ng-click="search($event)" ng-disabled="isInternational"></button>

#/html/body/emr-app/div/emr-app-body/main/incident-tab/emr-main-view/main-viewport/field-set[2]/eso-location/div[2]/eso-address/table[2]/tbody/tr[2]/td[2]/table/tbody/tr/td[2]/button

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
        
    # Handle missing "at-patient" time 
    if (exists('//span[text()="At Patient"]/../span[text()="- -"]')):
        e = driver.find_element_by_xpath('(//span[text()="On Scene"]/../span)[2]')
        # Add 3 minutes to "On Scene" time 
        try: 
            t = e.text.split(':')
            t[1] = str(int(t[1]) + 3)
            if int(t[1]) >= 60:
                t[0] = str(int(t[0]) + 1)
            newTime = "".join(t)
            print ("No at patient time, setting to " + newTime)
            cl('//button[text()="Set Times"]')
            sk('//time-entry[@label="At Patient"]//eso-masked-input//input', [Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE, 
                newTime])
            cl('//shelf-panel//button[text()="OK"]') 
        except Exception as e:
            print(e)

    ###################################################33
    # PATIENT tab
    cl('//li[@class="patient patient-bg"]')
    sleep(1)
    #ssEms("patient.demographics.ethnicityId", "Not")
    ssEms("patient.demographics.genderId", ("Male" if d.male.get() else "Female"))

    ###################################################33
    # NARRATIVE tab
    cl('//li[@class="narrative narrative-bg"]')
    sleep(1)
    ssEms("narrative.clinicalImpression.medicalTraumaId", "Trauma")
    ssEms("narrative.clinicalImpression.primaryImpressionId", d.pi.get())

    # Add a sign/sympt if one doens't yet texist 
    ssBut = "((//narrative-signs-symptoms//grid-row)[1]/grid-cell)[1]/button"
    if exists(ssBut):
        cl(ssBut)
        ssEms("narrative.supportingSignsAndSymptoms.signsAndSymptoms.supportPrimaryId", d.ssc.get())
        ssEms("narrative.supportingSignsAndSymptoms.signsAndSymptoms.supportSignId", d.ssd.get())
        cl('//shelf-panel//button[text()="OK"]', tmo=.5) 

    
    ###################################################33
    # SIGNATURES TAB tab
    # Make signature array with output from http://ramkulkarni.com/blog/record-and-playback-drawing-in-html5-canvas-part-ii/ 
    # and this: 
    # tr '}' '\n'  | perl -e 'while(<>){if(/"x":(\d+),"y":(\d+)/ && $count++ % 5 == 0) { $x=$1-$lx;$y=$2-$ly; $lx=$1;$ly=$2; print "[$x,$y],"; }}'
    # 

    cl('//li[@class="signatures signatures-bg"]')
    sleep(1)
    cl('//div[text()="Provider Signatures"]')
    if exists('//div[@class="signing-area signature signed-bg"]'):
        print("ALREADY SIGNED")
    else:
        print("NOT SIGNED")
        ssEms("signatures.standardSignatures.providerSignatures.leadProviderId", d.name.get())
        cl('//eso-signature-pad//canvas')

        canvas = driver.find_element_by_xpath('//div[@class="signing-area-container"]')
        #//eso-signature-pad//canvas')
        drawing = ActionChains(driver)\
            .move_to_element_with_offset(canvas, 120, -482) \
            .click_and_hold()
        for p in (
            [-20,-32],[-8,-51],[4,-53],[19,-8],[16,118],[-20,58],[-31,32],[-8,-2],[77,-95],[19,-16],[5,-3],[-6,16],        
            ):
            drawing = drawing.move_by_offset(p[0], p[1])
        drawing.release()

        drawing.perform()
        cl('//eso-signature-dialog//button[text()="OK"]') 
    cl('//shelf-panel//button[text()="OK"]') 

    ###################################################33
    # VALIDATE button Experiental stuff messing with Validate button
    if 0:  
        cl('//button[@class="validate check-circle-white-bg"]')
        waitfor('//shelf-panel//button[text()="OK"]') 
        sleep(5)
        if exists('//strong[text()="At Patient"]'):
            print ("AT PATIENT")


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

