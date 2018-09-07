#!/bin/bash

# get the full patch to this script, no matter where
# it is executed from nor how it is executed.

STR="$0"

# if the script name starts with "./", remove those characters
if [[ "${STR:0:2}" == "./" ]]; then
    STR="${STR:2}"
fi

# if the script name does not start with "/", then create
# a new script name by joining the PWD with the script
if [[ "${STR:0:1}" != "/" ]]; then
    STR="${PWD}/${STR}"
fi

# get the directory in which the absolute path
# including filename for this script name is located
STR=$(dirname "${STR}")

# make sure the CWD is ., no matter where this script is executed from
cd "$STR"

# Variables
LOGPATH=/home/pi
SCRIPTPATH=$STR

# Update apt-get and upgrade current packages
date | tee -a $LOGPATH/PC_install_log.txt
echo "=== Updating apt-get and current packages =================" | tee -a $LOGPATH/PC_install_log.txt
sudo apt-get update -y | tee -a $LOGPATH/PC_install_log.txt

# Install Dependencies
echo "=== Installing dependencies  =================" | tee -a $LOGPATH/PC_install_log.txt
sudo $SCRIPTPATH/InstallDependencies.sh
echo "->Finished installing dependencies..." | tee -a $LOGPATH/PC_install_log.txt

# Enable GPS
#echo "=== Enable Reading Serial Port / GPS ==================" | tee -a $LOGPATH/#PC_install_log.txt
#sudo $SCRIPTPATH/EnableGPS.sh
#echo "-> Finished." | tee -a $LOGPATH/PC_install_log.txt

# Enable SSH
echo "=== Enable SSH for debugging ====="
sudo $SCRIPTPATH/EnableSSH.sh
# part of enabling ssh is changing the pi password:
# download "expect" scripting language
echo "-> Installing expect package..." | tee -a $LOGPATH/PC_install_log.txt
sudo apt-get install expect -y | tee -a $LOGPATH/PC_install_log.txt
sudo -u pi $SCRIPTPATH/ChangePassword.sh | tee -a $LOGPATH/PC_install_log.txt
echo "-> Changed password." | tee -a $LOGPATH/PC_install_log.txt
echo "-> Finished." | tee -a $LOGPATH/PC_install_log.txt

# Enable Remote Git Updating
echo "=== Enabling Remote Git Updating ==="
# Add SSH keys for Remote Git updating
sudo -u pi $SCRIPTPATH/AddSSHKeys.sh
# make changes in local repo
sudo $SCRIPTPATH/EnableGitRemote.sh

# Change Hostname to last four characters of mac address
echo "=== Changing Hostname ==========" | tee -a $LOGPATH/PC_install_log.txt
sudo $SCRIPTPATH/ChangeHostname.sh

# Enable Ad-Hoc Wifi and LTE
echo "=== Editing interfaces file to enable ad-hoc wifi and LTE =================" | tee -a $LOGPATH/PC_install_log.txt
sudo $SCRIPTPATH/EnableAdHocWifi.sh
echo "Finished editing interfaces." | tee -a $LOGPATH/PC_install_log.txt

# Start PIBS Client at boot
echo "=== Editing rc.local file to enable pibs client at boot =================" | tee -a $LOGPATH/PC_install_log.txt
sudo $SCRIPTPATH/EnableStartAtBoot.sh
echo "Finished editing rc.local." | tee -a $LOGPATH/PC_install_log.txt

# Create system.json file automatically
echo "===== Creating system.json ==========" | tee -a $LOGPATH/PC_install_log.txt
python $SCRIPTPATH/create_system_json.py
echo "-> Finished." | tee -a $LOGPATH/PC_install_log.txt

# Change owner of files
echo "===== Changing ownerships to user pi ======" | tee -a $LOGPATH/PC_install_log.txt
cd /home/pi/pibs_client && sudo chown -R pi:pi . | tee -a $LOGPATH/PC_install_log.txt
echo "-> Finished." | tee -a $LOGPATH/PC_install_log.txt

echo "Finished configuration." | tee -a $LOGPATH/PC_install_log.txt
date | tee -a $LOGPATH/PC_install_log.txt
echo "See $LOGPATH/PC_install_log.txt for a log of the installation."
echo "Please reboot now after editing /etc/network/interfaces to set the static ip."

exit 0;