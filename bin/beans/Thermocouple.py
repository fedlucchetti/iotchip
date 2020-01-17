#!/usr/bin/python
# IoT Chip project version : 3.0

#import ConfigParser
import os
import utils
import mcp9600
import time

class Thermocouple():

    'Common base class for water temperature controllers'

    name = "Thermocouple"

    def __init__(self):
        m = mcp9600.MCP9600()


    def get(self):
        temperature = m.get_hot_junction_temperature()
        c = m.get_cold_junction_temperature()
        d = m.get_temperature_delta()
        return temperature


