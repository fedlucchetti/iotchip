#!/usr/bin/env python3
# IoT Chip project version : 2.0
import time
import utils
import urllib2
import os
import json
import sys, getopt

import ExecutePWM 

 


class FrontLED():
    """ FrontLED Class """

    name = "FrontLED"
    channel = None

    dimmer  = None
    strip   = None
    channel_0 = None
    channel_1 = None
    channel_2 = None
    channel_3 = None
    channel_4 = None

    def __init__(self):
        # LED strip configuration:
        LED_COUNT      = 5      # Number of LED pixels.
        #LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
        #LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
        LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
        LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
        LED_BRIGHTNESS = 80     # Set to 0 for darkest and 255 for brightest
        LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
        LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
        confs = utils.getConfiguration(self.name)
        if confs != None :
            self.channel = confs['channel']
            if self.channel!='None':
                self.channel = int(self.channel)
            else:
                self.channel = False
            print("FrontLED initialized - configuration found")
        else:
            self.channel = 18
            newConfs = [('channel',None)]
            utils.setConfiguration(self.name,newConfs)
            print("FrontLED initialized - Warning: new configuration")

        
        if self.channel != False:
            #from neopixel import *
            import neopixel
            # Create NeoPixel object with appropriate configuration.
            self.strip = neopixel.Adafruit_NeoPixel(LED_COUNT, self.channel, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
            # Intialize the library (must be called once before other functions).
            self.strip.begin()
            print("LED Strip  initialized")
        else:
            self.dimmer = ExecutePWM.ExecutePWM()
            confs = utils.getConfiguration(self.name)
            if confs != None :
                self.channel_0 = int(confs['channel_0'])
                self.channel_1 = int(confs['channel_1'])
                self.channel_2 = int(confs['channel_2'])
                self.channel_3 = int(confs['channel_3'])
                self.channel_4 = int(confs['channel_4'])
                print("Old IndicatorPanel initialized - configuration found")
            else:
                newConfs = [('channel_0',None),('channel_1',None),('channel_2',None),('channel_3',None),('channel_4',None)]
                utils.setConfiguration(self.name,newConfs)
                print("Old IndicatorPanel initialized - Warning: new configuration")

            
        
    def getgrb(self,color):
        if color=='g':
            grb = Color(255, 0  , 0  )
        elif color == 'r':
            grb = Color(0  , 255, 0  )
        elif color == 'b':
            grb = Color(0  , 0  , 255)
        elif color == 'o':
            grb = Color(75, 255, 0  )
        elif color == 'y':
            grb = Color(255, 255, 0  )
        elif color == 't':
            grb = Color(200, 0, 255)
        elif color == 'v':
            grb = Color(0, 255  , 180)
        elif color == 'w':
            grb = Color(255, 255, 255)
        elif color == '':
            grb = Color(0     , 0  , 0  )
        else:
            print('Invalid color string')
            grb = Color(0  , 0  , 0  )
        
        return grb
    
    def setOn(self,ledNumber,color):
        if self.channel!=False:
            grb = self.getgrb(color)
            self.strip.setPixelColor(ledNumber, grb)
            self.strip.show()
        else:
            pca_channel = getattr(self,'channel_'+str(ledNumber))
            self.dimmer.register({self.name+"_"+str(pca_channel) : {"channel":pca_channel,"duty":800,"flag":1}})
        


    def setOff(self,ledNumber):
        if self.channel!=False:
            grb = self.getgrb('off')
            self.strip.setPixelColor(ledNumber, grb)
            self.strip.show()
        else:
            pca_channel = getattr(self,'channel_'+str(ledNumber))
            self.dimmer.register({self.name+"_"+str(pca_channel) : {"channel":pca_channel,"duty":0,"flag":1}})


    
    def setArray(self,colorarray,delay=50/1000.0):
        if self.channel!=False:
            for i in range(self.strip.numPixels()):
                grb = self.getgrb(colorarray[i])
                self.strip.setPixelColor(i, grb)
                self.strip.show()
                time.sleep(delay)
        else:
            for i in range(5):
                if colorarray[i] =='g':
                    pca_channel = getattr(self,'channel_'+str(i))
                    self.dimmer.register({self.name+"_"+str(pca_channel) : {"channel":pca_channel,"duty":800,"flag":1}})
                else:
                    pca_channel = getattr(self,'channel_'+str(i))
                    self.dimmer.register({self.name+"_"+str(pca_channel) : {"channel":pca_channel,"duty":0,"flag":1}})
                 
                

    def checkup(self):
        colorarray = ['','','','','']
        """ Method for full system check up - unfinished """
        # if device is on
        if True:
            #self.setLedOn(0,'g')
            colorarray[0]='g'
            
        # if device is connected to Internet
        try:
            response=urllib2.urlopen('http://www.google.com', timeout=1)
            #self.setLedOn(1,'g')
            colorarray[1]='g'
        except urllib2.URLError as err:
            #self.setLedOff(1)
            colorarray[1]=''
            
        # if device can communicate with servers
        try:
            conf = utils.getConfiguration('BaseURL')
            base = conf['path']
            try:
                serialNumber = utils.getSerialNumber()
            except Exception,e: 
                utils.log("Microchip: ")
                utils.log(str(e))
            except:
                utils.log("Microchip: Unknown Error")
            appurl = base +"/api/v1/en/planthive/get-device-command/" + str(serialNumber)
            response=urllib2.urlopen(appurl, timeout=1)
            #self.setLedOn(2,'g')
            colorarray[2]='g'
        except urllib2.URLError as err: 
            #self.setLedOff(2)
            colorarray[2]=''
        
        # if usb is used
        if os.path.exists("/dev/video0"):
            #self.setLedOn(0,'b')
            colorarray[0]='b'
        else:
            #self.setLedOff(0,'g')
            colorarray[0]='g'
        
        # sensor values in range
        # checks: water temp [17,24], hum [10,95], air temp [17,28], moisture [250,420] 
        #self.setLedOff(3)
        try:
            colorarray[3]=''
            data_path = '/home/pi/iotchip/data/new_data2send.json'
            with open(data_path) as f:
            			data = json.load(f)
            
            data_path = '/home/pi/iotchip/conf/fetched_data.json'
            with open(data_path) as g:
            			lim_data = json.load(g)
            
            
            if data and 'temperature' in data and 'humidity' in data:
                if data['temperature'] < lim_data['payload']['temperatureMin']:
                    #self.setLedOn(3,'b')
                    colorarray[3]='b'
                elif data['temperature'] > lim_data['payload']['temperatureMax']:
                    #self.setLedOn(3,'r')
                    colorarray[3]='r'
                elif (data['temperature'] >= lim_data['payload']['temperatureMin'] and data['temperature'] <= lim_data['payload']['temperatureMax']):     
                    #self.setLedOn(3,'g')
                    colorarray[3]='g'
                elif data['humidity'] < lim_data['payload']['humidityMin']:
                    #self.setLedOn(3,'o')
                    colorarray[3]='o'
                elif data['humidity'] > lim_data['payload']['humidityMax']:
                    #self.setLedOn(3,'t')
                    colorarray[3]='t'
                elif (data['humidity'] >= lim_data['payload']['humidityMin'] and data['humidity'] <= lim_data['payload']['humidityMax']):     
                    #self.setLedOn(3,'g')
                    colorarray[3]='g'
                
            else:
                #self.setLedOff(3)
                colorarray[3]=''
    
            if data and 'moistures' in data and lim_data['payload']['medium']=='0':
                if data['moistures'] < lim_data['payload']['moistureMin']:
                    #self.setLedOn(3,'b')
                    colorarray[4]='o'
                elif data['moistures'] >= lim_data['payload']['moistureMin']:     
                    #self.setLedOn(3,'g')
                    colorarray[4]='g'
            elif data and 'waterTemperature' in data and lim_data['payload']['medium']=='1':
                if data['waterTemperature'] < lim_data['payload']['waterTemperatureMin']:
                    #self.setLedOn(3,'o')
                    colorarray[4]='o'
                elif data['waterTemperature'] > lim_data['payload']['waterTemperatureMax']:
                    #self.setLedOn(3,'t')
                    colorarray[4]='b'
                elif (data['waterTemperature'] >= lim_data['payload']['waterTemperatureMin'] and data['waterlevel'] <= lim_data['payload']['waterTemperatureMax']):     
                    #self.setLedOn(3,'g')
                    colorarray[4]='g'
                    
            else:
                #self.setLedOff(3)
                colorarray[4]='o'
        except:
            colorarray[4]='o'



        self.setArray(colorarray)
        
            

    def test():
        print('IndicatorPanel.main checkup')
        
        self.setArray(['g','g','g','g','g',],0.3)
        self.setArray(['r','r','r','r','r',],0.3)
        self.setArray(['b','b','b','b','g',],0.3)
        self.setArray(['o','o','o','o','o',],0.3)
        self.setArray(['t','t','t','t','t',],0.3)
        self.setArray(['w','w','w','w','w',],0.3)


    def main(argv):
        try:
            opts, args = getopt.getopt(sys.argv[1:],"c",[])
            obj = FrontLED()
            if len(opts) > 0:
                for x,y in opts:
                    #print(str(x)+" "+str(y))
                    if x == '-c':
                        print('IndicatorPanel.main checkup')
                        
                        obj.setArray(['g','g','g','g','g',],0.3)
                        obj.setArray(['r','r','r','r','r',],0.3)
                        obj.setArray(['b','b','b','b','g',],0.3)
                        obj.setArray(['o','o','o','o','o',],0.3)
                        obj.setArray(['t','t','t','t','t',],0.3)
                        obj.setArray(['w','w','w','w','w',],0.3)
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
    obj = FrontLED()
    obj.checkup()