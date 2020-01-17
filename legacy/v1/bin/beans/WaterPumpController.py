#!/usr/bin/python
# IoT Chip project version : 2.0

import sys, getopt
import RPi.GPIO as GPIO
import time, subprocess
import Relay
import utils

class WaterPumpController(object):
    """Class for Water Pump controller"""

    name = "WaterPumpController"
    controller_name = None # relay, radioemitter...
    controller_id = None # must point to controller id (Relay, Radio...)

    controller = None

    def __init__(self):
        confs = utils.getConfiguration(self.name)
        if confs != None :
            try:
                self.controller_name = str(confs['controller_name'])
                self.controller_id = int(confs['controller_id'])
            except:
                print("Notice: some of the Water Pump pins are not used")
            print("WaterPumpController initialized - configuration found")
        else:
            newConfs = [('controller_name',None),('controller_id',None)]
            utils.setConfiguration(self.name,newConfs)
            print("WaterPumpController initialized - Warning: new configuration")

        if self.controller_name.upper() == 'relay'.upper():
            self.controller = Relay.Relay()

    def execute(self,data):
        try:
            if data and 'water_pump_activity' in data and (data['water_pump_activity'] == "0" or data['water_pump_activity'] == "false" or data['water_pump_activity'].lower() == "off") :
                print("Switching Water Pump Off")
                self.controller.setOff(self.controller_id)
            else:
                print("Switching Water Pump On")
                self.controller.setOn(self.controller_id)
        except Exception,e: 
            print("WaterPumpController : "+str(e))
        except:
            print "WaterPumpController : Unknown Error"