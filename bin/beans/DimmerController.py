#!/usr/bin/python
# IoT Chip project version : 2.0

from __future__ import division
import utils
import json
import os, sys
import time

class DimmerController():
    """description of class DimmerController"""

    name = "DimmerController"
    pwm = None

    def __init__(self):
        print("DimmerController initialized")

    def getPwm(self):
        return self.pwm

    def register(self,data):
        confPath = utils.getContextPath()+'/conf'
        utils.updateJSONFile(confPath+'/pwm_conf.json',data)

    def runPwm(self):
        import Adafruit_PCA9685
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(1000)
        confPath = utils.getContextPath()+'/conf'
        with open(confPath+'/pwm_conf.json') as data_file:    
            data = json.load(data_file)
        for key, value in data.iteritems():
           print(value["value"])
           if value["flag"]==1 and value["value"] >=0 and value["value"] <=4095:
               self.pwm.set_pwm(value["channel"], 0, value["value"])
               self.register({key : {"channel":channel,"value":duty,"flag":1}})
               
