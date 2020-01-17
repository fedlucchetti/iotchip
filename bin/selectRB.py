# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time
import sys
# Import the PCA9685 module.
import Adafruit_PCA9685

wait = 0.01
max = 4000
chR = 6
chB = 7
chFanL = 9
chFan1 = 11
chFan2 = 11

# initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()
f = 1000
pwm.set_pwm_freq(f)

dutyR = int(sys.argv[1])
dutyB = int(sys.argv[2])


pwm.set_pwm(chB  , 0, dutyB)
pwm.set_pwm(chR  , 0, dutyR)
pwm.set_pwm(chFanL,0,0)
pwm.set_pwm(chFan1,0,0)
pwm.set_pwm(chFan2,0,0)
