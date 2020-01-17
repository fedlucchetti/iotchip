import datetime
import sys
import json
import urllib2
import time
import subprocess
import os
import logging
from beans import utils

new_data_file_path = '/home/pi/iotchip/data/new_data2send.json'
old_data_file_path = '/home/pi/iotchip/data/old_data2send.json'

# rename new file to old file

os.rename(new_data_file_path, old_data_file_path) 

# generate random Gaussian values
from random import seed
from random import gauss
#seed(1)

try:
    serialNumber = utils.getSerialNumber()
except Exception,e: 
    utils.log("Microchip: ")
    utils.log(str(e))
except:
    utils.log("Microchip: Unknown Error")
    
timestamp = int(time.time())*1000.0
now = datetime.datetime.now()



data = {
    'serial': serialNumber[:16],
    'timeHours': now.hour,
    'timeMinutes': now.minute,
    'temperature': round(gauss(22, 0.5)),
    'humidity': round(gauss(75, 0.5)),
    'moistures': round(gauss(75, 0.5)),
    'waterTemperature': round(gauss(22, 0.5)),
    'waterLevel':round(gauss(4, 0.5)) ,
    'lightDim':1,
    'lightMode':1,
    'dutyWhite': 50,
    'dutyBlue': 50,
    'dutyRed':50,
    'dutyFarRed':50,
    'pump' : 1,
    'fan' : 1,
    'humidifier' : 1,
    'climateControl': 0,
    'upgrades_status': {
        'waterpump_status': 0,
        'airpump_status': 0,
        'fan_status': 0,
        'humidifier': 0
	}
}



    
try:
    with open(new_data_file_path, 'w') as outfile:
        json.dump(data, outfile)
except:
    print('cannot open new data file')

print(data)
