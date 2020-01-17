#!/bin/bash
# IoT Chip project version : 3.0

updated=false
# updatedSourceList=false





# I2C
if grep "#dtparam=i2c_arm=on" /boot/config.txt ; then
	sudo echo "dtparam=i2c_arm=on" >> /boot/config.txt
	echo "/boot/config.txt updated with I2C arm on"
	updated=true
else
	echo "I2C already configured - /boot/config.txt"
fi




# clock
if grep "dtoverlay=i2c-rtc,ds1307" /boot/config.txt ; then
	echo "SPI already configured - /boot/config.txt"
else
	sudo echo "dtoverlay=i2c-rtc,ds1307" >> /boot/config.txt
	echo "/boot/config.txt updated with dtoverlay=i2c-rtc,ds1307"
	echo "rebooting..."
	echo "After reboot please execute install.sh and run option Install Sensors"
	sleep 3
	sudo reboot
fi

if grep "dtoverlay=i2c-rtc,ds1307" /boot/config.txt ; then
	sudo apt-get -y remove fake-hwclock
	sudo update-rc.d -f fake-hwclock remove
	echo "Cleaning fake hwclock done"
else
	sudo echo "dtoverlay=i2c-rtc,ds1307" >> /boot/config.txt
	echo "/boot/config.txt updated with dtoverlay=i2c-rtc,ds1307"
	sudo reboot
fi

if grep "#if \[ -e /run/systemd/system \] ; then.*#.*exit 0.*#fi" /lib/udev/hwclock-set ; then
	echo "Cleaning faske hwclock done"
else
	sudo python edit_hwclock.py 
	sudo hwclock -D -r
fi


# Samples with sed
# Sample 1
#if grep "if [ -e /run/systemd/system ] ; then\r\n exit 0\r\nfi" /lib/udev/hwclock-set ; then
#	echo "already configured"
#else
#	sudo sed -i "s/if [ -e \/run\/systemd\/system ] ; then/#if [ -e \/run\/systemd\/system ] ; then/g" /etc/inittab
#fi
# Sample 2
#if grep "deb http://archive.raspberrypi.org/debian/ wheezy main untested" /etc/apt/sources.list.d/raspi.list ; then
#	echo "update source already configured - /etc/apt/sources.list.d/raspi.list"
#else
#	sudo sed -i '1,5 s/^/#/' /etc/apt/sources.list.d/raspi.list
#	sudo echo "deb http://archive.raspberrypi.org/debian/ wheezy main untested" >> /etc/apt/sources.list.d/raspi.list
#	echo "/etc/apt/sources.list.d/raspi.list updated."
#  updated=true
#	#updatedSourceList=true
#fi

# Update if new source
# if $updatedSourceList ; then
#	updated=true
#	echo "updating and upgrading..."
#	sudo apt-get -y update
#	# sudo touch /var/run/iotchip_upgrade_host.txt
#	sudo apt-get -y upgrade
#	# sudo rm /var/run/iotchip_upgrade_host.txt
# fi

# Reboot if anything is updated
if $updated ; then
	echo "rebooting..."
	sudo reboot
fi
