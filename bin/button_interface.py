# Poweroff Reboot Script
# Author: Chicco Talo
# License: Eden Synthetics
from __future__ import division
import time
import sys
import RPi.GPIO as GPIO
from subprocess import call
import Adafruit_PCA9685
import json
import datetime 
import numpy as np

from beans import ExecutePWM 
from beans import utils
from beans import FrontLED
from beans import GrowLED

frontled = FrontLED.FrontLED()
growled  = GrowLED.GrowLED()
pwm      = ExecutePWM.ExecutePWM()

try:
    confs         = utils.getConfiguration('Button')
    input_channel = int(confs['pin'])
except:
    input_channel = 20
confs     = utils.getConfiguration('PCA_PWM_frequency')
f         = confs['value']

# determine if front LED is available , controllable via PCA or single pin shift register
confs     = utils.getConfiguration('FrontLED')
flag      = confs['channel']


pca = Adafruit_PCA9685.PCA9685()
pca.set_pwm_freq(f)

GPIO.setmode(GPIO.BCM)
GPIO.setup(input_channel, GPIO.IN)
GPIO.add_event_detect(input_channel, GPIO.RISING)






##################################### SUBS ###################################################




def dim_led(duty):
    pwm_data = utils.get_LED_PWM_file()
    growled.set('w',50*duty    ,pwm_data)
    growled.set('b',100*duty   ,pwm_data)
    growled.set('r',400*duty   ,pwm_data)
    growled.set('fr',1000*duty ,pwm_data)

        


def select_behaviour():
    state_array = ['g','','','','']
    frontled.setArray(state_array)
    idx = 0 # start with first LED
    now     = time.time()
    timeout = now + 4
    
    while now < timeout:
        if GPIO.input(input_channel):
            idx = idx +1
            idx = idx%len(state_array)
            timeout = time.time() + 4   # 4 seconds from now
            if idx == 0:
                state_array[4]   = ''
                state_array[idx]   = 'g'
            else:   
                state_array[idx]   = 'g'
                state_array[idx-1] = ''

            frontled.setArray(state_array)
            
            # only for alpha
            pwm.runPwm()
        
        now = time.time()    
        #time.sleep(0.1)
        #wait = wait + 0.1
        print('idx = ' + str(idx))
        time.sleep(0.1)
    return idx

def initialize_LED_array():
    state_array = ['','','','','']
    frontled.setArray(state_array)
    state_array = ['r','o','g','b','v']
    frontled.setArray(state_array,0.2)
    frontled.checkup()
    pwm.runPwm()
    
    
################################################### MAIN #############################################################################    



initialize_LED_array()


while True:
    button_pressed = GPIO.event_detected(input_channel)
    if button_pressed:
        #pwm.register({'master' : 0})
        mode = select_behaviour()
        if mode == 0:
            print('Dimming...')
            #dim_led(1)
        elif mode == 1:
            print('reboot')
            state_array = ['g','','','','']
            frontled.setArray(state_array)
            pwm.runPwm()
            dim_led(1)
            call(["sudo", "reboot"])
        elif mode == 2 :
            print('poweroff')
            state_array = ['','','','','']
            frontled.setArray(state_array)
            pwm.runPwm()
            dim_led(0)
            call(["sudo", "poweroff"])
        elif mode == 3 :
            print('Turn on access point')
            state_array = ['g','','','o','']
            frontled.setArray(state_array)
            #call(["sudo","pyaccesspoint","start", "-c"])
            #call(["sudo", "systemctl", "start", "wifi_page.service"])
            #pwm.runPwm()
            
        elif mode == 4:
            print('reset all')
            state_array = ['g','','','','v']
            frontled.setArray(state_array)
            #pwm.register({'master' : 1})
            initialize_LED_array()
            mode = -1
            #GPIO.remove_event_detect(input_channel)
            #call(["sudo","pyaccesspoint","stop"])
            #call(["sudo", "systemctl", "stop", "wifi_page.service"])
            #continue
    else:
        #print('run schedule')
        #try:
        #    pwm.runPwm()
        #except:
        pass
            #continue 
        
    time.sleep(0.2)

  


        







    
