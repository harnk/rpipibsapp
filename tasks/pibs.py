import json
import time
import sys
import tools
import os
import subprocess
import platform
from definitions import *

current_milli_time = lambda: int(round(time.time() * 1000))
TAG = 'tasks.pibs.'

def detectAndAvoid(node,args):
    print 'TASK: ' + TAG + sys._getframe().f_code.co_name + ' @time:', current_milli_time(), 'ms'
    print args[key_source_id]
    print args[key_uav_class]
    print args[key_current_position]
    print args[key_heading]
    print 'Detect and Avoid Logic Goes Here TBD'
    # dist = tools.getDistanceInMeters(args[key_current_position],[41.739565, -86.099060, 100])
    # dist = tools.getDistanceInMeters([41.739565, -86.099060, 100],[41.739001, -86.097830, 110])
    dist = tools.getDistanceInMeters([41.739565, -86.099060, 100],[41.739565, -86.099060, 500])
    print str(dist) + " meters away factoring in alt ..."

