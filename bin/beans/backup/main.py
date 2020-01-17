#!/usr/bin/python
# IoT Chip project version : 2.0
import datetime
import sys
import json
import urllib2
import time
import subprocess
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

from beans import Microchip as microchipRef
from beans import Hygrometer as hygrometerRef
from beans import AquaThermometer as aquaThermometerRef
from beans import Thermometer as thermometerRef
from beans import ThermoHygrometer as thermoHygrometerRef
from beans import Phmeter as phmeterRef
from beans import ECmeter as ecmeterRef
from beans import Moisturemeter as moisturemeterRef
# from beans import Camera as cameraRef
from beans import CameraUSB as cameraUSBRef
from beans import IndicatorPanel as indicatorRef
from beans import LedController as ledsRef
from beans import FanController as fansRef
from beans import AirPumpController as airPumpRef
from beans import GpioController as gpioRef
from beans import DimmerController as dimmerRef

import beans.utils as utils

###
### IMPORTANT !
### DO NOT ALTER VARIABLES NAMES NOR PARAMETERS
### CHANGING THE VALUES MAY CAUSE THE SCRIPT TO NOT WORK CORRECTLY
###

### Constants

baseUrl = "http://demo.planthive.com"
#baseUrl = "http://192.168.0.101/boxbeta"

### Variables

serialNumber = ""
waterTemperature = 0
temperature = 0
humidity = 0
waterLevel = 0
ph = 0
ec = 0
moistureLevel1 = 0
moistureLevel2 = 0
moistureLevel3 = 0
moistureLevel4 = 0
ipText = ""
ipLocalText = ""

### Test Control

x_microchip = True
x_aquathermometer = False
x_thermohygrometer = False
x_thermometer = False
x_hygrometer = False
x_phmeter = False
x_ecmeter = False
x_moisturemeter = False
x_indicator = False
x_leds = False
x_fans = False
x_airpump = False
x_dimmer = False # should always be true
x_camera = False
x_send_server_data = False
x_send_server_photo = False # x_camera must be True

### temporary test

# udata = { 'spotlight_starttime_hours':9,'spotlight_starttime_minutes':50, 'spotlight_duration_hours':16, 'spotlight_duration_minutes':00 }
# leds = ledsRef.LedController()
# leds.scheduleProcessing(udata)
# print(leds.dutyRed(udata))
# print(leds.dutyBlue(udata))
# sys.exit(0)

###----------------------
# Read Local Data Collection
###----------------------

# Get available data from local json file: conf/data_collect.json
# the values were written in the file by boxRoutineSelf.py
confPath = utils.getContextPath()+'/conf'
with open(confPath+'/data_collect.json') as data_collect_repo:
    dataCollectRepo = json.load(data_collect_repo)
    #print(dataCollectRepo)
temperature = dataCollectRepo["temperature"]
humidity = dataCollectRepo["humidity"]

###----------------------
### Call Sensors and Controllers 
###----------------------

# Power on GPIO
print("- - - - - - - - - - - - - - - - - - - - ")
gpio = gpioRef.GpioController(False)
gpio.powerOn()

if x_microchip :
    print("- - - - - - - - - - - - - - - - - - - - ")
    try:
        microchip = microchipRef.Microchip()
        print("detection: "+microchip.detectSerialNumber())
        serialNumber = microchip.getSerialNumber()
        print("Microchip Serial Number : " + serialNumber)
    except Exception,e: 
        print("Microchip : "+str(e))
    except:
        print "Microchip : Unknown Error"

if x_aquathermometer:
    print("- - - - - - - - - - - - - - - - - - - - ")
    try:
        aquaThermometer = aquaThermometerRef.AquaThermometer()
        print("Getting Water Temperature...")
        waterTemperature = aquaThermometer.get()
        print("Aqua Temperature: "+str(waterTemperature))
    except Exception,e: 
        print "AquaThermometer :"
        print str(e)
    except:
        print "AquaThermometer : Unknown Error"

