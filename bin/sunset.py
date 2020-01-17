from __future__ import division
import time
import sys
import Adafruit_PCA9685
import RPi.GPIO as GPIO


from beans import utils





#confs      = utils.getConfiguration('PCA_PWM_enable')
#pin = int(confs['pin'])
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(pin, GPIO.OUT)
#GPIO.output(pin,0)


pwmfan = 0
wait = 0.02
max = 800

chFanL = 9
chFan1 = 10
chFan2 = 11


confs      = utils.getConfiguration('GrowLED')
channel_w1 = int(confs['channel_w1'])
channel_w2 = int(confs['channel_w2'])
channel_b  = int(confs['channel_b'])
channel_r1 = int(confs['channel_r1'])
channel_r2 = int(confs['channel_r2'])
channel_fr = int(confs['channel_fr'])

confs      = utils.getConfiguration('Fan_Right')
channel_fan_led = int(confs['channel']) 
confs      = utils.getConfiguration('Fan_Left')
channel_fan_L   = int(confs['channel'])
confs      = utils.getConfiguration('Fan_LED')
channel_fan_R   = int(confs['channel']) 
print("LedController initialized - configuration found")

confs      = utils.getConfiguration('PCA_PWM_frequency')
f = float(confs['value'])
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(f)


## init all to 0

pwm.set_pwm(channel_w1  , 0, 0)	
pwm.set_pwm(channel_w2  , 0, 0)	
pwm.set_pwm(channel_b   , 0, 0)	
pwm.set_pwm(channel_r1  , 0, 0)	
pwm.set_pwm(channel_r1  , 0, 0)	
pwm.set_pwm(channel_fr  , 0, 0)	


pwm.set_pwm(channel_fan_led  , 0, 0)	
pwm.set_pwm(channel_fan_L  , 0, 0)	
pwm.set_pwm(channel_fan_R  , 0, 0)	
        
#pwm.set_all_pwm(0, 0)	


while True:
    for dc in range(0, max, 10):
        pwm.set_pwm(channel_fan_led  , 0, 4095)	
        pwm.set_pwm(channel_fan_L  , 0, 4095)	
        pwm.set_pwm(channel_fan_R  , 0, 4095)	
        
        pwm.set_pwm(channel_w1  , 0, dc)	
        time.sleep(wait)
        
    
    for dc in range(max, 0, -10):
        pwm.set_pwm(channel_fan_led  , 0, 4095)	
        pwm.set_pwm(channel_fan_L  , 0, 0)	
        pwm.set_pwm(channel_fan_R  , 0, 0)	
        
        pwm.set_pwm(channel_w1, 0, dc)
        pwm.set_pwm(channel_w2, 0, max-dc)	
        time.sleep(wait)
    
    for dc in range(max, 0, -10):
        pwm.set_pwm(channel_fan_led  , 0, 0)	
        pwm.set_pwm(channel_fan_L  , 0, 4095)	
        pwm.set_pwm(channel_fan_R  , 0, 0)	
        
        pwm.set_pwm(channel_w2, 0, dc)
        pwm.set_pwm(channel_b, 0, max-dc)	
        time.sleep(wait)

    for dc in range(max, 0, -10):
        pwm.set_pwm(channel_fan_led  , 0, 0)	
        pwm.set_pwm(channel_fan_L  , 0, 0)	
        pwm.set_pwm(channel_fan_R  , 0, 4095)	
                
        pwm.set_pwm(channel_b, 0, dc)
        pwm.set_pwm(channel_r1, 0, max-dc)	
        time.sleep(wait)

    for dc in range(max, 0, -10):
        pwm.set_pwm(channel_fan_led  , 0, 4095)	
        pwm.set_pwm(channel_fan_L  , 0, 0)	
        pwm.set_pwm(channel_fan_R  , 0, 0)	
        
        pwm.set_pwm(channel_r1, 0, dc)
        pwm.set_pwm(channel_r2, 0, max-dc)	
        time.sleep(wait)
    
    for dc in range(max, 0, -10):
        pwm.set_pwm(channel_fan_led  , 0, 0)	
        pwm.set_pwm(channel_fan_L  , 0, 4095)	
        pwm.set_pwm(channel_fan_R  , 0, 0)	
        
        pwm.set_pwm(channel_r2, 0, dc)
        pwm.set_pwm(channel_fr, 0, max-dc)	
        time.sleep(wait)

    for dc in range(max, 0, -10):
        pwm.set_pwm(channel_fan_led  , 0, 0)	
        pwm.set_pwm(channel_fan_L  , 0, 0)	
        pwm.set_pwm(channel_fan_R  , 0, 4095)	
        
        pwm.set_pwm(channel_fr, 0, dc)
        time.sleep(wait)

if __name__ == "__main__":
    sunset().main()