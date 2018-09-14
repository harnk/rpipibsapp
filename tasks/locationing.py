import requests
import json
import time
import sys
from threading import Event
from definitions import *
import tools

current_milli_time = lambda: int(round(time.time() * 1000))
TAG = 'tasks.locationing.'


def updateRaspberryPiGPSHat(node, args=None):
    # get gps for checking location
    gps = node.sensors.getAnySensor('sensors.locationing')
    # initialize results
    lat = None
    lon = None
    alt = None
    # check GPS
    print("Checking HAT GPS ...")
    try:
        lat = gps.gpsd.fix.latitude
        lon = gps.gpsd.fix.longitude
        alt = gps.gpsd.fix.altitude
        gpstime = gps.gpsd.fix.time
    except:
        print("Error connecting to HAT GPS, try again later!")
        return
    else:
        # if we move more than GPS_TOLERANCE, save location to file
        if lat != None and lon != None:
            print "GPS Reading: ", lat, ", ", lon, ", ",alt, ", time: ",gpstime
            oldLat, oldLon, oldAlt = gps.getLocation()
            oldPosition = [oldLat, oldLon, oldAlt]
            newPosition = [lat, lon, alt]
            changeInDistance = tools.getDistanceInMeters(oldPosition, newPosition)
            # update parameters in Manet class
            gps.setParameters(latitude=lat, longitude=lon, altitude=alt)
            if changeInDistance > GPS_TOLERANCE:
                # save to file the new lat lon alt
                print "tools.saveConfigurationToFile(node) TBD",

                # delay a bit, but clear the buffer while we wait...
    then = time.time()
    while time.time() - then < 1 :  # wait 1 seconds
        gps.gpsd.next()  # this will continue to grab EACH set of gpsd info to clear the buffer

    # loop task by calling this task again SCXTT TBD - CHANGE THIS we dont want LTE round trip for every GPS reading
    # May want to consider setting up a local MQTT broker like RH does
    # payload_dict = {"task_name": "tasks.locationing.updateRaspberryPiGPSHat", "arguments": {}}
    # payload_str = json.dumps(payload_dict)
    # if node.messenger != None:
    #     thisTopic = node.system['initial_topics'][0]
    #     node.messenger.publish(thisTopic, payload_str)

def getRaspberryPiGPSHat(node,args):
    # get gps for checking location
    gps = node.sensors.getAnySensor('sensors.locationing')
    # initialize results
    lat = None
    lon = None
    alt = None
    # check GPS
    print("Checking HAT GPS ...")
    try:
        lat = gps.gpsd.fix.latitude
        lon = gps.gpsd.fix.longitude
        alt = gps.gpsd.fix.altitude
    except:
        print("Error connecting to HAT GPS, try again later!")

    topic = args[key_topic]
    payload_dict = {key_latitude: lat, key_longitude: lon, key_altitude: alt}
    node.messenger.publish(topic,payload=json.dumps(payload_dict))


def getGPS(node, args):
    print 'TASK: ' + TAG + sys._getframe().f_code.co_name + ' @time:', current_milli_time(), 'ms'
    """
    args =  {
                "topic":<mqtt reply topic>"
            }
    """
    if key_topic not in args:
        node.messenger.publish(PIBS_MQTT_DEFAULT_DEBUG_TOPIC,
                               payload='ERROR: tasks.locationing.getGPS requires the argument topic.')
    else:
        topic = args[key_topic]
        # get gps for checking location
        gps = node.sensors.getAnySensor('sensors.locationing')
        # get location
        lat, lon, alt = gps.getLocation()
        # send message back
        payload_dict = {key_latitude: lat, key_longitude: lon, key_altitude: alt}
        node.messenger.publish(topic, payload=json.dumps(payload_dict))
