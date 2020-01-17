#!/usr/bin/python
# IoT Chip project version : 2.0
import datetime
import sys
import json
import urllib2
import time
import subprocess
import os
import logging
from beans import utils
from beans import Microchip as microchipRef
frequency = 60 # every X sec a request is sent

x_send_server_data = True

baseUrl = " https://planthive-uat.appspot.com"

new_data_file_path = '/home/pi/iotchip/data/new_data2send.json'
old_data_file_path = '/home/pi/iotchip/data/old_data2send.json'


try:
    serialNumber = utils.getSerialNumber()
except Exception,e: 
    utils.log("Microchip: ")
    utils.log(str(e))
except:
    utils.log("Microchip: Unknown Error")
    
#serialNumber = '0000000000000002'
#serialNumber = 0000000000000001

while True:
	
	try:
		with open(old_data_file_path) as f:
			olddata = json.load(f)
	except Exception,e:
                        utils.log("Error opening Json data file "+str(e))

		
	timestamp = int(time.time())*1000.0
	now = datetime.datetime.now()
	print now.year, now.month, now.day, now.hour, now.minute, now.second

	try:
                with open(new_data_file_path) as f:
                        newdata = json.load(f)
        except Exception,e:
                        utils.log("Error opening Json data file "+str(e))



	#with open(new_data_file_path) as f:
	#	newdata = json.load(f)
	#print json.dumps(newdata, indent=4, sort_keys=True)


###-----------------------------
### Test if values have changed
###-----------------------------
	print('tnow = ' + str(newdata['timeMinutes']+60*newdata['timeHours']))
	print('tbefore = ' + str(olddata['timeMinutes']+60*olddata['timeHours']))



	if newdata['temperature']!=olddata['temperature'] or newdata['temperature']!=olddata['temperature'] or newdata['temperature']!=olddata['temperature']:
		data_changed = True
	else:
		data_changed = False

###----------------------
### Send Data to server
###----------------------

	if x_send_server_data and data_changed :
		print('Attempting to post to   ' + baseUrl+'/api/v1/en/planthive/post-device-data')
    		try:
       			print("Sending Data to Server...")
        		# Send Data
        		reqData = urllib2.Request(baseUrl+'/api/v1/en/planthive/post-device-data')
        		reqData.add_header('Content-Type','application/json')
        		respData = urllib2.urlopen(reqData,json.dumps(newdata)).read()
        		print(respData)
    		except Exception,e:
        		utils.log("Sending Data: "+str(e))
    
    	time.sleep(frequency)

