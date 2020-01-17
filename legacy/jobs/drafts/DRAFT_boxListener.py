#!/usr/bin/python
#from pusher import Pusher
import pusherclient
import sys
import time
import json
import logging
from beans import Microchip as microchipRef

global pusher
global appkey
global serialNumber
global clientData

# Add a logging handler so we can see the raw communication data
root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
root.addHandler(ch)

def initialize():
    global appkey
    global serialNumber
    global clientData
    clientData = {}
    appkey = "f3a6952cc326ee48eb10"
    try:
        microchip = microchipRef.Microchip()
        serialNumber = microchip.getSerialNumber()
    except Exception,e: 
        print("Microchip: "+str(e))
            
# We can't subscribe until we've connected, so we use a callback handler 
# to subscribe when able
def connect_handler(data):
    global pusher
    global serialNumber
    channel = pusher.subscribe('channel_'+str(serialNumber))
    channel.bind('event_'+str(serialNumber), callback)

def callback(data):
    global clientData
    print("inside handler")
    print(data)
    clientData = data
    clientDatas = json.loads(data)
    if 'message' in data:
        print("Test successful!")

def ping_handler():
    print("pinging...")

def run():
    global serialNumber
    global clientData
    while True:
        # Do other things in the meantime here...
        print("Listening for "+str(serialNumber)+"...")
        print clientData
        time.sleep(2)

initialize()
pusher = pusherclient.Pusher("f3a6952cc326ee48eb10",True,"700363677ba4fd2d6f8c",{'cluster':'eu'},logging.INFO,True,None,2)
pusher.connection.bind('pusher:connection_established', connect_handler)
pusher.connect()
while True:
    # Do other things in the meantime here...
    print("Listening for "+str(serialNumber)+"...")
    print clientData
    time.sleep(2)
