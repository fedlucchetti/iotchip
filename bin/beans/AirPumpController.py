#!/usr/bin/python
# IoT Chip project version : 2.0

import DimmerController as dimmerController
#import os, sys, getopt
import utils

class AirPumpController:
    """description of class AirPumpController"""

    name = "AirPumpController"
    channel = None

    dimmer = None

    def __init__(self):
        self.dimmer = dimmerController.DimmerController()
        confs = utils.getConfiguration(self.name)
        if confs != None :
            self.channel = int(confs['channel'])
            print("AirPumpController initialized - configuration found")
        else:
            newConfs = [('channel',None)]
            utils.setConfiguration(self.name,newConfs)
            print("AirPumpController initialized - Warning: new configuration")

    def setOn(self):
        print("Pump ON")
        self.dimmer.register({self.name+"_"+str(self.channel) : {"channel":self.channel,"value":4095}})
        #self.pwm.set_pwm(int(self.channel), 0, 4095)

    def setOff(self):
        self.dimmer.register({self.name+"_"+str(self.channel) : {"channel":self.channel,"value":0}})
        print("Pump OFF")
        #self.pwm.set_pwm(int(self.channel), 0, 0)

    def set(self,value):
        self.dimmer.register({self.name+"_"+str(self.channel) : {"channel":self.channel,"value":value}})
        print("PWM set")
        #self.pwm.set_pwm(int(self.channel), 0, 0)