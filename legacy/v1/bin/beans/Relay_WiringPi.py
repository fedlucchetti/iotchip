#!/usr/bin/python
# IoT Chip project version : 1.0 mod (renamed class)

import os
import subprocess
import sys
import getopt
import wiringpi2

class Relay_WiringPi(object):
    # Class for Relay with WiringPi

    name = "Relay_WiringPi"
    _relayAIO = 1
    _relayBIO = 3

    def __init__(self):
        wiringpi2.wiringPiSetup()
        wiringpi2.pinMode(self._relayAIO, 1)
        wiringpi2.pinMode(self._relayBIO, 1)
        print("Relay Initialized")

    def _relayOn(self, pin):
        print("Relay_WiringPi "+str(pin)+" On")
        if pin == self._relayAIO:
            wiringpi2.digitalWrite(self._relayAIO, 1)
        elif pin == self._relayBIO:
            wiringpi2.digitalWrite(self._relayBIO, 1)
            
    def _relayOff(self, pin):
        print("Relay_WiringPi "+str(pin)+" Off")
        if pin == self._relayAIO:
            wiringpi2.digitalWrite(self._relayAIO, 0)
        elif pin == self._relayBIO:
            wiringpi2.digitalWrite(self._relayBIO, 0)

    # input 5 or 6 / 1 or 3 / 24 or 25
    def switchPower(self, input, onOff):
        print("switchPower: "+str(input)+" "+str(onOff)) 
        if onOff == 0 :
            self._relayOff(int(input))
        else :
            self._relayOn(int(input))

    def run(argv):
        try:
            opts, args = getopt.getopt(sys.argv[1:],"0:1:on:off",[])
        except getopt.GetoptError,e:
            print 'Relay_WiringPi: main.py 1|3 on|off'
            #sys.exit(2)
        #for arg in args:
        if len(args) > 0:
            relayObj = Relay_WiringPi()
            if args[0] not in ("1","3") or args[1] not in ("on","0","On","ON","off","1","OFF","Off") :
                print 'Relay_WiringPi takes 2 arguments: 24|25 as target and on|1|ON|On OR off|0|OFF|Off as action'
                #sys.exit()
            elif args[0] in ("1","3") and args[1] in ("on","1","On","ON"):
                print 'Relay_WiringPi main.py on'
                relayObj.switchPower(args[0],1)
            elif args[0] in ("1","3") and args[1] in ("off","0","OFF","Off"):
                print 'Relay_WiringPi main.py off'
                relayObj.switchPower(args[0],0)
        else:
            print 'Relay_WiringPi: main.py "1","3" on|off'

if __name__ == "__main__":
    Relay_WiringPi().run()