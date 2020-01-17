#!/usr/bin/python
# IoT Chip project version : 2.0

import os
import time
import datetime
import subprocess

import utils

class CameraUSB:

    def __init__(self):
        print("Camera USB initialized - no configuration found")

    def capture(self):
        photosPath = utils.getContextPath()+"/data/photos"
        tstamp = time.time()
        dtstr = datetime.datetime.fromtimestamp(tstamp).strftime('%Y%m%d%H%M%S')
        subprocess.call(["fswebcam","-r","1280x720","--no-banner",photosPath+'/snapshot_'+str(dtstr)+'.jpg'])
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
    