#!/usr/bin/python
import ConfigParser
import os
import subprocess
import sys
import getopt

from beans import utils

class RadioEmitter(object):
    'Class for Radio Emitter Switch'

    name = "RadioEmitter"
    pin = 21
    digits = 12345678

    def __init__(self):
        config = ConfigParser.ConfigParser()
        #confPath = os.path.dirname(__file__) + '/../../conf/keys.ini'
        confPath = utils.getContextPath()+'/conf/keys.ini'
        config.read(confPath)
        if config.has_section(self.name):
            self.pin = config.get(self.name, 'pin')
            self.digits = config.getint(self.name, 'digits')
        else :
            try :
                config.add_section(self.name)
                config.set(self.name, "pin", 21)
                config.set(self.name, "digits", 12345678)
                with open(confPath, 'wb') as configfile:
                    config.write(configfile)
            except Exception,e:
                print(self.name+" Config Key: " + str(e))

    # input 0, 1 or 2
    def switchPower(self, input, onOff):
        #libPackPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))+"/lib/wiringPi"
        libPath = utils.getContextPath()+'/lib/wiringPi'
        # print("Path: "+libPackPath)
        ### when shell=True sudo will no work
        # subprocess.call("pwd",shell=True)
        #subprocess.call(["sudo", "chmod", "+x", libPackPath+"/build"])
        #subprocess.call(["sudo", libPackPath+"/build"])
        #subprocess.call(["sudo", "chmod", "+x", libPackPath+"/makefile"])
        #subprocess.call(["sudo", libPackPath+"/make"])
        subprocess.call(["sudo", "chmod", "+x", libPath+"/send"])
        subprocess.call(["sudo", libPath+"/send", str(self.pin), str(self.digits), str(input), onOff])

    def test(self):
        print("test is currently commented, to use this method, uncomment in Class RadioEmitter")
        # for x in range(0, 32):
        #     print "Testing %d" % (x)
        #     subprocess.call(["pwd"])
        #     subprocess.call(["sudo", "./iotchip/bin/lib/wiringPi/send", str(x), "12345678", "0", "on"])
        # subprocess.call(["sudo", "./iotchip/bin/lib/wiringPi/send", "21", "12345678", "0", "off"])
        # time.sleep(3)
        # subprocess.call(["sudo", "./iotchip/bin/lib/wiringPi/send", "21", "12345678", "0", "on"])
        # sys.exit(0)

    def run(argv):
        try:
            opts, args = getopt.getopt(sys.argv[1:],"0:1:on:off",[])
        except getopt.GetoptError,e:
            print 'RadioEmitter: main.py 0|1|2|3 on|off'
            #sys.exit(2)
        #for arg in args:
        if len(args) > 0:
            if args[0] not in ("0","1","2","3") or args[1] not in ("on","0","On","ON","off","1","OFF","Off") :
                print 'RadioEmitter takes 2 arguments: 0|1|2|3 as target and on|1|ON|On OR off|0|OFF|Off as action'
                #sys.exit()
            elif args[0] in ("0","1","2","3") and args[1] in ("on","0","On","ON"):
                print 'RadioEmitter main.py on'
                RadioEmitter().switchPower(args[0],args[1])
            elif args[0] in ("0","1","2","3") and args[1] in ("off","1","OFF","Off"):
                print 'RadioEmitter main.py off'
                RadioEmitter().switchPower(args[0],args[1])
        else:
            print 'RadioEmitter: main.py 0|1|2|3 on|off'

if __name__ == "__main__":
    RadioEmitter().run()