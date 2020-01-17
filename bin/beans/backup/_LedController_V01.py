#!/usr/bin/python
# IoT Chip project version : 2.0

import os, sys, getopt
import DimmerController as dimmerController
from datetime import datetime, timedelta
import time, subprocess
import math
import utils
import json

class LedController():
    """Class for LED controller """

    name = "LedController"
    channel_0 = None
    channel_1 = None

    dimmer = None
    
    vegetatifStates = { '1' : { 'lightDuration' : 16, 'muR1' : 4.5*60, 'muR2' : 11.5*60,  'sigmaR' : 2.5*60, 'muB' : 8*60,   'sigmaB' : 3.5*60, 'AR' : 0.2, 'AB' : 0.2, 'maxR' : 0.0027, 'maxB' : 0.0027 },
                        '2' : { 'lightDuration' : 18, 'muR1' : 6*60,   'muR2' : 12*60,    'sigmaR' : 2.5*60, 'muB' : 9*60,   'sigmaB' : 3.5*60, 'AR' : 0.2, 'AB' : 0.5, 'maxR' : 0.0027, 'maxB' : 0.0027 },
                        '3' : { 'lightDuration' : 18, 'muR1' : 6*60,   'muR2' : 12*60,    'sigmaR' : 3*60,   'muB' : 9*60,   'sigmaB' : 2.5*60, 'AR' : 0.7, 'AB' : 1,   'maxR' : 0.0023, 'maxB' : 0.0027 },
                        '4' : { 'lightDuration' : 12, 'muR1' : 6*60,   'muR2' : 12*60,    'sigmaR' : 3.5*60, 'muB' : 6*60,   'sigmaB' : 2.5*60, 'AR' : 1,   'AB' : 1,   'maxR' : 0.0020, 'maxB' : 0.0027 } }

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

    # PID LEDs 
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
        self.scheduleProcessing(data)

    def scheduleProcessing(self,data):
        dutyR = self.dutyRed(data)
        dutyB = self.dutyBlue(data)
        print(str(dutyR)+" "+str(dutyB))
        self.set(0,dutyR)
        self.set(1,dutyB)


    def dutyRed(self,data):
        vegetatifStates = { '1' : { 'lightDuration' : 16, 'muR1' : 4.5*60, 'muR2' : 11.5*60,  'sigmaR' : 2.5*60, 'muB' : 8*60,   'sigmaB' : 3.5*60, 'AR' : 0.5, 'AB' : 0.2, 'maxR' : 0.0027, 'maxB' : 0.0027 },
                        '2' : { 'lightDuration' : 18, 'muR1' : 6*60,   'muR2' : 12*60,    'sigmaR' : 2.5*60, 'muB' : 9*60,   'sigmaB' : 3.5*60, 'AR' : 0.5, 'AB' : 0.5, 'maxR' : 0.0027, 'maxB' : 0.0027 },
                        '3' : { 'lightDuration' : 18, 'muR1' : 6*60,   'muR2' : 12*60,    'sigmaR' : 3*60,   'muB' : 9*60,   'sigmaB' : 2.5*60, 'AR' : 0.7, 'AB' : 1,   'maxR' : 0.0023, 'maxB' : 0.0027 },
                        '4' : { 'lightDuration' : 12, 'muR1' : 6*60,   'muR2' : 12*60,    'sigmaR' : 3.5*60, 'muB' : 6*60,   'sigmaB' : 2.5*60, 'AR' : 1,   'AB' : 1,   'maxR' : 0.0020, 'maxB' : 0.0027 } }
        led_on_h  = int(data["spotlight_starttime_hours"])
        led_on_m  = int(data["spotlight_starttime_minutes"])
        veg_stage = int(data["germination_stage"])	
        species   = data["specie_scheme"]
        substrate = data["agriculture_mode"]
        delta_on  = int(vegetatifStates[data['germination_stage']]['lightDuration'])*60

        # Process LED schedule

        timeNow              = datetime.now()
        timeNowMinutes       = datetime.now().hour*60 + datetime.now().minute
        timeScheduled        = timeNow.replace(hour=int(data['spotlight_starttime_hours']), minute=int(data['spotlight_starttime_minutes']))
        timeScheduledMinutes = int(timeScheduled.hour*60 + timeScheduled.minute)
        ton                 =  int(led_on_h)*60 + int(led_on_m)
        tof                 =  ton+delta_on

        if tof > ton:
	        tof = tof-1439
        else:
	        tof = tof


        if ton < tof:
	        t = timeNowMinutes

        elif tof - 1439 < ton:
	        t = timeNowMinutes + 1439 - ton 

        if tof < ton:
                tof = tof+1439
        else:
                tof = tof

        print('timeOn = ' + str(ton))
        print('timeOff = ' + str(tof))
        print('timeNowMinutes = ' + str(timeNowMinutes))
        
        sigmaR = float(vegetatifStates[data['germination_stage']]['sigmaR'])
        muR1   = float(vegetatifStates[data['germination_stage']]['muR1'])
        muR2   = float(vegetatifStates[data['germination_stage']]['muR2'])
        AR     = float(vegetatifStates[data['germination_stage']]['AR'])
        maxR   = float(vegetatifStates[data['germination_stage']]['maxR'])
        
        if t>1439:
	        t = t-1439
        else:
	        t = t
        print('t = ' + str(t))
        #print(delta_on)
        if t > 0 and t < delta_on:
            part1 = float(1/math.sqrt(2*math.pi*math.pow(sigmaR,2)))
            part2 = float(math.exp(-math.pow(((t - muR1)/(math.sqrt(2)*sigmaR)),2)))
            part3 = float(math.exp(-math.pow(((t - muR2)/(math.sqrt(2)*sigmaR)),2)))
            dutyR = AR*4095*float((part1 * ( part2 + part3 )) / maxR)
        else:
	        dutyR = 0
	
	return int(dutyR)

    def dutyBlue(self,data):
        vegetatifStates = { '1' : { 'lightDuration' : 16, 'muR1' : 4.5*60, 'muR2' : 11.5*60,  'sigmaR' : 2.5*60, 'muB' : 8*60,   'sigmaB' : 3.5*60, 'AR' : 0.4, 'AB' : 0.2, 'maxR' : 0.0027, 'maxB' : 0.0027 },
                        '2' : { 'lightDuration' : 18, 'muR1' : 6*60,   'muR2' : 12*60,    'sigmaR' : 2.5*60, 'muB' : 9*60,   'sigmaB' : 3.5*60, 'AR' : 0.5, 'AB' : 0.5, 'maxR' : 0.0027, 'maxB' : 0.0027 },
                        '3' : { 'lightDuration' : 18, 'muR1' : 6*60,   'muR2' : 12*60,    'sigmaR' : 3*60,   'muB' : 9*60,   'sigmaB' : 2.5*60, 'AR' : 0.7, 'AB' : 1,   'maxR' : 0.0023, 'maxB' : 0.0027 },
                        '4' : { 'lightDuration' : 12, 'muR1' : 6*60,   'muR2' : 12*60,    'sigmaR' : 3.5*60, 'muB' : 6*60,   'sigmaB' : 2.5*60, 'AR' : 1,   'AB' : 1,   'maxR' : 0.0020, 'maxB' : 0.0027 } }
        led_on_h  = int(data["spotlight_starttime_hours"])
        led_on_m  = int(data["spotlight_starttime_minutes"])
        veg_stage = int(data["germination_stage"])	
        species   = data["specie_scheme"]
        substrate = data["agriculture_mode"]
        delta_on  = int(vegetatifStates[data['germination_stage']]['lightDuration'])*60

        # Process LED schedule

        timeNow              = datetime.now()
        timeNowMinutes       = datetime.now().hour*60 + datetime.now().minute
        timeScheduled        = timeNow.replace(hour=int(data['spotlight_starttime_hours']), minute=int(data['spotlight_starttime_minutes']))
        timeScheduledMinutes = int(timeScheduled.hour*60 + timeScheduled.minute)
        ton                 =  int(led_on_h)*60 + int(led_on_m)
        tof                 =  ton+delta_on

        if tof > ton:
	        tof = tof-1439
        else:
	        tof = tof


        if ton < tof:
	        t = timeNowMinutes
	        #tof            = delta_on
	        #ton            = 0
        elif tof - 1439 < ton:
	        t = timeNowMinutes + 1439 - ton 
	        #tof            = delta_on
	        #ton            = 0

        if tof < ton:
                tof = tof+1439
        else:
                tof = tof

        print('timeOn = ' + str(ton))
        print('timeOff = ' + str(tof))
        print('timeNowMinutes = ' + str(timeNowMinutes))

        # Compute DutyB

        sigmaB = float(vegetatifStates[data['germination_stage']]['sigmaB']) #float(2.5*60)
        muB    = float(vegetatifStates[data['germination_stage']]['muB']) #float(480)
        maxB   = float(vegetatifStates[data['germination_stage']]['maxB']) #float(0.0027)
        AB     = float(vegetatifStates[data['germination_stage']]['AB'])

        if t>1439:
	        t = t-1439
        else:
	        t = t
        print('t = ' + str(t))
        
        if t > 0 and t < delta_on:
	        part1 = 1/math.sqrt(2*math.pi*math.pow(sigmaB,2))
	        part2 = math.exp(-math.pow(((t - muB)/(math.sqrt(2)*sigmaB)),2))
	        part2 = part2 * 4095
	        dutyB = AB*(part1 * part2) / maxB
	
        else:
	        dutyB = 0
	        

        return int(dutyB)

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
