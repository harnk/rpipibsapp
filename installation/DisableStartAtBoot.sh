#!/bin/bash

# Variables
LOGPATH=/home/pi

# edit /etc/rc.local file for disabling pibs_client at boot
sudo sed -i -e 's+/home/pi/pibs_client/RunPibsClient.sh &++g' /etc/rc.local


exit 0;
