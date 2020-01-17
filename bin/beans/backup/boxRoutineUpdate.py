#!/usr/bin/python
# IoT Chip project version : 2.0
#import datetime
#import sys
#import time
#import subprocess
import os
import json
import requests
import urllib2
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

from beans import utils
from beans import Microchip as microchipRef
from beans import LedController as ledControllerRef
from beans import FanController as fanControllerRef
# from beans import IndicatorPanel as indicatorRef
from beans import DimmerController as dimmerRef
# from beans import AirPumpController as airpumpRef

###
### IMPORTANT !
### DO NOT ALTER VARIABLES NAMES NOR PARAMETERS
### CHANGING THE VALUES MAY CAUSE THE SCRIPT TO NOT WORK CORRECTLY
###

### Constants

baseUrl = "http://demo.planthive.com"
#baseUrl = "http://192.168.0.101/boxbeta"

### Control Variables

x_microchip = True
x_read_server_json = True
x_read_server_file = False
x_read_server_insta = True

### Sensors and Controllers 

if x_microchip :
    print("- - - - - - - - - - - - - - - - - - - - ")
    try:
        microchip = microchipRef.Microchip()
        serialNumber = microchip.getSerialNumber()
        print("Microchip Serial Number : " + serialNumber)
    except Exception,e: 
        utils.log("Microchip: ")
        utils.log(str(e))
    except:
        utils.log("Microchip: Unknown Error")

###-------------------------------------
### Read Configurations from Server
###-------------------------------------

### JSON request method

if x_read_server_json:
    print("- - - - - - - - - - - - - - - - - - - - ")
    print("Reading Configuration Data from Server JSON Request...")
    isDataValid = False
    data = {}
    url = baseUrl+"/plantum/download/configuration?serialnumber="+serialNumber
    try :
        response = urllib2.urlopen(url)
        data = json.loads(response.read())
        print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        # check if data is a data dict and a valid json
        if not(isinstance(data, (int, long))) and "configuration_name" in data:
            isDataValid = True
            confPath = utils.getContextPath()+'/conf'
            with open(confPath+'/activecfg.json', "w") as confJSONfile:
                json.dump(data, confJSONfile, indent=4, separators=(',', ': '))
        else:
            print("Configuration not found on server")
    except Exception,e: 
        utils.log("Server JSON Request: "+str(e))
    except:
        utils.log("Server JSON Request: Unknown Error")

### JSON file method
## Note : this method is scheduled to be deprecated in the next update

if x_read_server_file :
    found = False
    isDataValid = False
    data = {}
    print("- - - - - - - - - - - - - - - - - - - - ")
    try :
        print("Reading Configuration Data from Server File...")
        url = baseUrl+"/dataio/devices/"+serialNumber+"/configurations/fwdi_0.json"
        response = urllib2.urlopen(url)
        data = json.loads(response.read())
        print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        confPath = utils.getContextPath()+'/conf'
        with open(confPath+'/activecfg.json', "w") as confJSONfile:
            json.dump(data, confJSONfile, indent=4, separators=(',', ': ')) 
        found = True
        isDataValid = True
    except Exception,e: 
        utils.log("Server Read Try 1 :")
        utils.log(str(e))
    except:
        utils.log("Server Read Try 1: Unknown Error")

    if not found :
        try :
            print("Reading Configuration Data from Server...")
            url = baseUrl+"/dataio/devices/"+serialNumber+"/configurations/fwdi_1.json"
            response = urllib2.urlopen(url)
            data = json.loads(response.read())
            print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
            confPath = utils.getContextPath()+'/conf'
            with open(confPath+'/activecfg.json', "w") as confJSONfile:
                json.dump(data, confJSONfile, indent=4, separators=(',', ': '))
            found = True
            isDataValid = True
        except Exception,e: 
            utils.log("Server Read Try 2 :")
            utils.log(str(e))
        except:
            utils.log("Server Read Try 2: Unknown Error")

    if not found :
        try :
            print("Reading Configuration Data from Server...")
            url = baseUrl+"/dataio/devices/"+serialNumber+"/configurations/fwdi_2.json"
            response = urllib2.urlopen(url)
            data = json.loads(response.read())
            print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
            confPath = utils.getContextPath()+'/conf'
            with open(confPath+'/activecfg.json', "w") as confJSONfile:
                json.dump(data, confJSONfile, indent=4, separators=(',', ': '))
            found = True
            isDataValid = True
        except Exception,e: 
            utils.log("Server Read Try 3 :")
            utils.log(str(e))
        except:
            utils.log("Server Read Try 3: Unknown Error")

###----------------------------
### Read Insta Commands
###----------------------------

if x_read_server_insta :

    #resp = requests.post('http://www.mywebsite.com/user')
    #resp = requests.put('http://www.mywebsite.com/user/put')
    #resp = requests.delete('http://www.mywebsite.com/user/delete')

    print("Reading Insta Commands from Server...")
    instaReqParams = {"serialnumber" : serialNumber}
    instaCommandsResponse = requests.get(baseUrl+'/plantum/insta/execommand', params=instaReqParams)
    #print(str(instaCommandsResponse.status_code))
    instaCommandsJSON = instaCommandsResponse.json()

    ## Alternative
    #instaReq = urllib2.Request(baseUrl+'/plantum/insta/execommand')
    #instaReqParams = {'serialnumber' : serialNumber }
    #instaReqParamsEnc = urllib2.urlencode(instaReqParams)
    #instaCommandsResponse = urllib2.urlopen(instaReq,instaReqParamsEnc).read()
    
    confPath = utils.getContextPath()+'/conf'
    with open(confPath+'/instacommands.json', "w") as instaJSONfile:
        json.dump(instaCommandsJSON, instaJSONfile, indent=4, separators=(',', ': '))
    print json.dumps(instaCommandsJSON, sort_keys=True, indent=4, separators=(',', ': '))

###--------------------------
### Process Configuration 
###--------------------------

if x_read_server_file or x_read_server_json :
    if isDataValid :
        print("Processing Configuration...")
        try:
            ## Leds
            print("- - - - - - - - - - - - - - - - - - - - ")
            ledControllerObj = ledControllerRef.LedController()
            ledControllerObj.execute(data)
            #ledControllerObj.set(0,200)
            #ledControllerObj.set(1,200)

            ## Fans
            # fanObj = fanControllerRef.FanController()
            # fanObj.setOff(0)

            ## AirPump 
            # no control

            ## Indicator
            # indicatorObj = indicatorRef.IndicatorPanel() 

            ## Dimmer
            print("- - - - - - - - - - - - - - - - - - - - ")
#            dimmer = dimmerRef.DimmerController()
#            dimmer.runPwm()

        except Exception,e: 
            utils.log("Processing Configuration :")
            utils.log(str(e))
        except:
            utils.log("Processing Configuration : Unknown Error")


###--------------------------
### Process Insta Commands 
###--------------------------

if x_read_server_insta :
    print("- - - - - - - - - - - - - - - - - - - - ")
    if instaCommandsJSON and not(isinstance(instaCommandsJSON, (int, long))) :
        for cmd in instaCommandsJSON:
            if cmd == "insta_collect_data" :
                os.system("sudo python "+utils.getContextPath()+"/bin/boxRoutineCollect.py")
            if cmd == "insta_collect_photo" :
                os.system("sudo python "+utils.getContextPath()+"/bin/boxRoutineCollectPhoto.py")
            if cmd == "insta_shutdown_system" :
                os.system("sudo shutdown now")
            if cmd == "insta_reboot_system" :
                os.system("sudo reboot")
    else :
        print "Insta Commands: Nothing to do"