#!/usr/bin/python

#import datetime
import sys
import time
#import subprocess
import os
import json

from beans import utils
from beans import Microchip as microchipRef
from beans import Hygrometer as hygrometerRef
from beans import AquaThermometer as aquaThermometerRef
from beans import Thermometer as thermometerRef
from beans import ThermoHygrometer as thermoHygrometerRef
from beans import Moisturemeter as moisturemeterRef
from beans import GpioController as gpioRef
from beans import LedController as ledControllerRef
from beans import FanController as fanControllerRef
from beans import IndicatorPanel as indicatorRef
from beans import AirPumpController as airpumpRef
from beans import ExecutePWM as executepwmRef
# from beans import Camera as cameraRef

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
x_execute = True

### Sensors and Controllers 

if x_microchip :
    try:
        microchip = microchipRef.Microchip()
        serialNumber = microchip.getSerialNumber()
        print("Microchip Serial Number : " + serialNumber)
    except Exception,e: 
        utils.log("Microchip: ")
        utils.log(str(e))
    except:
        utils.log("Microchip: Unknown Error")

### Read from local configuration file

try :
    dataConfiguration = {}
    print("Reading Configuration from File...")
    confPath = utils.getContextPath()+"/conf/fetched_data.json"
    with open(confPath) as data_file:    
        dataConfiguration = json.load(data_file)
    print json.dumps(dataConfiguration, indent=4, sort_keys=True)
except Exception,e: 
    utils.log("File Read Failed :")
    utils.log(str(e))
except:
    utils.log("File Read Failed: Unknown Error")

print("Collecting sensors data...")
try:
    ####----------------------------------------------------
    # Step : Collect data from sensors and save to json file
    ####----------------------------------------------------

    # Power on GPIO
    print("- - - - - - - - - - - - - - - - - - - - ")
    gpio = gpioRef.GpioController(False)
    gpio.powerOn()

    #thermometer = thermometerRef.Thermometer()
    #temperature = thermometer.get()
    #print(temperature)

    #hygrometer = hygrometerRef.Hygrometer()
    #humidity = hygrometer.get()
    #print(humidity)

    print("- - - - - - - - - - - - - - - - - - - - ")
    thmeter = thermoHygrometerRef.ThermoHygrometer()
    #temperature, humidity = thmeter.get()
    temperature = 22
	    humidity    = 69
	    print("Air T: "+str(temperature))
    print("Air H: "+str(humidity))

    print("- - - - - - - - - - - - - - - - - - - - ")
    waterTemperature = 0
    #aquaThermometer = aquaThermometerRef.AquaThermometer()
    #print("Getting Water Temperature...")
    #waterTemperature = aquaThermometer.get()
    print("Water Temp: "+str(waterTemperature))

    print("- - - - - - - - - - - - - - - - - - - - ")
    moisturemeter = moisturemeterRef.Moisturemeter()
    #moistureLevel1 = moisturemeter.get(1)
    #moistureLevel2 = moisturemeter.get(2)
    #moistureLevel3 = moisturemeter.get(3)
    #moistureLevel4 = moisturemeter.get(4)
    
    moistureLevel1 = 0
    moistureLevel2 = 0
    moistureLevel3 = 0
    moistureLevel4 = 0

    # Other (defaults for non-implemented)
    ph = 7
    waterlevel = 50

    # get timestamp
    timestamp = int(time.time())*1000.0

    # power off gpio
    gpio.powerOff()
    
    # Gather collected data in a dictionnary
    dataCollect = {
        'serialnumber': serialNumber,
        'datetime': timestamp,
        'temperature': temperature,
        'humidity': humidity,
        'moisture_level_1': moistureLevel1,
        'moisture_level_2': moistureLevel2,
        'moisture_level_3': moistureLevel3,
        'moisture_level_4': moistureLevel4,
        'aqua_temperature': waterTemperature,
     	'ph': ph,
        'waterlevel' : waterlevel,
    }
    #print dataCollect
    print("- - - - - - - - - - - - - - - - - - - - ")
    print("Collected data for save")
    print json.dumps(dataCollect, indent=4, sort_keys=True)
    
    # Write collected data into json file /conf/data_collect.json
    # this file will be used by boxRoutineCollect.py
    collectPath = utils.getContextPath()+'/conf'
    with open(collectPath+'/data_collect.json', "w") as collectJSONfile:
        json.dump(dataCollect, collectJSONfile, indent=4, separators=(',', ': '))

    ####--------------------------------------------------------------------
    # Step : Use the dataConfiguration from configurations and sensors to control devices
    ####--------------------------------------------------------------------

    # invoke led, fan, pump and dimmer classes
    ledsObj    = ledControllerRef.LedController()
    fanObj     = fanControllerRef.FanController()
    airpumpObj = airpumpRef.AirPumpController()

    print("- - - - - - - - - - - - - - - - - - - - ")
    # execute and update led status
    ledsObj.execute(dataConfiguration)

    print("- - - - - - - - - - - - - - - - - - - - ")
    # enable/disbale fan & pump
    #airpumpObj.set(0)
    fanObj.setOn('front')
    fanObj.setOn('back')
    fanObj.setOn('led')

    time.sleep(15) # enable led fan for 15 secs to cool off system   
   
    fanObj.setOff('front')
    fanObj.setOff('back')
    fanObj.setOff('led')

    print("- - - - - - - - - - - - - - - - - - - - ")
    # indicator checkup
    indicatorObj = indicatorRef.IndicatorPanel() 
    indicatorObj.checkup(baseUrl+"/plantum/download/check?serialnumber="+serialNumber,dataCollect)
    


except Exception,e: 
    utils.log("Processing Configuration :")
    utils.log(str(e))
except:
    utils.log("Processing Configuration : Unknown Error")

