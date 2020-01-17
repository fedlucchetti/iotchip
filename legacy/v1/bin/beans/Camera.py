#!/usr/bin/python
# IoT Chip project version : 2.0

import picamera
import os
import time
import datetime
import subprocess
import json

import utils

class Camera:

    name = "Camera"
    option_snapshot_vflip = False
    option_snapshot_hflip = False

    isOn = False

    def __init__(self):
        confs = utils.getConfiguration(self.name)
        if confs != None :
            if confs['option_snapshot_vflip'] == 'True':
                self.option_snapshot_vflip = True
            if confs['option_snapshot_hflip'] == 'True':
                self.option_snapshot_hflip = True
            print("Camera initialized - configuration found")
        self.isOn = bool(self.getInRam()['camera_is_on'])

    def stopRPiCWI(self):
        print("Trying to Stop Camera with RPi Cam Web Interface...")
        utils.log("Trying to Stop Camera with RPi Cam Web Interface...")
        libPackPath = utils.getContextPath()+"/lib/RPi_Cam_Web_Interface"
        subprocess.call(["sudo", "chmod", "+x", libPackPath+"/stop.sh"])
        subprocess.call(["sudo", libPackPath+"/stop.sh"])
        self.isOn = False
        self.persistInRam({'camera_is_on':False})

    def startRPiCWI(self):
        if not self.isOn :
            print("Trying to Start Camera with RPi Cam Web Interface...")
            utils.log("Trying to Start Camera with RPi Cam Web Interface...")
            libPackPath = utils.getContextPath()+"/lib/RPi_Cam_Web_Interface"
            subprocess.call(["sudo", "chmod", "+x", libPackPath+"/start.sh"])
            subprocess.call(["sudo", libPackPath+"/start.sh"])
            self.isOn = True
            self.persistInRam({'camera_is_on':True})
   
    def capture(self):
        with picamera.PiCamera() as camera:
            camera.sharpness = 0
            camera.contrast = 0
            camera.brightness = 50
            camera.saturation = 0
            camera.ISO = 0
            camera.video_stabilization = False
            camera.exposure_compensation = 0
            camera.exposure_mode = 'auto'
            camera.meter_mode = 'average'
            camera.awb_mode = 'auto'
            camera.image_effect = 'none'
            camera.color_effects = None
            camera.rotation = 0
            camera.hflip = self.option_snapshot_hflip
            camera.vflip = self.option_snapshot_vflip
            camera.crop = (0.0, 0.0, 1.0, 1.0)
            photosPath = utils.getContextPath()+"/data/photos"
            tstamp = time.time()
            dtstr = datetime.datetime.fromtimestamp(tstamp).strftime('%Y%m%d%H%M%S')
            camera.capture(photosPath+'/snapshot_'+str(dtstr)+'.jpg')
            camera.close()
            del(camera)
            return photosPath+'/snapshot_'+str(dtstr)+'.jpg'

    def cleanUpRepository(self,doRemove=False):
        tstamp = time.time()
        dtstr = datetime.datetime.fromtimestamp(tstamp).strftime('%Y%m%d%H%M%S')
        photosPath = utils.getContextPath()+"/data/photos"
        print("Starting Camera Repository CleanUp... path: "+photosPath)
        utils.log("Starting Camera Repository CleanUp... path: "+photosPath)
        for file in os.listdir(photosPath):
            if file.endswith(".jpg") :
                #print(file[9:][0:8])
                if int(file[9:][0:8]) < int(dtstr[0:8])-2 :
                    if doRemove :
                        print("Removing "+photosPath+os.path.sep+file+"...")
                        utils.log("Removing "+photosPath+os.path.sep+file+"...")
                        os.remove(photosPath+os.path.sep+file)
                    else :
                        print("Marked for removal: "+photosPath+os.path.sep+file)
                        utils.log("Marked for removal: "+photosPath+os.path.sep+file)
                        
    def execute(self, data):
        try:
            if data and 'camera_activity' in data and (data['camera_activity'] == "0" or data['camera_activity'] == "false" or data['camera_activity'].lower() == "off") :
                print("Switching Camera Off")
                self.stopRPiCWI()
            elif data and 'camera_activity' in data and (data['camera_activity'] == "1" or data['camera_activity'] == "true" or data['camera_activity'].lower() == "on") :
                print("Switching Camera On If Not Already On")
                self.startRPiCWI()
        except Exception,e: 
            print "Camera :"
            print str(e)
        except:
            print "Camera : Unknown Error"

    def persistInRam(self, data):
        parentPath = os.path.abspath(os.path.dirname(__file__))
        with open(parentPath+'/camera.ram.json', 'w') as outfile:
            json.dump(data, outfile)

    def getInRam(self):
        try:
            parentPath = os.path.abspath(os.path.dirname(__file__))
            with open(parentPath+'/camera.ram.json') as dataFile:    
                data = json.load(dataFile)
                return data
        except Exception,e:
            if str(type(e).__name__) == "ValueError":
                self.persistInRam({'camera_is_on':False})
                return {'camera_is_on':False}
            if str(type(e).__name__) == "IOError":
                self.persistInRam({'camera_is_on':False})
                return {'camera_is_on':False}
            else:
                print(str(e))
                print "Camera getInRam: "+str(e)
        except:
                print("Camera getInRam : Unknown Error")