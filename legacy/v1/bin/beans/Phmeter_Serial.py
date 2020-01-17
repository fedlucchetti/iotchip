#!/usr/bin/python
import serial

class Phmeter_Serial:

    'Common base class for PH Serial sensors'

    def __init__(self):
        print("PH Meter Serial Controller initialized");
   
    # input as pin or usb
    def get(self):
        print("Getting PH...")
        usbport = '/dev/ttyAMA0' #default
        ser = serial.Serial(
            port=usbport,\
            baudrate=9600,\
            parity=serial.PARITY_NONE,\
            stopbits=serial.STOPBITS_ONE,\
            bytesize=serial.EIGHTBITS)
        dPh = ""
        k = 0
        while(k<8):
            y = ser.write('P')
            dPh = dPh + ser.read()
            k = k + 1
        return dPh[3:]
