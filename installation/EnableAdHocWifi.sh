#!/bin/bash

# Variables
FILENAME=/etc/network/interfaces

# edit /etc/network/interfaces file to setup ad-hoc wifi and lte

sudo echo "source-directory /etc/network/interfaces.d" > /etc/network/interfaces

sudo echo "auto lo" >> /etc/network/interfaces
sudo echo "iface lo inet loopback" >> /etc/network/interfaces

sudo echo "iface eth0 inet dhcp" >> /etc/network/interfaces

sudo echo "allow-hotplug eth1" >> /etc/network/interfaces
sudo echo "auto eth1" >> /etc/network/interfaces
sudo echo "iface eth1 inet dhcp" >> /etc/network/interfaces

sudo echo "auto wlan0" >> /etc/network/interfaces
sudo echo "iface wlan0 inet static" >> /etc/network/interfaces
sudo echo "  address 10.2.1.14" >> /etc/network/interfaces
sudo echo "  netmask 255.255.255.0" >> /etc/network/interfaces
sudo echo "  wireless-channel 1" >> /etc/network/interfaces
sudo echo "  wireless-essid PiAdHocNetwork" >> /etc/network/interfaces
sudo echo "  wireless-mode ad-hoc" >> /etc/network/interfaces


exit 0;