#!/usr/bin/python
# IoT Chip project version : 2.0

import time, sys
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import utils

class Phmeter:
    'Common base class for PH Meter sensors'
    
    name= "Phmeter"
    channel = None
    SPI_PORT = 0
    SPI_DEVICE = 0

    def __init__(self):
        confs = utils.getConfiguration(self.name)
        if confs != None :
            self.channel = int(confs['channel'])
            print("Phmeter initialized - configuration found")
        else:
            newConfs = [('channel',None)]
            utils.setConfiguration(self.name,newConfs)
            print("Phmeter initialized - Warning: new configuration")
   
    def get(self):
        print("Getting PH from channel "+str(self.channel)+"...")
        mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(self.SPI_PORT, self.SPI_DEVICE))
        sum = 0
        n = 1
        while n<40:
                value = mcp.read_adc(int(self.channel))
                # print(value)
                sum = sum + value
                mean = sum/n
                adc_voltage = mean*3.3/1023/0.66
                # print(adc_voltage)
                time.sleep(0.5)
                n = n+1

        # convert voltage into pH value using calibration curve
        p0 = 2.307 # read from calibration curve
        p1 = 0 # offs
        ph = p0 * adc_voltage + p1
        return ph
