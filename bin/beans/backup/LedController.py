#!/usr/bin/python
# IoT Chip project version : 3.0

import os, sys, getopt
import ExecutePWM as pwmController
from datetime import datetime, timedelta
import time, subprocess
import math
import utils

class GrowLED():
    """Class for LED controller """

    name = "GrowLED"
    channel_r = None
    channel_b = None
    channel_w = None
    channel_f = None

    ex_pwm = None
    
    vegetatifStates = { '1' : { 'lightDuration' : 16, 'muR1' : 4.5*60, 'muR2' : 11.5*60,  'sigmaR' : 2.5*60, 'muB' : 8*60,   'sigmaB' : 3.5*60, 'AR' : 0.5, 'AB' : 0.2, 'maxR' : 0.0027, 'maxB' : 0.0027 },
                        '2' : { 'lightDuration' : 18, 'muR1' : 6*60,   'muR2' : 12*60,    'sigmaR' : 2.5*60, 'muB' : 9*60,   'sigmaB' : 3.5*60, 'AR' : 0.5, 'AB' : 0.5, 'maxR' : 0.0027, 'maxB' : 0.0027 },
                        '3' : { 'lightDuration' : 18, 'muR1' : 6*60,   'muR2' : 12*60,    'sigmaR' : 3*60,   'muB' : 9*60,   'sigmaB' : 2.5*60, 'AR' : 0.7, 'AB' : 1,   'maxR' : 0.0023, 'maxB' : 0.0027 },
                        '4' : { 'lightDuration' : 12, 'muR1' : 6*60,   'muR2' : 12*60,    'sigmaR' : 3.5*60, 'muB' : 6*60,   'sigmaB' : 2.5*60, 'AR' : 1,   'AB' : 1,   'maxR' : 0.0020, 'maxB' : 0.0027 } }

    def __init__(self):
        self.ex_pwm = pwmController.ExecutePWM()
        confs = utils.getConfiguration(self.name)
        if confs != None :
            self.channel_w1 = int(confs['channel_w1'])
            self.channel_w2 = int(confs['channel_w2'])
            self.channel_b  = int(confs['channel_b'])
            self.channel_r1 = int(confs['channel_r1'])
            self.channel_r2 = int(confs['channel_r2'])
            self.channel_fr = int(confs['channel_fr'])
            print("LedController initialized - configuration found")
        else:
            newConfs = [('channel_r1',None),('channel_r2',None),('channel_b',None),('channel_w1',None),('channel_w2',None),('channel_fr',None)]
            utils.setConfiguration(self.name,newConfs)
            print("LedController initialized - Warning: new configuration")



    def set(self, color, duty):
        if color=='w' or color=='r':
            duty = int(round(duty/2))
            channel = getattr(self,'channel_' + color + '1')
            self.ex_pwm.register({self.name+"_"+color : {"channel":channel,"duty":duty,"flag":1}})
            channel = getattr(self,'channel_' + color + '2')
            self.ex_pwm.register({self.name+"_"+color : {"channel":channel,"duty":duty,"flag":1}})
        elif color=='b' or color=='fr':
            #print("Led "+str(ledNumber)+" set to "+str(duty))
            channel = getattr(self,'channel_'+color)
            self.ex_pwm.register({self.name+"_"+color : {"channel":channel,"duty":duty,"flag":1}})




    # Method for stand-alone LEDs controller
    def execute(self, data):
        print('ledmode = ' + str(data["payload"]["lights"]["modeAuto"]))
        print('dim     = ' + str(data["payload"]["lights"]["dim"]))
        try:
            led_mode = data["payload"]["lights"]["modeAuto"]
            dim      = data["payload"]["lights"]["dim"]
            print('OK1')
            if  led_mode:
                self.scheduleProcessing(data)
                print('duty automatically set')
            else:
                if dim:
                    self.set('w',50)
                    self.set('b',100)
                    self.set('r',400)
                    self.set('f',1000)
                    print("Dimming")
                else:
                    self.set('w',(int(data['payload']['lights']['dutyWhite'])*4095)/100)
                    self.set('b',(int(data['payload']['lights']['dutyBlue'])*4095)/100)
                    self.set('r',(int(data['payload']['lights']['dutyRed'])*4095)/100)
                    self.set('f',(int(data['payload']['lights']['dutyFarRed'])*4095)/100)
                    print('duty manually set')
        except Exception,e: 
            print("LedController : "+str(e))
        except:
            print "LedController : Unknown Error"

    def scheduleProcessing(self,data):
        dutyR = self.dutyRed(data)
        dutyB = self.dutyBlue(data)
        print("DutyR: "+str(dutyR)+" DutyB: "+str(dutyB))
        self.set('r',dutyR)
        self.set('b',dutyB)

    def dutyRed(self,data):
        print("- - - Duty Red - - -")
        led_on_h  = int(data["spotlight_starttime_hours"])
        led_on_m  = int(data["spotlight_starttime_minutes"])
        veg_stage = int(data["germination_stage"])	
        species   = data["specie_scheme"]
        substrate = data["agriculture_mode"]
        delta_on  = int(self.vegetatifStates[data['germination_stage']]['lightDuration'])*60

        # Process LED schedule
        timeNow              = datetime.now()
        timeNowMinutes       = datetime.now().hour*60 + datetime.now().minute
        timeScheduled        = timeNow.replace(hour=int(data['spotlight_starttime_hours']), minute=int(data['spotlight_starttime_minutes']))
        timeScheduledMinutes = int(timeScheduled.hour*60 + timeScheduled.minute)
        ton                  = int(led_on_h)*60 + int(led_on_m)
        tof                  = ton+delta_on

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
        
        # Compute DutyR
        sigmaR = float(self.vegetatifStates[data['germination_stage']]['sigmaR'])
        muR1   = float(self.vegetatifStates[data['germination_stage']]['muR1'])
        muR2   = float(self.vegetatifStates[data['germination_stage']]['muR2'])
        AR     = float(self.vegetatifStates[data['germination_stage']]['AR'])
        maxR   = float(self.vegetatifStates[data['germination_stage']]['maxR'])
        
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
        print("- - - Duty Blue - - -")
        led_on_h  = int(data["spotlight_starttime_hours"])
        led_on_m  = int(data["spotlight_starttime_minutes"])
        veg_stage = int(data["germination_stage"])	
        species   = data["specie_scheme"]
        substrate = data["agriculture_mode"]
        delta_on  = int(self.vegetatifStates[data['germination_stage']]['lightDuration'])*60

        # Process LED schedule
        timeNow              = datetime.now()
        timeNowMinutes       = datetime.now().hour*60 + datetime.now().minute
        timeScheduled        = timeNow.replace(hour=int(data['spotlight_starttime_hours']), minute=int(data['spotlight_starttime_minutes']))
        timeScheduledMinutes = int(timeScheduled.hour*60 + timeScheduled.minute)
        ton                  = int(led_on_h)*60 + int(led_on_m)
        tof                  = ton+delta_on

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
        sigmaB = float(self.vegetatifStates[data['germination_stage']]['sigmaB']) #float(2.5*60)
        muB    = float(self.vegetatifStates[data['germination_stage']]['muB']) #float(480)
        maxB   = float(self.vegetatifStates[data['germination_stage']]['maxB']) #float(0.0027)
        AB     = float(self.vegetatifStates[data['germination_stage']]['AB'])

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

    # Main, Do Not Change This Method
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
                LedController().ex_pwm.runPwm()
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