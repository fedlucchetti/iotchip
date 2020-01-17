#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. && pwd )"
export installdir="$DIR"

#if [ ! -f /var/run/iotchip_upgrade_host.txt ]; then
#    echo "No Upgrade Required"
#	echo "No Upgrade Required" >> "$installdir/logs/reboot_log.txt"
#else
#	echo "Upgrade Executed" >> "$installdir/logs/reboot_log.txt"
#	sudo rm /var/run/iotchip_upgrade_host.txt
#	sudo apt-get -y upgrade
#fi

sudo modprobe w1-gpio
echo "modprobe w1-gpio executed" >> "$installdir/logs/reboot_log.txt"

sudo modprobe w1-therm
echo "modprobe w1-therm executed" >> "$installdir/logs/reboot_log.txt"

# sudo rm "$installdir"/bin/scripts/fan/pid_*
# sudo rm "$installdir"/bin/scripts/led/pid_*
# echo "scripts PIDs deleted" >> "$installdir/logs/reboot_log.txt"

# sudo python "$installdir"/bin/beans/IndicatorPanel.py -c
# echo "indicator panel checked up" >> "$installdir/logs/reboot_log.txt"

#chmod +x "$installdir/run/boxbgsvc.sh"
#nohup "$installdir/run/boxbgsvc.sh" &
#echo "nohup executed" >> "$installdir/logs/reboot_log.txt"

echo "reboot script executed" >> "$installdir/logs/reboot_log.txt"
