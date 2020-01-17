#!/usr/bin/python
# IoT Chip project version : 3.0
import time
import json
import urllib2
from beans import utils

from beans import GrowLED 
from beans import FanController 
from beans import ExecutePWM 
from beans import FrontLED


confs     = utils.getConfiguration('BaseURL')
baseUrl   = confs['path']

confs     = utils.getConfiguration('HTTP_request_frequency')
frequency = float(confs['value'])
print('http frequency = ' + str(frequency) + ' s')

        
#baseUrl = "https://planthive-uat.appspot.com"
#frequency = 10 # every X sec a request is sent

x_read_server_json = True


ledsObj    = GrowLED.GrowLED()
fanObj     = FanController.FanController()
pwm        = ExecutePWM.ExecutePWM()
frontled   = FrontLED.FrontLED()

###-------------------------------------
### Read Configurations from Server
###-------------------------------------

### JSON request method

try:
    serialNumber = utils.getSerialNumber()
except Exception,e: 
    utils.log("Microchip: ")
    utils.log(str(e))
except:
    utils.log("Microchip: Unknown Error")
#serialNumber = '0000000000000002'

url = baseUrl+"/api/v1/en/planthive/get-device-command/" + serialNumber

print('request data from  ' + url)

while True:
    time.sleep(frequency)
    if x_read_server_json:
        #print("- - - - - - - - - - - - - - - - - - - - ")
        #print("Reading Configuration Data from Server JSON Request...")
        isDataValid = False
        data = {}
        
        try :
            response = urllib2.urlopen(url)
            data = json.loads(response.read())
            print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception,e: 
            utils.log("Server JSON Request: "+str(e))
        except:
            utils.log("Server JSON Request: Unknown Error")
        
        
        try :
            confPath = utils.getContextPath()+'/conf'
            with open(confPath+'/fetched_data.json', "w") as confJSONfile:
                json.dump(data, confJSONfile, indent=4, separators=(',', ': '))

        except Exception,e: 
            utils.log("JSON writing Request: "+str(e))
        except:
            utils.log("JSON writing Request: Unknown Error")
            

    ledsObj.execute(data)
    fanObj.execute()
    frontled.checkup()
    
    
    
    #print('running PWM')
    try:
        pwm.runPwm()
    except:
        print('error running execute pwm')
    
         
    



