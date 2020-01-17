#!/usr/bin/python
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
from beans import CameraUSB as cameraUSBRef

###
### IMPORTANT !
### DO NOT ALTER VARIABLES NAMES NOR PARAMETERS
### CHANGING THE VALUES MAY CAUSE THE SCRIPT TO NOT WORK CORRECTLY
###

### Variables

baseUrl = "http://demo.planthive.com"
#baseUrl = "http://192.168.0.101/boxbeta"
serialNumber = ""
photo = ""

### Control

x_microchip = True # always true as serial number is needed
x_camera = True # if this one if off, no request will be sent
x_send_server_photo = True # x_camera must be True

### Sensors and Controllers 

if x_microchip :
    try:
        microchip = microchipRef.Microchip()
        serialNumber = microchip.getSerialNumber()
        print("Microchip Serial Number: " + serialNumber)
    except Exception,e: 
        utils.log("Microchip :")
        utils.log(str(e))
    except:
        utils.log("Microchip : Unknown Error")


if x_camera:
    try:
        camera = cameraUSBRef.CameraUSB()
        time.sleep(1); utils.log("."); time.sleep(1); utils.log(".");
        print("Trying to Snapshot...")
        photo = camera.capture()
        camera.cleanUpRepository(True)
        print(photo)
    except Exception,e: 
        utils.log("CameraUSB :")
        utils.log(str(e))
    except:
        utils.log("CameraUSB : Unknown Error")

### ------------------------------- ###
### ------------------------------- ###
### ------------------------------- ###

### Send Data to server

if x_send_server_photo and x_camera :
    print("Trying to send photo...")
    # Send Snapshot
    register_openers()
    try:
        datagen, headers = multipart_encode({
            "img": open(photo, "rb"),
            "serialnumber": serialNumber,
        })
        reqPhoto = urllib2.Request(baseUrl+'/plantum/upload/photo', datagen, headers)
        respPhoto = urllib2.urlopen(reqPhoto).read()
        print(respPhoto)
    except Exception,e:
        utils.log("Send Photo: ")
        utils.log(str(e))
    except:
        utils.log("Send Photo: Unknown Error")
