#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#

# Variables
LOGPATH=/home/pi

# Find mac (hardware) address and store in variable
NEWHOSTNAME=$(cat /sys/class/net/eth0/address) 
# get rid of colons (':'), e.g. replace ':' with ''
NEWHOSTNAME=${NEWHOSTNAME//:/}
# take the last four characters of the mac address
NEWHOSTNAME=${NEWHOSTNAME:(-4)}

# Change hostname
echo "-> Changing hostname to last four characters of mac address..." | tee -a $LOGPATH/PC_install_log.txt
sudo hostname $NEWHOSTNAME
sudo echo $NEWHOSTNAME > /etc/hostname | tee -a $LOGPATH/PC_install_log.txt
# replace hostname in /etc/hosts
sudo sed -i -e "s/$HOSTNAME/$NEWHOSTNAME/g" /etc/hosts | tee -a $LOGPATH/PC_install_log.txt
# restart hostname process
sudo /etc/init.d/hostname.sh start | tee -a $LOGPATH/PC_install_log.txt

exit 0;