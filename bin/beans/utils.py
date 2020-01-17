#!/usr/bin/python
# IoT Chip project version : 3.0

import subprocess as subprocessRef
import json
import ConfigParser
import urllib 
import urllib2 
import socket
import fcntl
import struct


## Context Path

#CONTEXT_PATH='/opt/iotchip' # new version
CONTEXT_PATH='/home/pi/iotchip' # current version
#CONTEXT_PATH='/home/erebus/Documents/Iotchip_Beta/iotchip_v03/'
#CONTEXT_PATH='/home/ergonium/Documents/iotchip/iotchip_v03'

def getContextPath():
    return CONTEXT_PATH


## Configuration File

def getConfiguration(name):
    config = ConfigParser.ConfigParser()
    confPath = getContextPath()+'/conf/keys.ini'
    config.read(confPath)
    if config.has_section(name):
        return dict(config.items(name))
    else :
        print("Configuration "+name+" not found")
        return None

def setConfiguration(name,data):
    try :
        config = ConfigParser.ConfigParser()
        confPath = getContextPath()+'/conf/keys.ini'
        config.read(confPath)
        config.add_section(name)
        for x, y in data:
            config.set(name, x, y)
        with open(confPath, 'wb') as configfile:
            config.write(configfile)
    except Exception,e:
        print("setConfiguration("+name+",data): " + str(e))

def getSerialNumber():
    serialNumber = "0000000000000000"
    try:
        f = open('/proc/cpuinfo','r')
        for line in f:
            if line[0:6]=='Serial':
                serialNumber = line[10:27]
        f.close()
    except:
        serialNumber = "ERROR000000000"
    return serialNumber


## Logging

def log(text):
    """ The log file must exist """
    print(str(text))
    #try:
    #    logPath = CONTEXT_PATH+'/logs/log.txt'
    #    logging.basicConfig(filename=logPath,level=logging.DEBUG)
    #    nowDateTime = datetime.now()
    #    logging.debug(str(nowDateTime)+": "+text)
    #except Exception,e:
    #    print("Log Warning: "+str(e))


## Read/Write File

def fwrite(file, content):
    try:
        afile = open(file,'w')
        afile.truncate()
        afile.write(str(content))
        afile.close()
    except Exception,e:
        print("Error fwrite: "+str(e))
    except:
        print("Error fwrite: unknown")

def fread(file):
    try:
        afile = open(file,'r')
        line = str(afile.read(16))
        afile.close()
        return line
    except Exception,e:
        print("Error fread: unknown")

def test_inet():
    loop_value = 1
    while (loop_value == 1):
        try:
            urllib.urlopen("https://www.google.com/")
        except urllib2.URLError, e:
            print "Network down."
            return False
        else:
            loop_value = 0
            return True


## Network
## getIPAddress takes the network interface name as attribute ex. getIPAddress('wlan0')
def getIPAddress(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

## Read Write / Save to JSON file

def updateJSONFile(file,data):
    try:
        with open(file) as f:
            feeds = json.load(f)
    except:
        print('Nothing')
        feeds = {}
    feeds.update(data)
    #print feeds
    with open(file,'w') as cft:
        json.dump(feeds, cft, indent=4, separators=(',',': '))

def get_PWM_file():
    confPath = getContextPath()+'/conf'
    pwm_data = {}
    try:
        with open(confPath+'/pwm_conf.json') as data_file:    
            pwm_data = json.load(data_file)
    except:
        print('Error loading PWM file')
    return pwm_data

def get_LED_PWM_file():
    confPath = getContextPath()+'/conf'
    pwm_data = {}
    try:
        with open(confPath+'/growLED_pwm_conf.json') as data_file:    
            pwm_data = json.load(data_file)
    except:
        print('Error loading PWM file')
    return pwm_data

def get_fetched_JSON_file():
    confPath = getContextPath()+'/conf'
    data = {}
    try:
        with open(confPath+'/fetched_data.json') as data_file:    
            data = json.load(data_file)
    except:
        print('Error loading fetched json')
    return data

def register(data):
    confPath = getContextPath()+'/conf'
    updateJSONFile(confPath+'/pwm_conf.json',data)
    
def register_LED(data):
    confPath = getContextPath()+'/conf'
    updateJSONFile(confPath+'/growLED_pwm_conf.json',data)

def app_send_json(data):
    confs     = getConfiguration('BaseURL')
    baseUrl   = confs['path']
    print('Attempting to post to   ' + baseUrl+'/api/v1/en/planthive/post-device-data')
    try:
   		print("Sending Data to Server...")
    		# Send Data
    		reqData = urllib2.Request(baseUrl+'/api/v1/en/planthive/post-device-data')
    		reqData.add_header('Content-Type','application/json')
    		respData = urllib2.urlopen(reqData,json.dumps(data)).read()
    		print(respData)
    except Exception,e:
    		utils.log("Sending Data: "+str(e))

def app_get_json():
    data         = {}
    confs        = getConfiguration('BaseURL')
    baseUrl      = confs['path']
    serialNumber = getSerialNumber()
    url          = baseUrl+"/api/v1/en/planthive/get-device-command/" + serialNumber
    
    try :
        response = urllib2.urlopen(url)
        data = json.loads(response.read())
        print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    except Exception,e: 
        utils.log("Server JSON Request: "+str(e))
    except:
        utils.log("Server JSON Request: Unknown Error")

    return data

    

