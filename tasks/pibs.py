import json
import time
import sys
import tools
import os
import subprocess
import platform
import gps
from definitions import *

current_milli_time = lambda: int(round(time.time() * 1000))
TAG = 'tasks.pibs.'

def detectAndAvoid(node,args):
    print 'TASK: ' + TAG + sys._getframe().f_code.co_name + ' @time:', current_milli_time(), 'ms'
    if (args[key_source_id] == node.mac_address):
        # received my own message so ignore it
        return

    gps = node.sensors.getAnySensor('sensors.locationing')
    lat, lon, alt = gps.getLocation()
    myCurrentPosition = [lat,lon,alt]
    receivedPosition = args[key_current_position]
    # print args[key_source_id]
    # print args[key_uav_class]
    # print args[key_current_position]
    # print args[key_heading]
    # print "receivedPosition: ",receivedPosition,", myCurrentPosition: ",myCurrentPosition
    # dist = tools.getDistanceInMeters([41.739565, -86.099065, 100],[41.739565, -86.099060, 500])

    # compare my current position with received position
    dist = tools.getDistanceInMeters(myCurrentPosition,receivedPosition)
    print "Detect and Avoid Logic Goes Here TBD - message from: ",args[key_source_id], " which is ", str(dist), " meters away ..."

