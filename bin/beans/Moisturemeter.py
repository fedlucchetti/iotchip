#!/usr/bin/python
# IoT Chip project version : 2.0

import time
import sys
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import utils

class Moisturemeter():
    """Class for Moisturemeter"""

    name= "Moisturemeter"
    channel_1 = None
    channel_2 = None
    channel_3 = None
    channel_4 = None
    SPI_PORT = 0
    SPI_DEVICE = 0

    def __init__(self):
        confs = utils.getConfiguration(self.name)
        if confs != None :
            self.channel_1 = int(confs['channel_1'])
            self.channel_2 = int(confs['channel_2'])
            self.channel_3 = int(confs['channel_3'])
            self.channel_4 = int(confs['channel_4'])
            print("Moisturemeter initialized - configuration found")
        else:
            # newConfs = [('channel',None)]
            # utils.setConfiguration(self.name,newConfs)
            print("Moisturemeter initialized - Warning: configuration not found")
   
    def get(self,channelNumber):
        print("getting moisture...")
        theChannel = getattr(self,'channel_'+str(channelNumber))
        print("Getting Moisture from channel "+str(theChannel)+"...")
        mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(self.SPI_PORT, self.SPI_DEVICE))
        sum = 0
        n = 1
        while n<20:
                value = mcp.read_adc(int(theChannel))
                # print(value)
                sum = sum + value
                mean = sum/n
                # mean = float(mean)
                # print(adc_voltage)
                time.sleep(0.5)
                n = n+1

        mean = float(mean)
        moisture = 100*(1-mean/1023)
        return moisture
