#!/usr/bin/python
# IoT Chip project version : 2.0

#import ConfigParser
import os
import utils

class AquaThermometer():

    'Common base class for water temperature controllers'

    name = "AquaThermometer"
    serialNumber = "none"

    def __init__(self):
        confs = utils.getConfiguration(self.name)
        if confs != None :
            self.serialNumber = str(confs['serial_number'])
            print("AquaThermometer initialized - configuration found")
        else:
            serialNumber = self.detectSerialNumber()
            self.serialNumber = serialNumber
            newConfs = [('serial_number',str(serialNumber))]
            utils.setConfiguration(self.name,newConfs)
            print("AquaThermometer initialized - Warning: new configuration")

    def get(self):
        tfile = open("/sys/bus/w1/devices/"+self.serialNumber+"/w1_slave")
        text = tfile.read()
        tfile.close()
        secondline = text.split("\n")[1]
        temperaturedata = secondline.split(" ")[9]
        temperature = float(temperaturedata[2:])
        temperature = temperature / 1000
        return temperature

    def detectSerialNumber(self):
        allDirs = [name for name in os.listdir('/sys/bus/w1/devices/')]
        #print(allDirs)
        if str(allDirs[0]).startswith('28-') and "00000" not in allDirs[0]:
            #print(allDirs[0])
            return allDirs[0]
        else:
            return None