if x_thermohygrometer:
    print("- - - - - - - - - - - - - - - - - - - - ")
    try:
        thmeter = thermoHygrometerRef.ThermoHygrometer()
        print("Getting Air Temperature and Humidity...")
        temperature, humidity = thmeter.get()
        print(temperature)
        print(humidity)
    except Exception,e: 
        print("ThermoHygrometer : "+str(e))
    except:
        print "ThermoHygrometer : Unknown Error"

if x_thermometer:
    print("- - - - - - - - - - - - - - - - - - - - ")
    try:
        thermometer = thermometerRef.Thermometer()
        print("Getting Air Temperature...")
        temperature = thermometer.get()
        print(temperature)
    except Exception,e: 
        print("Thermometer : "+str(e))
    except:
        print "Thermometer : Unknown Error"

if x_hygrometer:
    print("- - - - - - - - - - - - - - - - - - - - ")
    try:
        hygrometer = hygrometerRef.Hygrometer()
        print("Getting Air Humidity...")
        humidity = hygrometer.get()
        print(humidity)
    except Exception,e: 
        print("Hygrometer : "+str(e))
    except:
        print "Hygrometer : Unknown Error"

if x_phmeter:
    print("- - - - - - - - - - - - - - - - - - - - ")
    try:
        phmeter = phmeterRef.Phmeter()
        ph = phmeter.get()
        print(ph)
    except Exception,e: 
        print("Ph-Meter :"+str(e))
    except:
        print "Ph-Meter : Unknown Error"

if x_ecmeter:
    print("- - - - - - - - - - - - - - - - - - - - ")
    try:
        ecmeter = ecmeterRef.ECmeter()
        ec = ecmeter.get(temperature)
        print(ec)
    except Exception,e: 
        print("EC-Meter :"+str(e))
    except:
        print "EC-Meter : Unknown Error"

if x_moisturemeter:
    print("- - - - - - - - - - - - - - - - - - - - ")
    try:
        moisturemeter = moisturemeterRef.Moisturemeter()
        moistureLevel1 = moisturemeter.get(1)
        #moistureLevel2 = moisturemeter.get(2)
        #moistureLevel3 = moisturemeter.get(3)
        #moistureLevel4 = moisturemeter.get(4)
        print(str(moistureLevel1)+" "+str(moistureLevel2)+" "+str(moistureLevel3)+" "+str(moistureLevel4))
    except Exception,e: 
        print("Moisturemeter :"+str(e))
    except:
        print "Moisturemeter : Unknown Error"

if x_indicator:
    print("- - - - - - - - - - - - - - - - - - - - ")
    try:
        indicator = indicatorRef.IndicatorPanel()
        indicator.checkup(baseUrl+"/plantum/download/check?serialnumber="+serialNumber)
        
        #indicator.setLedOn(0)
        #indicator.setLedOff(1)
        #indicator.setLedOff(2)
        #indicator.setLedOn(3)
        #indicator.setLedOff(4)
        
        print("Done Testing IndicatorPanel")
    except Exception,e:
        print("IndicatorPanel : "+str(e))
    except:
        print("IndicatorPanel: Unknown Error")

if x_leds:
    print("- - - - - - - - - - - - - - - - - - - - ")
    try:
        leds = ledsRef.LedController()
        leds.set(0,400)
        leds.set(1,300)
        print("Done Testing LEDs")
    except Exception,e:
        print("LEDs : ")
        print(str(e))
    except:
        print("LEDs: Unknown Error")

if x_fans:
    print("- - - - - - - - - - - - - - - - - - - - ")
    try:
        fans = fansRef.FanController()
        fans.setOn(0)
        fans.setOn(1)
        fans.setOn(2)
        fans.setOff(0)
        fans.setOff(1)
        fans.setOff(2)
        print("Done Testing Fans")
    except Exception,e:
        print("Fans : ")
        print(str(e))
    except:
        print("Fans: Unknown Error")

