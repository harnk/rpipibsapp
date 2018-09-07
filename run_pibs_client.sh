#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# Copyright 2018 University of Notre Dame.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

# run as sudo on Linux
if [[ $(uname) == "Linux" ]]; then
    if [[ ${USER} == "pi" ]]; then
	sudo $0 $*
    fi
fi

###
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

###
# catch various signals to terminate cleanly

on_die()
{
    echo ""
    echo "Terminating pibs client...."

    # Need to exit the script explicitly when done.
    # Otherwise the script would live on, until system
    # really goes down, and KILL signals are sent.

    exit 0
}

function ctrl_c()
{
    echo "CTRL-C detected..."
    exit 0
}

trap 'on_die' SIGINT SIGTERM SIGKILL

trap 'ctrl_c' INT
###
# Start client running

echo "Initializing icarus client...."

python start.py $*
