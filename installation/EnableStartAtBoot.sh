#!/bin/bash

# Variables
LOGPATH=/home/pi

# edit /etc/rc.local file for starting pibs_client at boot

sudo sed -i -e 's+/home/pi/icarus/run_icarus.sh &++g' /etc/rc.local
sudo sed -i -e 's+/home/pi/pibs_client/RunPibsClient.sh &++g' /etc/rc.local
sudo sed -i -e 's/exit 0//g' /etc/rc.local
sudo echo "/home/pi/pibs_client/RunPibsClient.sh &" >> /etc/rc.local
sudo echo "exit 0" >> /etc/rc.local

exit 0;