if x_airpump:
    print("- - - - - - - - - - - - - - - - - - - - ")
    try:
        airpump = airPumpRef.AirPumpController()
        airpump.setOn()
        print("Done Testing AirPump")
    except Exception,e:
        print("AirPump : ")
        print(str(e))
    except:
        print("AirPump: Unknown Error")

if x_camera:
    try:
        camera = cameraUSBRef.CameraUSB()
        time.sleep(1); print("."); time.sleep(1); print("."); time.sleep(1); print("."); time.sleep(1); print("."); time.sleep(1); print(".");
        print("Trying to Snapshot...")
        photo = camera.capture()
        time.sleep(1); print("."); time.sleep(1); print("."); time.sleep(1); print("."); time.sleep(1); print("."); 
        # camera.cleanUpRepository(False)
        print(photo)
    except Exception,e: 
        print "CameraUSB :"
        print str(e)
    except:
        print "CameraUSB : Unknown Error"

if x_dimmer:
    try:
        dimmer = dimmerRef.DimmerController()
        dimmer.runPwm()
    except Exception,e: 
        print "Dimmer :"
        print str(e)
    except:
        print "Dimmer : Unknown Error"

# Power off GPIO
gpio.powerOff()

### -----------------------------------------------------

###----------------------
### Get IP on LAN and WAN
###----------------------

### WAN

timestamp = int(time.time())*1000.0
try:
    ipTok = ["""wget http://ipinfo.io/ip -qO -"""]
    ipText = subprocess.check_output(ipTok,shell=True)
    if (len(ipText) > 16) or (len(ipText) < 7) :
        ipText = ""
except Exception,e:
    print("IP FAILED : "+str(e))
except:
    print("IP FAILED External Reason")

### LAN

## alternative cmd 
## ipLocalTok = ["""ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'"""]
ipLocalTok = ["""hostname -I"""]
ipLocalText = subprocess.check_output(ipLocalTok,shell=True)
ipLocalText.join(ipLocalText.strip('\n') for ipLocalText in ipLocalText)
ipLocalText.join(ipLocalText for ipLocalText in ipLocalText if ipLocalText.isalnum())
ipLocalText = ipLocalText.replace('\n', ' ').replace('\r', '')
if (len(ipLocalText) > 16) or (len(ipLocalText) < 7) :
    ipLocalText = "255.255.255.255"
if not ipLocalText.startswith('192') :
    ipLocalText = utils.getIPAddress('wlan0')
    print("LAN IP: "+str(ipLocalText))
    
###----------------------
### Package Data in collection
###----------------------

data = {
 	'serialnumber': serialNumber,
 	'datetime': timestamp,
 	'temperature': temperature,
 	'humidity': humidity,
 	'ph': ph,
    'moisture_level_1': moistureLevel1,
    'moisture_level_2': moistureLevel2,
    'moisture_level_3': moistureLevel3,
    'moisture_level_4': moistureLevel4,
 	'aqua_temperature': waterTemperature,
    'waterlevel' : waterLevel,
    'ipaddress' : ipText,
    'iplocal' : ipLocalText,
}
#print(data)
print json.dumps(data, indent=4, sort_keys=True)

###----------------------
### Send Data to server
###----------------------

if x_send_server_data :
    print("- - - - - - - - - - - - - - - - - - - - ")
    print("Sending Data to Server...")
    # Send Data
    reqData = urllib2.Request(baseUrl+'/plantum/upload/data')
    reqData.add_header('Content-Type','application/json')
    respData = urllib2.urlopen(reqData,json.dumps(data)).read()
    print(respData)

if x_send_server_photo and x_camera :
    print("- - - - - - - - - - - - - - - - - - - - ")
    print("Sending Photo to Server...")
    # Send Snapshot
    register_openers()
    datagen, headers = multipart_encode({
        "img": open(photo, "rb"),
        "serialnumber": serialNumber,
    })
    reqPhoto = urllib2.Request(baseUrl+'/plantum/upload/photo', datagen, headers)
    respPhoto = urllib2.urlopen(reqPhoto).read()
    print(respPhoto)

