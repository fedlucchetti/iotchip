#!/usr/bin/python
import ConfigParser
import os
import time
from beans import utils
import RPi.GPIO as GPIO

class MoistureDetector(object):

    # Common base class for air Moisture Detection sensors

    name = "MoistureDetector"
    pin = 0 # may vary across different chips, read from conf/keys.ini 

    def __init__(self):
        config = ConfigParser.ConfigParser()
        #confPath = os.path.dirname(__file__) + '/../../conf/keys.ini'
        confPath = utils.getContextPath()+'/conf/keys.ini'
        config.read(confPath)
        if config.has_section(self.name):
            self.pin = config.getint(self.name, 'pin')
        else :
            try :
                config.add_section(self.name)
                config.set(self.name, "pin", 0)
                with open(confPath, 'wb') as configfile:
                    config.write(configfile)
            except Exception,e:
                print(self.name+" Config Key: " + str(e))
   
    def get(self):
        try :
            reading = 0
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.OUT)
            GPIO.output(self.pin, GPIO.LOW)
            time.sleep(0.1) 
            GPIO.setup(self.pin, GPIO.IN)
            returnValue = 0
            while True:
                if (GPIO.input(self.pin) == GPIO.LOW):
                    reading += 1
                if reading >= 1000:
                    returnValue = 0
                    print 'MoistureDetector with pin %d : %d' % (self.pin,returnValue)
                    return 0
                if (GPIO.input(self.pin) != GPIO.LOW):
                    returnValue = 1
                    print 'MoistureDetector with pin %d : %d' % (self.pin,returnValue)
                    return 1
        except Exception,e:
            utils.log("MoistureDetector Error: "+str(e))
            print("MoistureDetector Error: "+str(e))
        except:
            utils.log("MoistureDetector: Error")
            print("MoistureDetector: Error")


