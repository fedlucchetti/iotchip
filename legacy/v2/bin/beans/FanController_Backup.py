#!/usr/bin/python
# IoT Chip project version : 2.0

import sys, getopt
import RPi.GPIO as GPIO
import time, subprocess
import utils

class FanController():
    """Class for Fan controller"""
    # Warning: this Class is incomplete and untested yet

    name = "FanController"
    frequency = 1 # default 
    pin_0 = None # pin number (RPi)
    pin_1 = None # pin number (RPi)
    pin_2 = None # pin number (RPi)
    pin_3 = None # pin number (RPi)
    #enable_pin = 6 # ENABLE PIN is hardware enabled (always ON, cannot mod programatically)

    def __init__(self):
        confs = utils.getConfiguration(self.name)
        if confs != None :
            try:
                self.pin_0 = int(confs['pin_0'])
                self.pin_1 = int(confs['pin_1'])
                self.pin_2 = int(confs['pin_2'])
                self.pin_3 = int(confs['pin_3'])
            except:
                print("Notice: some of the Fan pins are not used")
            print("FanController initialized - configuration found")
        else:
            newConfs = [('pin_0',None),('pin_1',None),('pin_2',None),('pin_3',None)]
            utils.setConfiguration(self.name,newConfs)
            print("FanController initialized - Warning: new configuration")

    def set(self, fanNumber, duty):
        print("Fan "+str(fanNumber)+" set")
        pin = getattr(self,'pin_'+str(fanNumber))
        self.pwm.set_pwm(pin, 0, duty)

    def setOn(self, fanNumber):
        print("Fan "+str(fanNumber)+" ON")
        pin = getattr(self,'pin_'+str(fanNumber))
        self.pwm.set_pwm(pin, 0, 4095)

    def setOff(self, fanNumber):
        print("Fan "+str(fanNumber)+" OFF")
        pin = getattr(self,'pin_'+str(fanNumber))
        self.pwm.set_pwm(pin, 0, 0)

    def setAllOn(self):
        self.setOn(0)
        self.setOn(1)

    def setAllOff(self):
        self.setOff(0)
        self.setOff(1)

    # cleans latest processes
    def cleanProcess(self,fanNumber):
        try:
            pid = utils.fread(utils.getContextPath()+'/bin/scripts/fan/pid_'+str(fanNumber))
            subprocess.call(["sudo","kill",str(pid)])
            print("Process "+str(pid)+" killed")
        except:
            print("No process found")

    def setCycleOn(self, fanNumber):
        self.cleanProcess(fanNumber)
        pin = getattr(self, 'pin_'+str(fanNumber))
        proc = subprocess.Popen(['nohup','python',utils.getContextPath()+'/bin/scripts/fan/on.py',str(pin),'&'])
        utils.fwrite(utils.getContextPath()+'/bin/scripts/fan/pid_'+str(fanNumber),proc.pid)
        print("Fan PID: "+str(proc.pid))
        print("FanController is now ON")
        return

    def setCycleOff(self, fanNumber):
        self.cleanProcess(fanNumber)
        pin = getattr(self, 'pin_'+str(fanNumber))
        proc = subprocess.Popen(['nohup','python',utils.getContextPath()+'/bin/scripts/fan/off.py',str(pin),'&'])
        utils.fwrite(utils.getContextPath()+'/bin/scripts/fan/pid_'+str(fanNumber),proc.pid)
        print("Fan PID: "+str(proc.pid))
        print("FanController is now OFF")
        return

    # Method for stand-alone Fan controller, not tested
    def execute(self, data):
        try:
            for i in [0,1,2,3]:
                if data and 'fan_multipin_'+str(i)+'_activity' in data and (data['fan_multipin_'+str(i)+'_activity'] == "0" or data['fan_multipin_'+str(i)+'_activity'] == "false" or data['fan_multipin_'+str(i)+'_activity'].lower() == "off") :
                    print("Switching Fan "+str(i)+" Off")
                    self.setOff(i)
                else:
                    print("Switching Fan "+str(i)+" On")
                    self.setOn(i)
        except Exception,e: 
            print("FanController : "+str(e))
        except:
            print "FanController : Unknown Error"

    def main(argv):
        try:
            opts, args = getopt.getopt(sys.argv[1:],"s:h:",[])
            obj = FanController()
            if len(opts) > 0:
                for x,y in opts:
                    #print(str(x)+" "+str(y))
                    if x == '-s':
                        if int(y) in [0,1,2,3]:
                            obj.setOn(int(y))
                        else :
                            obj.setOn(0)
                            obj.setOn(1)
                            obj.setOn(2)
                        print('FanController.main '+str(y)+' On')
                        if len(args) > 0 and args[0] != None:
                            # speed not integrated
                            obj.setOn(int(y))
                            print('FanController.main '+str(y)+' On, speed='+str(args[0]))
                    if x == '-h':
                        if int(y) in [0,1,2,3]:
                            obj.setOff(int(y))
                        else :
                            obj.setOff(0)
                            obj.setOff(1)
                            obj.setOff(2)
                        print('FanController.main '+str(y)+' Off')
            else:
                print 'FanController.main -s|-h <fan#> [<speed>]'
        except getopt.GetoptError,e:
            print("FanController.main GetoptError: "+str(e))
        except Exception,ex:
            print("FanController.main Exception: "+str(ex))
        except:
            print("FanController.main unknown error")

if __name__ == "__main__":
    FanController().main()