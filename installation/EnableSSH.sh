#!/usr/bin/env bash
# -*- coding: utf-8 -*-

# Variables
LOGPATH=/home/pi

# create a file named ssh in /boot
sudo touch /boot/ssh | tee -a $LOGPATH/PC_install_log.txt
echo "-> Enabled ssh..." | tee -a $LOGPATH/PC_install_log.txt



