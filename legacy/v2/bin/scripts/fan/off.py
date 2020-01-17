#!/usr/bin/python
import sys, getopt, time
import RPi.GPIO as GPIO

def main(argv):
    opts, args = getopt.getopt(argv,"p:",[])
    print("trying to run fan/off.py: ")
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(int(args[0]), GPIO.OUT)
    frequency = 1
    pwm = GPIO.PWM(int(args[0]), frequency)
    pwm.start(0)
    print("starting duty cycle loop... ")
    while True:
        pwm.ChangeDutyCycle(100)

if __name__ == "__main__":
    main(sys.argv[1:])
