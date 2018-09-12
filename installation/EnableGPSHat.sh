#!/bin/bash

# Variables
LOGPATH=/home/pi

# This script enables using the GPS Hat of the Raspberry Pi through the serial

# install dependencies
sudo apt-get install gpsd gpsd-clients python-gps -y
# modify the default settings
sudo bash -c 'echo START_DAEMON="true" > /etc/default/gpsd'
sudo bash -c 'echo GPSD_OPTIONS="-n" >> /etc/default/gpsd'
sudo bash -c 'echo DEVICES="/dev/serial0" >> /etc/default/gpsd'
sudo bash -c 'echo GPSD_SOCKET="/var/run/gpsd.sock" >> /etc/default/gpsd'
sudo bash -c 'echo USBAUTO="true" >> /etc/default/gpsd'

# modify the serial port usage

if sudo grep -i -q "console=serial0,115200" /boot/cmdline.txt; then
	# erase the expression from the file (this disables login via the serial port)
	sudo sed -i -e 's/console=serial0,115200 //g' /boot/cmdline.txt
	echo "Disabled login via serial port." | tee -a $LOGPATH/RH_install_log.txt
else
	# you're good!
	echo "Login via serial port already disabled." | tee -a $LOGPATH/RH_install_log.txt
fi

# check if splash is there for boot
if sudo grep -i -q "splash" /boot/cmdline.txt; then
	# check if plymouth.ignore-serial-consoles is there
	if sudo grep -i -q "plymouth.ignore-serial-consoles" /boot/cmdline.txt; then
		# you're good!
		echo "Splash screen already told to ignore serial console." | tee -a $LOGPATH/PC_install_log.txt
	else
		# add command to ignore serial console
		sudo echo "plymouth.ignore-serial-consoles" >> /boot/cmdline.txt
		echo "Updated splash screen to ignore serial console." | tee -a $LOGPATH/PC_install_log.txt
	fi
else
	echo "No splash screen is used, so no updates needed." | tee -a $LOGPATH/PC_install_log.txt
fi