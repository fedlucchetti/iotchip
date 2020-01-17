#!/usr/bin/python
# IoT Chip project version : 2.0

import DimmerController as dimmerController
import os
import urllib2
import sys, getopt
import utils

class IndicatorPanel():
    """ Indicator Panel Class """

    name = "IndicatorPanel"
    channel_0 = None
    channel_1 = None
    channel_2 = None
    channel_3 = None
    channel_4 = None

    dimmer = None

    def __init__(self):
        self.dimmer = dimmerController.DimmerController()
        confs = utils.getConfiguration(self.name)
        if confs != None :
            self.channel_0 = int(confs['channel_0'])
            self.channel_1 = int(confs['channel_1'])
            self.channel_2 = int(confs['channel_2'])
            self.channel_3 = int(confs['channel_3'])
            self.channel_4 = int(confs['channel_4'])
            print("IndicatorPanel initialized - configuration found")
        else:
            newConfs = [('channel_0',None),('channel_1',None),('channel_2',None),('channel_3',None),('channel_4',None)]
            utils.setConfiguration(self.name,newConfs)
            print("IndicatorPanel initialized - Warning: new configuration")

    def setLed(self,ledNumber,duty):
        channel = getattr(self,'channel_'+str(ledNumber))
        self.dimmer.register({self.name+"_"+str(channel) : {"channel":channel,"duty":duty,"flag":1}})
        #self.pwm.set_pwm(channel, 0, duty)

    def setLedOn(self,ledNumber):
        channel = getattr(self,'channel_'+str(ledNumber))
        self.dimmer.register({self.name+"_"+str(channel) : {"channel":channel,"duty":800,"flag":1}})
        #self.setLed(channel,500)

    def setLedOff(self,ledNumber):
        channel = getattr(self,'channel_'+str(ledNumber))
        self.dimmer.register({self.name+"_"+str(channel) : {"channel":channel,"duty":0,"flag":1}})
        #self.setLed(channel,0)

    def checkup(self,appurl,data):
        """ Method for full system check up - unfinished """
        # if device is on
        if True:
            self.setLedOn(0)
        # if device is connected to Internet
        try:
            response=urllib2.urlopen('http://www.google.com', timeout=1)
            self.setLedOn(1)
        except urllib2.URLError as err:
            self.setLedOff(1)
        # if device can communicate with servers
        try:
            response=urllib2.urlopen(appurl, timeout=1)
            self.setLedOn(2)
        except urllib2.URLError as err: 
            self.setLedOff(2)
        # if usb is used
        if os.path.exists("/dev/video0"):
            self.setLedOn(3)
        else:
            self.setLedOff(3)
        # sensor values in range
        # checks: water temp [17,24], hum [10,95], air temp [17,28], moisture [250,420] 
        self.setLedOff(4)
        if data and 'temperature' in data and (data['temperature'] <= 28 and (data['temperature'] >= 17)) :
            if 'humidity' in data and (data['humidity'] <= 95 and (data['humidity'] >= 10)) :
                if 'aqua_temperature' in data and (data['aqua_temperature'] <= 24 and (data['aqua_temperature'] >= 17)) :
                    if ('moisture_level_1' in data and (data['moisture_level_1'] <= 420 and data['moisture_level_1'] >= 250) and
                        'moisture_level_2' in data and (data['moisture_level_2'] <= 420 and data['moisture_level_2'] >= 250) and
                        'moisture_level_3' in data and (data['moisture_level_3'] <= 420 and data['moisture_level_3'] >= 250) and
                        'moisture_level_4' in data and (data['moisture_level_4'] <= 420 and data['moisture_level_4'] >= 250) ):
                        self.setLedOn(4)
    def main(argv):
        try:
            opts, args = getopt.getopt(sys.argv[1:],"c",[])
            obj = IndicatorPanel()
            if len(opts) > 0:
                for x,y in opts:
                    #print(str(x)+" "+str(y))
                    if x == '-c':
                        obj.setLedOn(0)
                        obj.setLedOff(1)
                        obj.setLedOn(2)
                        obj.setLedOff(3)
                        obj.setLedOn(4)
                        obj.dimmer.runPwm()
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