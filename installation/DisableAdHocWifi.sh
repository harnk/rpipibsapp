#!/bin/bash

# Variables
FILENAME=/etc/network/interfaces

# edit /etc/network/interfaces file to setup ad-hoc wifi and lte

sudo echo "source-directory /etc/network/interfaces.d" > /etc/network/interfaces

exit 0;