#!/usr/bin/python
# IoT Chip project version : 2.0

import os, sys, getopt
import DimmerController as dimmerController
from datetime import datetime, timedelta
import time, subprocess
import math
import utils

class LedController():
    """Class for LED controller """

    name = "LedController"
    channel_0 = None
    channel_1 = None

    dimmer = None
    
    vegetatifStates = { '1' : { 'lightDuration' : 0, 'muR1' : 4*60, 'muR2' : 12*60, 'sigmaR' : 2.5*60, 'muB' : 8*60, 'sigmaB' : 3.5*60, 'AR' : 0, 'AB' : 0, 'maxR' : 1, 'maxB' : 1 }, 
                        '2' : { 'lightDuration' : 16, 'muR1' : 4*60, 'muR2' : 12*60, 'sigmaR' : 2.5*60, 'muB' : 8*60, 'sigmaB' : 3.5*60, 'AR' : 0.2, 'AB' : 0.5, 'maxR' : 0.0027, 'maxB' : 0.0027 }, 
                        '3' : { 'lightDuration' : 16, 'muR1' : 4*60, 'muR2' : 12*60, 'sigmaR' : 2*60, 'muB' : 8*60, 'sigmaB' : 2.5*60, 'AR' : 0.8, 'AB' : 1, 'maxR' : 0.0032, 'maxB' : 0.0027 },
                        '4' : { 'lightDuration' : 12, 'muR1' : 5.5*60, 'muR2' : 10.5*60, 'sigmaR' : 2*60, 'muB' : 8*60, 'sigmaB' : 2.5*60, 'AR' : 1, 'AB' : 0.5, 'maxR' : 0.0035, 'maxB' : 0.00027 } }

    def __init__(self):
        self.dimmer = dimmerController.DimmerController()
        confs = utils.getConfiguration(self.name)
        if confs != None :
            self.channel_0 = int(confs['channel_0'])
            self.channel_1 = int(confs['channel_1'])
            print("LedController initialized - configuration found")
        else:
            newConfs = [('channel_0',None),('channel_1',None)]
            utils.setConfiguration(self.name,newConfs)
            print("LedController initialized - Warning: new configuration")

    def setOn(self, ledNumber):
        print("Led "+str(ledNumber)+" ON")
        channel = getattr(self,'channel_'+str(ledNumber))
        self.dimmer.register({self.name+"_"+str(channel) : {"channel":channel,"value":4095}})
        #self.pwm.set_pwm(channel, 0, 4095)

    def setOff(self, ledNumber):
        print("Led "+str(ledNumber)+" OFF")
        channel = getattr(self,'channel_'+str(ledNumber))
        self.dimmer.register({self.name+"_"+str(channel) : {"channel":channel,"value":0}})
        #self.pwm.set_pwm(channel, 0, 0)

    def set(self, ledNumber, duty):
        print("Led "+str(ledNumber)+" set")
        channel = getattr(self,'channel_'+str(ledNumber))
        self.dimmer.register({self.name+"_"+str(channel) : {"channel":channel,"value":duty}})
        #self.pwm.set_pwm(channel, 0, duty)

    def setAllOn(self):
        self.setOn(0)
        self.setOn(1)

    def setAllOff(self):
        self.setOff(0)
        self.setOff(1)

    # Cycle leds
    def setCycle(self,dutyR,dutyB):
        self.cleanProcess()
        procR = subprocess.Popen(['nohup','python',utils.getContextPath()+'/bin/scripts/led/on.py',str(self.channel_0),str(dutyR),'&'])
        procB = subprocess.Popen(['nohup','python',utils.getContextPath()+'/bin/scripts/led/on.py',str(self.channel_1),str(dutyB),'&'])
        utils.fwrite(utils.getContextPath()+'/bin/scripts/led/pid_0',procR.pid)
        utils.fwrite(utils.getContextPath()+'/bin/scripts/led/pid_1',procB.pid)
        print("Red channel PID: "+str(procR.pid)+", Blue channel PID: "+str(procB.pid))
        
        print("LedController cycle running")
        return

    # Method for stand-alone LEDs controller
    def execute(self, data):
        try:
            if data and 'spotlight_activity' in data and (data['spotlight_activity'] == "0" or data['spotlight_activity'] == "false" or data['spotlight_activity'].lower() == "off") :
                print("Switching LEDs Off")
                #self.setCycle(0,0)
                self.setAllOff()
            elif data and 'spotlight_activity' in data and (data['spotlight_activity'] == "1" or data['spotlight_activity'] == "true" or data['spotlight_activity'].lower() == "on") :
                if 'spotlight_mode' in data and (data['spotlight_mode'] == "manual") :
                    self.set(0,(int(data['spotlight_intensity_1'])*4095)/100)
                    self.set(1,(int(data['spotlight_intensity_2'])*4095)/100)
                else:
                    print("Schedule for LED started")
                    self.scheduleProcessing(data)
        except Exception,e: 
            print("LedController : "+str(e))
        except:
            print "LedController : Unknown Error"

    def scheduleProcessing(self,data):
        timeNow = datetime.now()
        #timeNow = timeNow.replace(day=7, hour=1, minute=41)
        timeScheduled = timeNow.replace(hour=int(data['spotlight_starttime_hours']), minute=int(data['spotlight_starttime_minutes']))
        timeScheduledOff = timeScheduled + timedelta(hours=self.vegetatifStates[data['germination_stage']]['lightDuration']) + timedelta(minutes=00)
        # duration default 16
        print(str(timeNow.time())+" \n"+str(timeScheduled.time())+" \n"+str(timeScheduledOff.time()))
        if timeScheduled.time() < timeScheduledOff.time() : 
            if timeNow.time() >= timeScheduled.time() and timeNow.time() <= timeScheduledOff.time() :
                print("Now On 1")
                dutyR = self.dutyRed(data)
                dutyB = self.dutyBlue(data)
                #self.setCycle(dutyR,dutyB)
                print(str(dutyR)+" "+str(dutyB))
                self.set(0,dutyR)
                self.set(1,dutyB)
            else : 
                print("Now Off 1")
                #self.setCycle(0,0)
                self.setAllOff()
        else :
            if timeNow.time() >= timeScheduled.time() or timeNow.time() <= timeScheduledOff.time() :
                print("Now On 2")
                dutyR = self.dutyRed(data)
                dutyB = self.dutyBlue(data)
                #self.setCycle(dutyR,dutyB)
                print(str(dutyR)+" "+str(dutyB))
                self.set(0,dutyR)
                self.set(1,dutyB)
            else : 
                print("Now Off 2")
                #self.setCycle(0,0)
                self.setAllOff()

    def dutyRed(self,data):
        timeNow = datetime.now()
        timeNowMinutes = datetime.now().hour*60 + datetime.now().minute
        print("timeNowMinutes: "+str(timeNowMinutes))
        timeScheduled = timeNow.replace(hour=int(data['spotlight_starttime_hours']), minute=int(data['spotlight_starttime_minutes']))
        timeScheduledMinutes = timeScheduled.hour*60 + timeScheduled.minute
        print("timeScheduledMinutes: "+str(timeScheduledMinutes))
        timeDiff = timeNowMinutes - timeScheduledMinutes
        print("timeDiff: "+str(timeDiff))
        sigmaR = float(self.vegetatifStates[data['germination_stage']]['sigmaR'])
        muR1 = float(self.vegetatifStates[data['germination_stage']]['muR1'])
        muR2 = float(self.vegetatifStates[data['germination_stage']]['muR2'])
        AR = float(self.vegetatifStates[data['germination_stage']]['AR'])
        maxR = float(self.vegetatifStates[data['germination_stage']]['maxR'])
        part1 = 1/math.sqrt(2*math.pi*math.pow(sigmaR,2))
        #print(part1)
        part2 = math.exp(-math.pow(((timeDiff - muR1)/(math.sqrt(2)*sigmaR)),2))
        part2 = part2 * 100
        #print(part2)
        part3 = math.exp(-math.pow(((timeDiff - muR2)/(math.sqrt(2)*sigmaR)),2))
        part3 = part3 * 100
        #print(part3)
        dutyR = (part1 * ( part2 + part3 )) / maxR
        print("dutyCycle Red: "+str(int(dutyR*AR)))
        return int(dutyR*AR)

    def dutyBlue(self,data):
        timeNow = datetime.now()
        timeNowMinutes = datetime.now().hour*60 + datetime.now().minute
        print("timeNowMinutes: "+str(timeNowMinutes))
        timeScheduled = timeNow.replace(hour=int(data['spotlight_starttime_hours']), minute=int(data['spotlight_starttime_minutes']))
        timeScheduledMinutes = timeScheduled.hour*60 + timeScheduled.minute
        print("timeScheduledMinutes: "+str(timeScheduledMinutes))
        timeDiff = timeNowMinutes - timeScheduledMinutes
        print("timeDiff: "+str(timeDiff))
        sigmaB = float(self.vegetatifStates[data['germination_stage']]['sigmaB']) #float(2.5*60)
        muB = float(self.vegetatifStates[data['germination_stage']]['muB']) #float(480)
        maxB = float(self.vegetatifStates[data['germination_stage']]['maxB']) #float(0.0027)
        AB = float(self.vegetatifStates[data['germination_stage']]['AB'])
        part1 = 1/math.sqrt(2*math.pi*math.pow(sigmaB,2))
        #print(part1)
        part2 = math.exp(-math.pow(((timeDiff - muB)/(math.sqrt(2)*sigmaB)),2))
        part2 = part2 * 100
        #print(part2)
        dutyB = (part1 * part2) / maxB
        print("dutyCycle Blue: "+str(int(dutyB*AB)))
        return int(dutyB*AB)

    # Main
    def main(argv):
        try:
            opts, args = getopt.getopt(sys.argv[1:],"s:h:",[])
            obj = LedController()
            if len(opts) > 0:
                for x,y in opts:
                    #print(str(x)+" "+str(y))
                    if x == '-s':
                        if int(y) in [0,1]:
                            obj.setOn(y)
                            print('LedController.main '+str(y)+' On')
                        else:
                            obj.setAllOn()
                            print('LedController.main All On')
                    if x == '-h':
                        if int(y) in [0,1]:
                            obj.setOff(y)
                            print('LedController.main '+str(y)+' Off')
                        else:
                            obj.setAllOff()
                            print('LedController.main All Off')
                LedController().dimmer.runPwm()
            else:
                print 'LedController.main -s[start]|-h[halt] [led#]'
        except getopt.GetoptError,e:
            print("LedController.main GetoptError: "+str(e))
        except Exception,ex:
            print("LedController.main Exception: "+str(ex))
        except:
            print("LedController.main unknown error")

if __name__ == "__main__":
    LedController().main()