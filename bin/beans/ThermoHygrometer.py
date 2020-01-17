#!/usr/bin/python
# IoT Chip project version : 2.0

import Adafruit_DHT
import utils

class ThermoHygrometer:
    """Class for air temperature and air humidity sensor"""

    name = "ThermoHygrometer"
    sensor = None
    pin = None
    sensors = { '11': Adafruit_DHT.DHT11, '22': Adafruit_DHT.DHT22, '2302': Adafruit_DHT.AM2302 }

    def __init__(self):
        confs = utils.getConfiguration(self.name)
        if confs != None :
            self.pin = int(confs['pin'])
            self.sensor = confs['sensor']
            print("ThermoHygrometer initialized - configuration found")
        else:
            newConfs = [('pin',None),('sensor',None)]
            utils.setConfiguration(self.name,newConfs)
            print("ThermoHygrometer initialized - Notice: new configuration")

    def get(self):
        utils.log("ThermoHygrometer : trying with sensor "+str(self.sensor)+" and pin "+str(self.pin)+" ...")
        air_hum, air_temp = Adafruit_DHT.read_retry(self.sensors[str(self.sensor)], int(self.pin))
        return air_temp, air_hum
