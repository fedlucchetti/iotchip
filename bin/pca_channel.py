# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time
import sys
# Import the PCA9685 module.
import Adafruit_PCA9685
from beans import utils


# initialise the PCA9685 using the default address (0x40).
pwm  = Adafruit_PCA9685.PCA9685()
conf = utils.getConfiguration("PCA_PWM_frequency")
f    = int(float(conf["value"]))
pwm.set_pwm_freq(f)

pwm.set_pwm(int(sys.argv[1])  , 0, int(sys.argv[2]))
