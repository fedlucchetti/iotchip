#!/usr/bin/python
# IoT Chip project version : 2.0

import sys, getopt
import RPi.GPIO as GPIO
import time, subprocess
import utils

class Relay(object):
    """ Class for Relay, untested, incomplete """

    name = "Relay"
    pin_0 = None
    pin_1 = None

    def __init__(self):
        confs = utils.getConfiguration(self.name)
        if confs != None :
            try:
                self.pin_0 = int(confs['pin_0'])
                self.pin_1 = int(confs['pin_1'])
            except:
                print("Notice: some of the Relay pins are not set")
            print("Relay initialized - configuration found")
        else:
            newConfs = [('pin_0',None),('pin_1',None)]
            utils.setConfiguration(self.name,newConfs)
            print("Relay initialized - Warning: new configuration")

    def setOn(self, relayNumber):
        print("Relay "+str(relayNumber)+" ON")
        pin = getattr(self,'pin_'+str(relayNumber))
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        #GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
        #GPIO.output(self.enable_pin, GPIO.HIGH)

    def setOff(self, relayNumber):
        print("Relay "+str(relayNumber)+" OFF")
        pin = getattr(self,'pin_'+str(relayNumber))
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        #GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        #GPIO.output(self.enable_pin, GPIO.LOW)

    def main(argv):
        try:
            opts, args = getopt.getopt(sys.argv[1:],"s:h:",[])
            obj = Relay()
            if len(opts) > 0:
                for x,y in opts:
                    if x == '-s':
                        obj.setOn(int(y))
                        print('Relay.main '+str(y)+' On')
                    if x == '-h':
                        obj.setOff(int(y))
                        print('Relay.main '+str(y)+' Off')
            else:
                print 'Relay.main -s|-h <relay#>'
        except getopt.GetoptError,e:
            print("Relay.main GetoptError: "+str(e))
        except Exception,ex:
            print("Relay.main Exception: "+str(ex))
        except:
            print("Relay.main unknown error")

if __name__ == "__main__":
    Relay().main()