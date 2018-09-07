#!/bin/bash
# AddSSHKeys.sh
# Set up SSH authorized keys for administrative remote access

# find the directory in which this script is located
SCRIPTPATH=$(dirname $0)

echo "->Adding ssh authorized keys for Pibs servers...."

if [ -d "/home/pi/.ssh/" ]; then
	echo "-> .ssh directory already exists."
else
	echo "-> Creating .ssh directory."
	mkdir /home/pi/.ssh
fi

# copy pi@pi keys
cp $SCRIPTPATH/ssh/id_rsa /home/pi/.ssh/id_rsa
chmod 0600 /home/pi/.ssh/id_rsa

# Enabling pi@pi keys
eval "$(ssh-agent -s)"
ssh-add /home/pi/.ssh/id_rsa

echo "->Added ssh keys for Pibs servers."
echo "->Finished."

exit 0;