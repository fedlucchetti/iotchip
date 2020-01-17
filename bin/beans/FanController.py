#!/usr/bin/python
# IoT Chip project version : 3.0

import ExecutePWM as pwmController
import sys, getopt
import utils
import time
import json

class FanController():
    """Class for Fan controller"""

    name = "FanController"
    channel_front = None # channel number 
    channel_back = None # channel number 
    channel_led = None # channel number 
    fan_on_timeout_min  = None 
    fan_off_timeout_min = None  
    dimmer = None

    def __init__(self):
        self.ex_pwm = pwmController.ExecutePWM()
        confs = utils.getConfiguration(self.name)
        if confs != None :
            try:
                self.channel_front         = int(confs['channel_front'])
                self.channel_back          = int(confs['channel_back'])
                self.channel_led           = int(confs['channel_led'])
                self.fan_on_timeout_min    = float(confs['fan_on_timeout_min'])
                self.fan_off_timeout_min   = float(confs['fan_off_timeout_min'])
                
            except:
                print("Notice: some of the Fan channels are not used")
            print("FanController initialized - configuration found")
        else:
            newConfs = [('channel_front',None),('channel_back',None),('channel_led',None),('fan_on_timeout_min',1),('fan_off_timeout_min',5)]
            utils.setConfiguration(self.name,newConfs)
            print("Fan Object initialized - Warning: new configuration")

    def set(self, fan, duty):
        print("Fan "+str(fan)+" set")
        channel = getattr(self,'channel_'+str(fan))
        self.ex_pwm.register({self.name+"_"+str(fan) : {"channel":channel,"duty":duty,"flag":1}})
        #self.pwm.set_pwm(channel, 0, duty)

    def setOn(self, fan):
        print("Fan "+str(fan)+" ON")
        channel = getattr(self,'channel_'+str(fan))
        self.ex_pwm.register({self.name+"_"+str(fan) : {"channel":channel,"duty":4095,"flag":1,"timeout":round(time.time())+60.0*self.fan_on_timeout_min}})
                
                
    def setOff(self, fan):
        print("Fan "+str(fan)+" OFF")
        channel = getattr(self,'channel_'+str(fan))
        self.ex_pwm.register({self.name+"_"+str(fan) : {"channel":channel,"duty":0,"flag":1,"timeout":round(time.time())+60.0*self.fan_off_timeout_min}})
        #self.pwm.set_pwm(channel, 0, 0)

    def setAllOn(self):
        print('all fans on')
        self.setOn('front')
        self.setOn('back')
        self.setOn('led')

    def setAllOff(self):
        print('all fans off')
        self.setOff('front')
        self.setOff('back')
        self.setOff('led')

    # Method for stand-alone Fan controller, not tested
    def execute(self):
        s = 0
        confPath = utils.getContextPath()+'/conf'
        with open(confPath+'/growLED_pwm_conf.json') as data_file:    
            pwmdata = json.load(data_file)
        
        for key, value in pwmdata.iteritems():
            if (key[:7] == 'GrowLED'):
                s += value["duty"]
        
        s = float(s)/4095.0*100.0/6.0        
        print('current LED output',s)
        if s<10.0:
            self.setAllOff()
        elif s> 10.0 and s<80.0:   
            print('case 2')
            with open(confPath+'/pwm_conf.json') as data_file:    
                pwmdata = json.load(data_file)
            for key, value in pwmdata.iteritems():
                if key[:13]== 'FanController':
                    if value["duty"] > 4000.0 :
                        print('timeout=','value["timeout"]')
                        if value["timeout"] <  time.time():
                            self.setOff('front')
                            self.setOff('back')
                            self.setOff('led')
                        else:
                            print('still on, wait = ' + str(value["timeout"] -  time.time()))
                            pass
                    else:
                        if value["timeout"] <  time.time():
                            self.setOn('front')
                            self.setOn('back')
                            self.setOn('led')
                        else:
                            print('still off, wait = ' + str(value["timeout"] -  time.time()))
                            pass
        else:
            self.setOn('led')

if __name__ == "__main__":
    FanController().execute()