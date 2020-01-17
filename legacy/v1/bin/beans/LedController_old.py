#!/usr/bin/python
# IoT Chip project version : 2.0

import os, sys, getopt
# import RadioEmitter as radioEmitter
from datetime import datetime, timedelta
import time, subprocess
import RPi.GPIO as GPIO
import utils

class LedController():
    """Class for LED controller"""

    name = "LedController"
    pin_red = None
    pin_blue = None

    def __init__(self):
        confs = utils.getConfiguration(self.name)
        if confs != None :
            self.pin_red = int(confs['pin_red'])
            self.pin_blue = int(confs['pin_blue'])
            print("LedController initialized - configuration found")
        else:
            newConfs = [('pin_red',None),('pin_blue',None)]
            utils.setConfiguration(self.name,newConfs)
            print("LedController initialized - Warning: new configuration")

    def setOn(self, ledColor):
        self.cleanProcess()
        print("Led "+str(ledColor)+" ON")
        pin = getattr(self,'pin_'+str(ledColor))
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(int(pin), GPIO.OUT)
        #GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        #GPIO.output(self.enable_pin, GPIO.LOW)

    def setOff(self, ledColor):
        self.cleanProcess()
        print("Led "+str(ledColor)+" OFF")
        pin = getattr(self,'pin_'+str(ledColor))
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        #GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.output(int(pin), GPIO.HIGH)
        #GPIO.output(self.enable_pin, GPIO.HIGH)

    def setAllOn(self):
        self.setOn('red')
        self.setOn('blue')

    def setAllOff(self):
        self.setOff('red')
        self.setOff('blue')

    # cleans latest processes
    def cleanProcess(self):
        try:
            pidRedPath = utils.getContextPath()+'/bin/scripts/led/pid_red';
            pidBluePath = utils.getContextPath()+'/bin/scripts/led/pid_blue';
            if os.path.exists(pidRedPath) and os.path.isfile(pidRedPath):
                pidRed = utils.fread(utils.getContextPath()+'/bin/scripts/led/pid_red')
                if pidRed != None:
                    subprocess.call(["sudo","kill",str(pidRed)])
                    print("Process "+str(pidRed)+" killed")
            if os.path.exists(pidBluePath) and os.path.isfile(pidBluePath):
                pidBlue = utils.fread(utils.getContextPath()+'/bin/scripts/led/pid_blue')
                if pidBlue != None:
                    subprocess.call(["sudo","kill",str(pidBlue)])
                    print("Process "+str(pidBlue)+" killed")
        except:
            print("No process found")

    # turn all LEDs on
    def setCycleOn(self):
        self.cleanProcess()
        procB = subprocess.Popen(['nohup','python',utils.getContextPath()+'/bin/scripts/led/on.py',str(self.pin_blue),'&'])
        procR = subprocess.Popen(['nohup','python',utils.getContextPath()+'/bin/scripts/led/on.py',str(self.pin_red),'&'])
        utils.fwrite(utils.getContextPath()+'/bin/scripts/led/pid_red',procR.pid)
        utils.fwrite(utils.getContextPath()+'/bin/scripts/led/pid_blue',procB.pid)
        print("Red pin PID: "+str(procR.pid)+", Blue pin PID: "+str(procB.pid))
        
        print("LedController is now ON")
        return

    # turn all LEDs off
    def setCycleOff(self):
        self.cleanProcess()
        procB = subprocess.Popen(['nohup','python',utils.getContextPath()+'/bin/scripts/led/off.py',str(self.pin_blue),'&'])
        procR = subprocess.Popen(['nohup','python',utils.getContextPath()+'/bin/scripts/led/off.py',str(self.pin_red),'&'])
        utils.fwrite(utils.getContextPath()+'/bin/scripts/led/pid_red',procR.pid)
        utils.fwrite(utils.getContextPath()+'/bin/scripts/led/pid_blue',procB.pid)
        print("Red pin PID: "+str(procR.pid)+", Blue pin PID: "+str(procB.pid))

        print("LedController is now OFF")
        return

    # Warning: DEPRECATED
    # input 0, 1 or 2
    # This method is deprecated due for abandonning RadioEmitter
    def executeWithRadioEmitter(self, data):
        try:
            radioEmitterObj = radioEmitter.RadioEmitter()
            if data and 'spotlight_activity' in data and (data['spotlight_activity'] == "0" or data['spotlight_activity'] == "false" or data['spotlight_activity'].lower() == "off") :
                print("Switching LEDs Off")
                radioEmitterObj.switchPower(0,"off")
            elif data and 'spotlight_activity' in data and (data['spotlight_activity'] == "1" or data['spotlight_activity'] == "true" or data['spotlight_activity'].lower() == "on") :
                if data and 'spotlight_activity_mode' in data and (data['spotlight_activity_mode'] == "1" or data['spotlight_activity_mode'] == "true" or data['spotlight_activity_mode'].lower() == "on") :
                    if data and 'spotlight_starttime_hours' in data and 0 <= int(data['spotlight_starttime_hours'] <= 23) :
                        print "spotlight_starttime_hours..."
                        milliNow = int(time.mktime(datetime.now().timetuple())*1000)
                        timeNow = datetime.now()
                        timeScheduled = timeNow.replace(hour=int(data['spotlight_starttime_hours']), minute=int(data['spotlight_starttime_minutes']))
                        milliScheduled = int(time.mktime(timeScheduled.timetuple())*1000)
                        timeScheduledOff = timeScheduled + timedelta(hours=int(data['spotlight_duration_hours'])) + timedelta(minutes=int(data['spotlight_duration_minutes']))
                        milliScheduledOff = int(time.mktime(timeScheduledOff.timetuple())*1000)
                        print("Now: "+datetime.now().strftime('%Y-%m-%d %H:%M')+" Scheduled ON:"+timeScheduled.strftime('%Y-%m-%d %H:%M')+" Scheduled OFF:"+timeScheduledOff.strftime('%Y-%m-%d %H:%M'))
                        if(milliNow >= milliScheduled and milliNow <= milliScheduledOff):
                            print("Switching LEDs On as scheduled")
                            radioEmitterObj.switchPower(0,"on")
                        else:
                            print("Switching LEDs Off as scheduled")
                            radioEmitterObj.switchPower(0,"off")
                else:
                    print("Switching LEDs On")
                    radioEmitterObj.switchPower(0,"on")
        except Exception,e: 
            print "LedController :"
            print str(e)
        except:
            print "LedController : Unknown Error"

    # Method for stand-alone LEDs controller
    def execute(self, data):
        try:
            ledsDict = { 0: 'red', 1:'blue' }
            for i, j in ledsDict.iteritems():
                if data and 'spotlight_multipin_'+str(i)+'_activity' in data and (data['spotlight_multipin_'+str(i)+'_activity'] == "0" or data['spotlight_multipin_'+str(i)+'_activity'] == "false" or data['spotlight_multipin_'+str(i)+'_activity'].lower() == "off") :
                    print("Switching LEDs Off")
                    self.setOff(str(j))
                elif data and 'spotlight_multipin_'+str(i)+'_activity' in data and (data['spotlight_multipin_'+str(i)+'_activity'] == "1" or data['spotlight_multipin_'+str(i)+'_activity'] == "true" or data['spotlight_multipin_'+str(i)+'_activity'].lower() == "on") :
                    print("Switching LEDs On")
                    self.setOn(str(j))
                    """
                    #if data and 'spotlight_multipin_'+str(i)+'_schedule' in data and (data['spotlight_multipin_'+str(i)+'_schedule'] == "1" or data['spotlight_multipin_'+str(i)+'_schedule'] == "true" or data['spotlight_multipin_'+str(i)+'_schedule'].lower() == "on") :
                    #    if data and 'spotlight_multipin_'+str(i)+'_schedule_starttime_hours' in data and 0 <= int(data['spotlight_multipin_'+str(i)+'_schedule_starttime_hours'] <= 23) :
                    #        print "spotlight schedule..."
                    #        milliNow = int(time.mktime(datetime.now().timetuple())*1000)
                    #        timeNow = datetime.now()
                    #        timeScheduled = timeNow.replace(hour=int(data['spotlight_multipin_'+str(i)+'_schedule_starttime_hours']), minute=int(data['spotlight_multipin_'+str(i)+'_schedule_starttime_minutes']))
                    #        milliScheduled = int(time.mktime(timeScheduled.timetuple())*1000)
                    #        timeScheduledOff = timeScheduled + timedelta(hours=int(data['spotlight_multipin_'+str(i)+'_schedule_starttime_hours'])) + timedelta(minutes=int(data['spotlight_multipin_'+str(i)+'_schedule_starttime_minutes']))
                    #        milliScheduledOff = int(time.mktime(timeScheduledOff.timetuple())*1000)
                    #        print("Now: "+datetime.now().strftime('%Y-%m-%d %H:%M')+" Scheduled ON:"+timeScheduled.strftime('%Y-%m-%d %H:%M')+" Scheduled OFF:"+timeScheduledOff.strftime('%Y-%m-%d %H:%M'))
                    #        if(milliNow >= milliScheduled and milliNow <= milliScheduledOff):
                    #            print("Switching LEDs On as scheduled")
                    #            self.setOn(i)
                    #        else:
                    #            print("Switching LEDs Off as scheduled")
                    #            self.setOff(i)
                    #else:
                    #    print("Switching LEDs On")
                    #    self.setOn(i)
                    """
        except Exception,e: 
            print("LedController : "+str(e))
        except:
            print "LedController : Unknown Error"

    # Main
    def main(argv):
        try:
            opts, args = getopt.getopt(sys.argv[1:],"s:h:",[])
            obj = LedController()
            if len(opts) > 0:
                for x,y in opts:
                    #print(str(x)+" "+str(y))
                    if x == '-s':
                        if str(y) in ['red','blue']:
                            obj.setOn(str(y))
                            print('LedController.main '+str(y)+' On')
                        else:
                            obj.setAllOn()
                            print('LedController.main All On')
                    if x == '-h':
                        if str(y) in ['red','blue']:
                            obj.setOff(str(y))
                            print('LedController.main '+str(y)+' Off')
                        else:
                            obj.setAllOff()
                            print('LedController.main All Off')
            else:
                print 'LedController.main -s[start]|-h[halt] [ledColor]'
        except getopt.GetoptError,e:
            print("LedController.main GetoptError: "+str(e))
        except Exception,ex:
            print("LedController.main Exception: "+str(ex))
        except:
            print("LedController.main unknown error")

if __name__ == "__main__":
    LedController().main()