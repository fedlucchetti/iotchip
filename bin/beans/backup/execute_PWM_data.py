#!/usr/bin/python
# IoT Chip project version : 3.0
# Author: Chicco Talo

from __future__ import division
import time
from beans import ExecutePWM as executepwmRef



pwm = executepwmRef.ExecutePWM()

def main():
    while True:
        try:
            pwm.runPwm()
            time.sleep(1)
        except:
            continue    
        
    


                
        
if __name__ == "__main__":
    main()             
