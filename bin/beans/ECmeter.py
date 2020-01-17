#!/usr/bin/python
# IoT Chip project version : 2.0

import time, sys
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import utils

class ECmeter:
    'Class for EC Meter'

    name= "ECmeter"
    channel = None
    SPI_PORT   = 0
    SPI_DEVICE = 0

    def __init__(self):
        confs = utils.getConfiguration(self.name)
        if confs != None :
            self.channel = int(confs['channel'])
            print("ECmeter initialized - configuration found")
        else:
            newConfs = [('channel',None)]
            utils.setConfiguration(self.name,newConfs)
            print("ECmeter initialized - Warning: new configuration")

    def get(self, temperature):
        print("Getting EC from channel "+str(self.channel)+"...")
        mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(self.SPI_PORT, self.SPI_DEVICE))
        sum = 0
        n = 1
        while n<40:
            value = mcp.read_adc(int(self.channel))
            sum = sum + value
            mean = float(sum/n)
            # print(mean*3.3/1023/0.66)
            time.sleep(0.5)
            n = n+1
        alpha = float(3.3/5) # 
        adcvoltage = mean*3.3/1023/alpha
        
        # temperature = 22 # default, has to be adjusted later, after Armenia please!
        TempCoefficient = 1.0+0.0185*(temperature-25.0); 
        # temperature compensation formula: fFinalResult(25^C) = fFinalResult(current)/(1.0+0.0185*(fTP-25.0));
        CoefficientVoltage = adcvoltage/TempCoefficient;

        if CoefficientVoltage<150:
            print("No Solution") # 25^C 1413us/cm<-->about 216mv  if the voltage(compensate)<150,that is <1ms/cm,out of the range
            return 0
        elif CoefficientVoltage>3300:
            print("Out of the range!") # >20ms/cm,out of the range
            return 0
        else:
            if CoefficientVoltage<=448:
                ECcurrent=6.84*CoefficientVoltage-64.32 # 1ms/cm<EC<=3ms/cm
            elif CoefficientVoltage<=1457:
                ECcurrent=6.98*CoefficientVoltage-127;  # 3ms/cm<EC<=10ms/cm
            else:
                ECcurrent=5.3*CoefficientVoltage+2278;  # 10ms/cm<EC<20ms/cm
            ECcurrent = ECcurrent/1000 # convert us/cm to ms/cm
            # print("EC current = " + str(ECcurrent) + "ms/cm")
            return ECcurrent