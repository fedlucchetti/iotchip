#!/usr/bin/python
import sys, getopt, time
import RPi.GPIO as GPIO

def main(argv):
    opts, args = getopt.getopt(argv,"p:",[])
    print("trying to run led/on.py: ")
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(int(args[0]), GPIO.OUT)
    frequency = 1000
    pwm = GPIO.PWM(int(args[0]), frequency)
    pwm.start(0)
    print("starting duty cycle loop with ... "+args[1])
    while True:
        pwm.ChangeDutyCycle(100-int(args[1]))
        time.sleep(10)

if __name__ == "__main__":
    main(sys.argv[1:])
