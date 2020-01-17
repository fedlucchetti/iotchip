#!/usr/bin/python
# IoT Chip project version : 2.0

import ConfigParser
import os
import RPi.GPIO as GPIO
import time
from beans import utils

class UltrasoundProbe:
    
    name = "UltrasoundProbe"
    trig = 23
    echo = 24

    def __init__(self):
        confs = utils.getConfiguration(self.name)
        if confs != None :
            self.trig = int(confs['trig'])
            self.echo = int(confs['echo'])
            print("UltrasoundProbe initialized - configuration found")
        else:
            newConfs = [('trig',None),('echo',None)]
            utils.setConfiguration(self.name,newConfs)
            print("UltrasoundProbe initialized - Warning: new configuration")
    
    def get(self):
        GPIO.setmode(GPIO.BCM)
        print "Distance Measurement In Progress"
        utils.log("Distance Measurement In Progress")
        
        GPIO.setup(self.trig,GPIO.OUT)
        GPIO.output(self.trig, GPIO.LOW)
        GPIO.setup(self.echo,GPIO.IN)
        GPIO.output(self.trig, False)

        print "Waiting For Sensor To Settle"
        utils.log("Waiting For Sensor To Settle")
        time.sleep(2)

        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)

        while GPIO.input(self.echo)==0:
            pulse_start = time.time()

        while GPIO.input(self.echo)==1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)

        print "Distance:",distance,"cm"
        utils.log("Distance: "+str(distance)+"cm")

        GPIO.cleanup()
        return distance
