#!/usr/bin/python
# IoT Chip project version : 3.0

import sys, getopt
from datetime import datetime
import math
import utils

from beans import ExecutePWM
pwm        = ExecutePWM.ExecutePWM()



class GrowLED():
    """Class for GrowLED controller """

    name = "GrowLED"
    channel_r = None
    channel_b = None
    channel_w = None
    channel_f = None

    ex_pwm = None
    
    vegetatifStates = { '0' : { 'lightDuration' : 16, 'mu_r1' : 4.5*60, 'mu_r2' : 11.5*60,  'sigma_r' : 2.5*60, 'mu_b' : 8*60,   'sigma_b' : 3.5*60, 'A_r' : 0.5, 'A_b' : 0.2, 'max_r' : 0.0027, 'max_b' : 0.0027 },
                        '1' : { 'lightDuration' : 18, 'mu_r1' : 6*60,   'mu_r2' : 12*60,    'sigma_r' : 2.5*60, 'mu_b' : 9*60,   'sigma_b' : 3.5*60, 'A_r' : 0.5, 'A_b' : 0.5, 'max_r' : 0.0027, 'max_b' : 0.0027 },
                        '2' : { 'lightDuration' : 18, 'mu_r1' : 6*60,   'mu_r2' : 12*60,    'sigma_r' : 3*60,   'mu_b' : 9*60,   'sigma_b' : 2.5*60, 'A_r' : 0.7, 'A_b' : 1,   'max_r' : 0.0023, 'max_b' : 0.0027 },
                        '3' : { 'lightDuration' : 12, 'mu_r1' : 6*60,   'mu_r2' : 12*60,    'sigma_r' : 3.5*60, 'mu_b' : 6*60,   'sigma_b' : 2.5*60, 'A_r' : 1,   'A_b' : 1,   'max_r' : 0.0020, 'max_b' : 0.0027 } }

    def __init__(self):
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
            

    def set(self, color, duty, old_pwm_data, run = False):
        
        if color=='w' or color=='r':
            duty = int(round(duty))
            channel = getattr(self,'channel_' + color + '1')
            duty_old = old_pwm_data[self.name+"_"+color + '1']["duty"]
            
            if duty_old != duty:
                print('writing duty = ' + str(duty) + 'for color ' + color)
                pwm.soft_start(channel,duty_old,duty)
                utils.register_LED({self.name+"_"+color + '1': {"channel":channel,"duty_old":duty_old,"duty":duty,"flag":1}})
                channel = getattr(self,'channel_' + color + '2')
                duty_old = old_pwm_data[self.name+"_"+color + '2']["duty"]
                pwm.soft_start(channel,duty_old,duty)
                utils.register_LED({self.name+"_"+color + '2': {"channel":channel,"duty_old":duty_old,"duty":duty,"flag":1}})
        elif color=='b' or color=='fr':
            #print("Led "+str(ledNumber)+" set to "+str(duty))
            channel = getattr(self,'channel_'+color)
            duty_old = old_pwm_data[self.name+"_"+color]["duty"]
            if duty_old != duty:
                print('writing duty = ' + str(duty) + 'for color ' + color)
                utils.register_LED({self.name+"_"+color : {"channel":channel,"duty_old":duty_old,"duty":duty,"flag":1}})
                pwm.soft_start(channel,duty_old,duty)



    # Method for stand-alone LEDs controller
    def execute(self, data):
        old_pwm_data = utils.get_LED_PWM_file()
        
        print('ledmode = ' + str(data["payload"]["lights"]["modeAuto"]))
        print('dim     = ' + str(data["payload"]["lights"]["dim"]))
        try:
            led_mode = data["payload"]["lights"]["modeAuto"]
            dim      = data["payload"]["lights"]["dim"]
            print('OK1')
            if  led_mode:
                print("Schedule processing")
                self.scheduleProcessing(data)
                print('duty automatically set')
            else:
                if dim:
                    self.set('w', 50  ,old_pwm_data)
                    self.set('b', 100 ,old_pwm_data)
                    self.set('r', 400 ,old_pwm_data)
                    self.set('fr',1000,old_pwm_data)
                    print("Dimming")
                else:
                    self.set('w', (int(data['payload']['lights']['dutyWhite'] )*4095)/100 ,old_pwm_data)
                    self.set('b', (int(data['payload']['lights']['dutyBlue']  )*4095)/100 ,old_pwm_data)
                    self.set('r', (int(data['payload']['lights']['dutyRed']   )*4095)/100 ,old_pwm_data)
                    self.set('fr',(int(data['payload']['lights']['dutyFarRed'])*4095)/100 ,old_pwm_data)
                    print('duty manually set')
        except Exception,e: 
            print("GrowLED : "+str(e))
        except:
            print "GrowLED : Unknown Error"

    def scheduleProcessing(self,data):
        old_pwm_data = utils.get_LED_PWM_file()
        dutyR = self.dutyColor(data,'r')
        dutyB = self.dutyColor(data,'b')
        print("DutyR: "+str(dutyR)+" DutyB: "+str(dutyB))
        self.set('r',dutyR, old_pwm_data)
        self.set('b',dutyB, old_pwm_data)

    def dutyColor(self,data,color):
        print("- - - Duty_" + color + "- - -")
        led_on_h  = int(data["payload"]["tOnHours"])
        led_on_m  = int(data["payload"]["tOnMinutes"])

        delta_on  = int(self.vegetatifStates[str(data['payload']['growthStage'])]['lightDuration'])*60

        sigma    = float(self.vegetatifStates[str(data['payload']['growthStage'])]['sigma_' + color])
        
        if color == "r" or color =='fr':
            mu1  = float(self.vegetatifStates[str(data['payload']['growthStage'])]['mu_'    + color+'1'])
            mu2  = float(self.vegetatifStates[str(data['payload']['growthStage'])]['mu_'    + color+'2'])
        else:
            mu1      = float(self.vegetatifStates[str(data['payload']['growthStage'])]['mu_'    + color])
            mu2      = mu1
        A        = float(self.vegetatifStates[str(data['payload']['growthStage'])]['A_'     + color])
        maxAmp   = float(self.vegetatifStates[str(data['payload']['growthStage'])]['max_'   + color])

        
        # Process LED schedule
        timeNowMinutes       = datetime.now().hour*60 + datetime.now().minute
        ton                  = int(led_on_h)*60 + int(led_on_m)
        tof                  = ton+delta_on

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

        if t>1439:
            t = t-1439
        else:
            t = t
            
        print('t = ' + str(t))
        print('timeOn = ' + str(ton))
        print('timeOff = ' + str(tof))
        print('timeNowMinutes = ' + str(timeNowMinutes))
        
        # Compute Duty


        if t > 0 and t < delta_on:
            part1 = float(1/math.sqrt(2*math.pi*math.pow(sigma,2)))
            part2 = float(math.exp(-math.pow(((t - mu1)/(math.sqrt(2)*sigma)),2)))
            part3 = float(math.exp(-math.pow(((t - mu2)/(math.sqrt(2)*sigma)),2)))
            duty = A*4095*float((part1 * ( part2 + part3 )) / maxAmp)
        else:
            duty = 0
        
        return int(duty)


    # Main, Do Not Change This Method
    def main(argv):
        try:
            opts, args = getopt.getopt(sys.argv[1:],"s:h:",[])
            obj = GrowLED()
            if len(opts) > 0:
                for x,y in opts:
                    #print(str(x)+" "+str(y))
                    if x == '-s':
                        if int(y) in [0,1]:
                            obj.setOn(y)
                            print('GrowLED.main '+str(y)+' On')
                        else:
                            obj.setAllOn()
                            print('GrowLED.main All On')
                    if x == '-h':
                        if int(y) in [0,1]:
                            obj.setOff(y)
                            print('GrowLED.main '+str(y)+' Off')
                        else:
                            obj.setAllOff()
                            print('GrowLED.main All Off')
                #LedController().ex_pwm.runPwm()
            else:
                print 'GrowLED.main -s[start]|-h[halt] [led#]'
        except getopt.GetoptError,e:
            print("GrowLED.main GetoptError: "+str(e))
        except Exception,ex:
            print("GrowLED.main Exception: "+str(ex))
        except:
            print("GrowLED.main unknown error")

if __name__ == "__main__":
    GrowLED().main()