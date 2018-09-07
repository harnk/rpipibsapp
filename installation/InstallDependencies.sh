#!/bin/bash
# INSTALLATION OF PIBS CLIENT NODE

# Installation of the RadioHound dependencies for Icarus nodes
sudo apt-get install -y libusb-1.0-0-dev \
cmake \
python-dev \
python-scipy \
python-numpy \
python-ctypes \
python-matplotlib \
mosquitto \
mosquitto-clients

# Installation of the libraries for RadioHound

# 1) librtlsdr on the keenerd/rtl-sdr branch: https://github.com/keenerd/rtl-sdr

echo "=== Installing other python packages ================="
sudo pip install paho-mqtt 
sudo pip install netifaces
echo "->Finished installing python packages."

exit 0;
