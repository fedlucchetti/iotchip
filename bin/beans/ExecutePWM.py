#!/usr/bin/python
# IoT Chip project version : 3.0

from __future__ import division
import utils
import json
import Adafruit_PCA9685
import time

class ExecutePWM():
    """description of class ExecutePWM"""

    name = "ExecutePWM"
    pwm = None

    def __init__(self):
        confs     = utils.getConfiguration('PCA_PWM_frequency')
        frequency = confs['value']
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(frequency)
        print("ExecutePWM initialized")

    def getPwm(self):
        return self.pwm

    def soft_start(self,channel,start_duty,stop_duty):
        print('channel ' + str(channel)  + '   start ' + str(start_duty) + '---> stop  ' + str(stop_duty) )
        if start_duty +20 < stop_duty:
            for duty in range(start_duty,stop_duty,20):
                try:
                    self.pwm.set_pwm(channel, 0, duty)
                    #print('duty = ' + str(duty) + 'on channel  ' + str(channel))
                except:
                    print("error start-up")
                time.sleep(0.01)
        elif start_duty-20 > stop_duty:
            for duty in range(start_duty,stop_duty,-20):
                try:
                    self.pwm.set_pwm(channel, 0, duty)
                    #print('duty = ' + str(duty) + 'on channel  ' + str(channel))
                except:
                    print("error step down duty")
                time.sleep(0.01)
        else:
            try:
                #self.pwm.set_pwm(channel, 0, stop_duty)
                #print('duty = ' + str(stop_duty) + 'on channel  ' + str(channel))
                print(' old duty ~ new duty')
            except:
                print("error static duty")
            time.sleep(0.01)


    def register(self,data):
        confPath = utils.getContextPath()+'/conf'
        utils.updateJSONFile(confPath+'/pwm_conf.json',data)

    def runPwm(self): 

        confPath = utils.getContextPath()+'/conf'
        pwm_data = {}
        with open(confPath+'/pwm_conf.json') as data_file:    
            data = json.load(data_file)
                  
        for key, value in data.iteritems():           
            #if (key[:4]=='Grow' or key[:3] == 'FanController' or key[:14] == 'IndicatorPanel') and value["flag"]==1 and value["duty"] >= 0.0 and value["duty"] <=4095.0:
            if (key[:8] == 'FrontLED' ): 
                if(value["flag"]==1):
                    print(key,value)
                    self.pwm.set_pwm(value["channel"], 0, value["duty"])
                    pwm_data.update({key : {"channel":value["channel"],"duty":value["duty"],"flag":0}})
                else:
                    pass
            elif key[:3] == 'Fan':
                if(value["flag"]==1):
                    print(key,value)
                    self.pwm.set_pwm(value["channel"], 0, value["duty"])
                    pwm_data.update({key : {"channel":value["channel"],"duty":value["duty"],"flag":0,"timeout":value["timeout"]}})
                else:
                    pass
                

        self.register(pwm_data)
        
if __name__ == "__main__":
    ExecutePWM().runPwm()        
        