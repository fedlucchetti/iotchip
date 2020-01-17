#!/usr/bin/python
# IoT Chip project version : 2.0

import time
import subprocess
import math as maths
import urllib2
import sys, getopt

import utils
#import Microchip as microchipRef

class IndicatorPanel():
    """ Indicator Panel Class """

    name = "IndicatorPanel"
    i2cBus = "0x20"
    regA = "0x14"
    regB = "0x15"
    model = "1"
    reg_0_7 = ['0','0','0','0', '0','0','0','0']
    reg_8_15 = ['0','0','0','0', '0','0','0','0']

    def __init__(self):
        print(str(self.name)+" initialized")

    def _translate(self):
        composition_0_7 = ''.join(self.reg_0_7)
        composition_8_15 = ''.join(self.reg_8_15)
        #print(composition_8_15 + " " + composition_0_7)
        hexa_0_7 = hex(int(composition_0_7,2))
        hexa_8_15 = hex(int(composition_8_15,2))
        #print(hexa_0_7+" "+hexa_8_15)
        fhexa_0_7 = "{0:#0{1}x}".format(int(hexa_0_7,16),4)
        fhexa_8_15 = "{0:#0{1}x}".format(int(hexa_8_15,16),4)
        #print(fhexa_0_7+" "+fhexa_8_15)
        return fhexa_0_7, fhexa_8_15

    def setLed(self,ledNumber,onOff):
        # onOff = '0' or '1'
        if ledNumber < 8:
            ledArrNumber = 8-ledNumber%8
            self.reg_0_7[ledArrNumber-1] = str(onOff)
        elif ledNumber >= 8 and ledNumber < 16:
            ledNumber = ledNumber%8
            ledArrNumber = 8-(ledNumber%8)
            self.reg_8_15[ledArrNumber-1] = str(onOff)
        else:
            return
        hexas = self._translate()
        #print(str(hexas[0])+" "+str(hexas[1]))
        subprocess.call(["sudo", "i2cset", "-y", self.model, self.i2cBus, self.regA, str(hexas[0])])
        subprocess.call(["sudo", "i2cset", "-y", self.model, self.i2cBus, self.regB, str(hexas[1])])

    def setLedOn(self,ledNumber):
        self.setLed(ledNumber,'1')

    def setLedOff(self,ledNumber):
        self.setLed(ledNumber,'0')

    def checkup(self,microchipSerialNumber):
        """ Method for full system check up - unfinished """
        # microchip = microchipRef.Microchip()
        # if device is on
        if True:
            self.setLedOff(3)
            self.setLedOn(1)
        # if device is connected to Internet
        try:
            response=urllib2.urlopen('http://www.google.com', timeout=1)
            self.setLedOn(4)
            self.setLedOff(6)
        except urllib2.URLError as err:
            self.setLedOff(4)
            self.setLedOn(6)
        # if device can communicate with servers (not implemented)
        try:
            response=urllib2.urlopen('http://www.demodom.live/boxdemo/plantum/checkcom?sn='+microchipSerialNumber, timeout=1)
            self.setLedOn(7)
            self.setLedOff(9)
        except urllib2.URLError as err: 
            self.setLedOff(7)
            self.setLedOn(9)
        # if plant state is ok (not implemented)
        if True :
            self.setLedOff(10)
            self.setLedOn(12)
        # 5th set of leds not attributed (not implemented)
        self.setLedOff(13)
        self.setLedOn(14)
        self.setLedOff(15)

    def wave():
        """ test method """
        subprocess.call(["sudo", "i2cset", "-y", "1", "0x20", "0x00", "0x00"])
        subprocess.call(["sudo", "i2cset", "-y", "1", "0x20", "0x01", "0x00"])
        while True:
            subprocess.call(["sudo", "i2cset", "-y", "1", "0x20", "0x14", "0x02"])
            subprocess.call(["sudo", "i2cset", "-y", "1", "0x20", "0x14", "0x04"])
            subprocess.call(["sudo", "i2cset", "-y", "1", "0x20", "0x14", "0x08"])
            subprocess.call(["sudo", "i2cset", "-y", "1", "0x20", "0x14", "0x10"])
            subprocess.call(["sudo", "i2cset", "-y", "1", "0x20", "0x14", "0x20"])
            subprocess.call(["sudo", "i2cset", "-y", "1", "0x20", "0x14", "0x40"])
            subprocess.call(["sudo", "i2cset", "-y", "1", "0x20", "0x14", "0x80"])
            subprocess.call(["sudo", "i2cset", "-y", "1", "0x20", "0x14", "0x00"])
            
            subprocess.call(["sudo", "i2cset", "-y", "1", "0x20", "0x15", "0x01"])
            subprocess.call(["sudo", "i2cset", "-y", "1", "0x20", "0x15", "0x02"])
            subprocess.call(["sudo", "i2cset", "-y", "1", "0x20", "0x15", "0x04"])
            subprocess.call(["sudo", "i2cset", "-y", "1", "0x20", "0x15", "0x08"])
            subprocess.call(["sudo", "i2cset", "-y", "1", "0x20", "0x15", "0x10"])
            subprocess.call(["sudo", "i2cset", "-y", "1", "0x20", "0x15", "0x20"])
            subprocess.call(["sudo", "i2cset", "-y", "1", "0x20", "0x15", "0x40"])
            subprocess.call(["sudo", "i2cset", "-y", "1", "0x20", "0x15", "0x80"])

            subprocess.call(["sudo", "i2cset", "-y", "1", "0x20", "0x14", "0xFF"])
            subprocess.call(["sudo", "i2cset", "-y", "1", "0x20", "0x15", "0xFF"])
            
            subprocess.call(["sudo", "i2cset", "-y", "1", "0x20", "0x14", "0x00"])
            subprocess.call(["sudo", "i2cset", "-y", "1", "0x20", "0x15", "0x00"])


            subprocess.call(["sudo", "i2cset", "-y", "1", "0x20", "0x14", "0xFF"])
            subprocess.call(["sudo", "i2cset", "-y", "1", "0x20", "0x15", "0xFF"])

    def main(argv):
        try:
            opts, args = getopt.getopt(sys.argv[1:],"c",[])
            obj = IndicatorPanel()
            if len(opts) > 0:
                for x,y in opts:
                    #print(str(x)+" "+str(y))
                    if x == '-c':
                        obj.checkup("00000000")
                        print('IndicatorPanel.main checkup')
            else:
                print 'IndicatorPanel.main -c'
        except getopt.GetoptError,e:
            print("IndicatorPanel.main GetoptError: "+str(e))
        except Exception,ex:
            print("IndicatorPanel.main Exception: "+str(ex))
        except:
            print("IndicatorPanel.main unknown error")

if __name__ == "__main__":
    IndicatorPanel().main()