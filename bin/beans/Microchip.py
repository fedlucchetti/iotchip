#!/usr/bin/python
# IoT Chip project version : 2.0

import os
import subprocess as subprocessRef
import re
import sys
import getopt
import utils

class Microchip:

    'Common base class for microchip : raspberry, olimex'

    name = "Microchip"
    serialNumber = None

    # def special_match(strg, search=re.compile(r'[^00-9.]').search):
    #    return not bool(search(strg))

    # commented print for nodejs stdout reads all outputs
    def __init__(self):
        confs = utils.getConfiguration(self.name)
        if confs != None and confs['serial_number'] != None :
            self.serialNumber = str(confs['serial_number'])
            # print("Microchip initialized - configuration found")
        else:
            serialNumber = self.detectSerialNumber()
            self.serialNumber = serialNumber
            newConfs = [('serial_number',serialNumber)]
            utils.setConfiguration(self.name,newConfs)
            # print("Microchip initialized - Warning: new configuration")
    
    def detectSerialNumber(self):
        cmdTok = ["""cat /proc/cpuinfo |grep Serial"""]
        serialtext = subprocessRef.check_output(cmdTok,shell=True)
        serialNumber = serialtext[-16:]
        return serialNumber

    def getSerialNumber(self):
        return self.serialNumber

    def main(argv):
        try:
            opts, args = getopt.getopt(sys.argv[1:],"n",[])
            obj = Microchip()
            if len(opts) > 0:
                for x,y in opts:
                    #print(str(x)+" "+str(y))
                    if x == '-n':
                        sn = obj.getSerialNumber()
                        print str(sn)
                        return str(sn)
            else:
                print 'Microchip.main -n'
        except getopt.GetoptError,e:
            print('Microchip.main GetoptError: '+str(e))
        except Exception,ex:
            print("Microchip.main Exception: "+str(ex))
        except:
            print("Microchip.main unknown error")

if __name__ == "__main__":
    Microchip().main()