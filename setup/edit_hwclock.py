#!/usr/bin/python
import sys, os

file2 = open("/lib/udev/hwclock-set-new","w")
file = open("/lib/udev/hwclock-set","r+")
lines = file.readlines()
indexOfFound = ""

i = 0
for line in lines:
    print(str(i)+": "+line)
    if line=="if [ -e /run/systemd/system ] ; then"+"\n":
        modLine = "#if [ -e /run/systemd/system ] ; then"+"\n"
        file2.write(modLine)
        print(modLine)
        indexOfFound = i
    elif str(indexOfFound).isdigit() and i == int(indexOfFound) + 1:
        file2.write("# exit 0"+"\n")
        print("#exit 0")
    elif str(indexOfFound).isdigit() and i == int(indexOfFound) + 2:
        file2.write("#fi"+"\n")
        print("#fi")
    else :
        file2.write(line)
        print(line)
    i+=1

file.close()
file2.close()

os.remove("/lib/udev/hwclock-set")
os.rename("/lib/udev/hwclock-set-new","/lib/udev/hwclock-set")
