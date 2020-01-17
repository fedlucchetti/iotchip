#!/usr/bin/python
# IoT Chip project version : 3.0

from si7021 import Si7021
import utils
from time import sleep
from smbus import SMBus

class Hygrometer:
    """Common base class for air humidity sensors"""

    name = "Hygrometer"
    sensor = None
    pin = None

    def __init__(self):
        confs = utils.getConfiguration(self.name)
        print("Hygrometer initialized - configuration found")
        sensor = Si7021(SMBus(1))


    def get(self):
        hygro = sensor.read()
        return hygro
