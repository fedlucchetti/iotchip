#!/usr/bin/python
# IoT Chip project version : 2.0
import datetime
import sys
import json
import urllib2
import time
import subprocess
import os
import logging

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

from beans import utils
from beans import Microchip as microchipRef
from beans import Hygrometer as hygrometerRef
from beans import AquaThermometer as aquaThermometerRef
from beans import Thermometer as thermometerRef
from beans import ThermoHygrometer as thermoHygrometerRef
from beans import Phmeter as phmeterRef
from beans import Moisturemeter as moisturemeterRef
from beans import GpioController as gpioRef

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
moistureDetected = 0
moistureLevel1 = 0
moistureLevel2 = 0
moistureLevel3 = 0
moistureLevel4 = 0
ipText = ""
ipLocalText = ""

### Test Control

x_microchip = True
x_aquathermometer = True
x_thermometer = False       # now retreived from data_collect.json
x_hygrometer = False        # now retreived from data_collect.json
x_thermohygrometer = False  # now retreived from data_collect.json
x_phmeter = False
x_moisturemeter = True
x_send_server_data = True

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
        serialNumber = microchip.getSerialNumber()
        print("Microchip Serial Number : " + serialNumber)
    except Exception,e: 
        utils.log("Microchip :")
        utils.log(str(e))
    except:
        utils.log("Microchip : Unknown Error")

if x_thermometer:
    print("- - - - - - - - - - - - - - - - - - - - ")
    try:
        thermometer = thermometerRef.Thermometer()
        print("Getting Air Temperature...")
        temperature = thermometer.get()
        print(temperature)
    except Exception,e: 
        utils.log("Thermometer :")
        utils.log(str(e))
    except:
        utils.log("Thermometer : Unknown Error")

if x_hygrometer:
    print("- - - - - - - - - - - - - - - - - - - - ")
    try:
        hygrometer = hygrometerRef.Hygrometer()
        print("Getting Air Temperature...")
        humidity = hygrometer.get()
        print(humidity)
    except Exception,e: 
        utils.log("Hygrometer :")
        utils.log(str(e))
    except:
        utils.log("Hygrometer : Unknown Error")

if x_thermohygrometer:
    print("- - - - - - - - - - - - - - - - - - - - ")
    try:
        thmeter = thermoHygrometerRef.ThermoHygrometer()
        print("Getting Air Temperature and Humidity...")
        temperature, humidity = thmeter.get()
        print(temperature)
        print(humidity)
    except Exception,e: 
        utils.log("ThermoHygrometer :")
        utils.log(str(e))
    except:
        utils.log("ThermoHygrometer : Unknown Error")

if x_aquathermometer:
    print("- - - - - - - - - - - - - - - - - - - - ")
    try:
        aquaThermometer = aquaThermometerRef.AquaThermometer()
        print("Getting Water Temperature...")
        waterTemperature = aquaThermometer.get()
        print(waterTemperature)
    except Exception,e: 
        utils.log("AquaThermometer :")
        utils.log(str(e))
    except:
        utils.log("AquaThermometer : Unknown Error")

if x_phmeter:
    print("- - - - - - - - - - - - - - - - - - - - ")
    try:
        phmeter = phmeterRef.Phmeter()
        print("Getting Ph...")
        ph = phmeter.get()
        print(ph)
    except Exception,e: 
        utils.log("Ph-Meter :")
        utils.log(str(e))
    except:
        utils.log("Ph-Meter : Unknown Error")

if x_moisturemeter:
    print("- - - - - - - - - - - - - - - - - - - - ")
    try:
        moisturemeter = moisturemeterRef.Moisturemeter()
        moistureLevel1 = moisturemeter.get(1)
        moistureLevel2 = moisturemeter.get(2)
        moistureLevel3 = moisturemeter.get(3)
        moistureLevel4 = moisturemeter.get(4)
        print(moistureLevel1)
    except Exception,e: 
        utils.log("Moisturemeter :")
        utils.log(str(e))
    except:
        utils.log("Moisturemeter : Unknown Error")

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
    utils.log("IP FAILED : "+str(e))
except:
    utils.log("IP FAILED External Reason")

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
print json.dumps(data, indent=4, sort_keys=True)

###----------------------
### Send Data to server
###----------------------

if x_send_server_data :
    try:
        print("Sending Data to Server...")
        # Send Data
        reqData = urllib2.Request(baseUrl+'/plantum/upload/data')
        reqData.add_header('Content-Type','application/json')
        respData = urllib2.urlopen(reqData,json.dumps(data)).read()
        print(respData)
    except Exception,e:
        utils.log("Sending Data: "+str(e))