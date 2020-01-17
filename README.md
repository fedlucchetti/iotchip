# IoT Chip for Box Project

This Readme file covers the IoT box software.    

Environment:
* Raspberry Pi - Jessie

For the full documentation please refer to 
[Official IoT Project Docs](http://escorp.ddns.net:55575/iotbox/software-docs/)

## Development
To contribute to the development process, make sure you have a proper developer 
access to this project.   
### Contributors
Only valid GitLab accounts with <i>@planthive.com</i> address and third-party 
contributors are allowed into this project. 



## Installation
     $ mv iotchip_alpha/ iotchip
     $ cd iotchip/
     $ sudo chmod +x install.sh
     $ sudo ./install.sh

Choose options in this sequence (you might be prompted to reboot when necessary)

     $ (2 , 1)
     $ (2 , 2)
     $ (3)
     $ (4)
     $ (7) --> reboot
     $ (7) --> again!!
     $ (5)



Check whether daemons run flawlessly

     $ sudo systemctl status app_get_json.service
     $ sudo systemctl status app_send_json.service


## Edit configuration, key values, pins  (advanced users)
     $ nano /conf/keys.ini 


## Git commands
	$ git pull origin dev
	$ git fetch origin dev
	$ git clone ...
	$ 
	$ // stores the credentials indefinitely:
	$ git config credential.helper store
	$ // save credentials for 1 hour
	$ git config credential.helper 'cache --timeout=3600'
	$ // setup config
	$ sudo git config --global user.email "git.reporter@planthive.com"
	$ sudo git config --global user.name "Git Reporter"
	$ // force pull
	$ sudo git fetch origin alpha-stable
	$ sudo git reset --hard FETCH_HEAD
	$ // Clean up worktree to match .gitignore
	$ sudo git rm -r --cached .
	$ sudo git add .
	$ sudo git commit -m ".gitignore is now working"

## Application Context Path
The software application directories are located under `/opt/iotchip` or `/home/pi/iotchip`
This path is defined in multiple locations through predefined variables for python 
or hardcoded in shell files:
* <b>/bin/beans/utils</b> : for Python context, `utils.getContextPath()` will 
return <i>CONTEXT_PATH</i> value `/opt/iotchip` or `/home/pi/iotchip`

## Configuration files
Hardware configuration such as pins, sensor codes, serial numbers and other 
access or hardware tokens are stored in:  
`/iotchip/conf/keys.ini` 

<b>Be aware of invalid characters to use within INI files, this might cause the 
application to fail!</b> 

## Reserved Ports
* WAN : 8184

## Reserved Pins
* GPIO Pin / Pullup : 4



## Dimmer PWM Notes
Although a Dimmer is a safe way of controling the intensity of a device, it has its own 
technical flows such as the Python method that initializes the dimmer has to be called once 
because the library init method resets all channels upon the call of pwm.setPwm()

Therefore, a DimmerController class has been created, along with a Json file in /conf.
A supported device can register a change to PWM value through the DimmerController. 
Those changes are written in /conf/pwm_conf.json and later execute when runPwm() is called.
<b>Make sure to call runPwm() after each channel value modification</b>

### Supported Devices:
* GrowLedController
* FanController
* FrontLedPanel

### runPwm Calls
* get_data.py
* in each supported device main() method, used in NodeJs:
	* GrowLedController
	* FrontLedPanel
	* FanController

## Tutorials and sources
* RPi models:
    * http://www.raspberrypi-spy.co.uk/2012/06/simple-guide-to-the-rpi-gpio-header-and-pins/#prettyPhoto
* WiFi Dongle :
    * http://www.howtogeek.com/167425/how-to-setup-wi-fi-on-your-raspberry-pi-via-the-command-line/
* RPi Web Cam Interface : 
    * http://www.sitepoint.com/streaming-a-raspberry-pi-camera-into-vr-with-javascript/
    * http://elinux.org/RPi-Cam-Web-Interface
    * http://www.rs-online.com/designspark/electronics/knowledge-item/raspberry-pi-camera-setup
* Thermometer (Aqua) : 
    * https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/temperature/
* RadioEmitter : 
    * http://damien-battistella.fr/controle-de-prise-chacon-dio-first-via-raspberrypi/
    * http://www.homautomation.org/2013/10/09/how-to-control-di-o-devices-with-a-raspberry/
* Pusher WebSockets : 
* Pusher HTTP Python Library
    * https://github.com/pusher/pusher-http-php.git
    * https://github.com/pusher/pusher-http-python.git
* ekulyk/PythonPusherClient
    * https://github.com/ekulyk/PythonPusherClient.git
* liris/websocket-client		
    * https://github.com/liris/websocket-client.git
    * https://github.com/ekulyk/websocket-client.git
* Pusher NodeJS
    * https://github.com/pusher/pusher-http-node
    * `$ npm install pusher`
    * `$ npm install pusher-client`
    * https://pusher.com/docs/javascript_quick_start#/lang=node
* Requests
    * http://docs.python-requests.org/en/latest/
* Other:
    * https://github.com/CisecoPlc/B047-Slice-of-Relay
    * https://github.com/Gadgetoid/WiringPi2-Python.git
    * https://pinout.xyz/pinout/pin12_gpio18 <-- Good One
    * https://github.com/adafruit/Adafruit_TSL2591_Library
    * https://github.com/Gadgetoid/WiringPi2-Python
    * https://archive.raspberrypi.org/debian/dists/wheezy/main/

## Usefull commands
	$ sudo date -s "Thu Apr 28 23:31:01 UTC 2016" : set date and time manually 
	(use raspi-config on rpi)
	$ setxkbmap be/fr/us : changes keyboard layout from terminal on debian 
	$ df -h : view partition table
	$ ifconfig : view network configuration 
	$ sudo /etc/init.d/network-manager restart : restart network
	$ sudo dhclient -v wlan0 : request DHCP binding
	$ sudo ifdown/ifup wlan0 : switch on/off dungle ip configuration
	$ sed : string and regex manipulation doc : http://www.grymoire.com/Unix/Sed.html
	$ top : view processes
	$ ps : current user processes
	
