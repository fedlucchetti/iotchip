#!/usr/bin/python
# IoT Chip project version : 2.0

import RPi.GPIO as GPIO
import time
import subprocess
import sys, getopt
import utils

class GpioController():
    """description of class GpioController"""

    name = "GpioController"
    pin = 26

    def __init__(self,warnings=True):
        GPIO.setwarnings(warnings)
        print("GPIO warnings are set to "+str(warnings))
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin,GPIO.OUT)
        print("GPIO over pin "+str(self.pin)+" initialized")

    def powerOn(self):
        GPIO.output(self.pin,1)

    def powerOff(self):
        GPIO.output(self.pin,0)
