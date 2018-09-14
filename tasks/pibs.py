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
    gps = node.sensors.getAnySensor('sensors.locationing')
    myCurrentPosition = gps.getLocation()
    receivedPosition = args[key_current_position]
    print args[key_source_id]
    # print args[key_uav_class]
    # print args[key_current_position]
    # print args[key_heading]
    print 'Detect and Avoid Logic Goes Here TBD'
    print "receivedPosition: ",receivedPosition,", myCurrentPosition: ",myCurrentPosition
    # dist = tools.getDistanceInMeters(args[key_current_position],[41.739565, -86.099060, 100])
    # dist = tools.getDistanceInMeters([41.739565, -86.099060, 100],[41.739001, -86.097830, 110])
    dist = tools.getDistanceInMeters([41.739565, -86.099065, 100],[41.739565, -86.099060, 500])
    # compare received location in message(args[key_current_position] with my current location
    # dist = tools.getDistanceInMeters(args[key_current_position],[])
    print str(dist) + " meters away factoring in alt ..."

