import requests
import json
import time
from threading import Event
from definitions import *
import tools

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
    except:
        print("Error connecting to HAT GPS, try again later!")
    else:
        # if we move more than GPS_TOLERANCE, save location to file
        if lat != None and lon != None:
            print "GPS Reading: ", lat, ", ", lon, ", ",alt
            oldLat, oldLon, oldAlt = gps.getLocation()
            oldPosition = [oldLat, oldLon, oldAlt]
            newPosition = [lat, lon, alt]
            changeInDistance = tools.getDistanceInMeters(oldPosition, newPosition)
            # update parameters in Manet class
            gps.setParameters(latitude=lat, longitude=lon, altitude=alt)
            if changeInDistance > GPS_TOLERANCE:
                # save to file
                print "tools.saveConfigurationToFile(node) TBD",

                # delay a bit, but clear the buffer while we wait...
    then = time.time()
    while time.time() - then < GPS_UPDATE_RATE:  # wait 5 seconds
        gps.gpsd.next()  # this will continue to grab EACH set of gpsd info to clear the buffer

    # loop task by calling this task again
    payload_dict = {"task_name": "tasks.locationing.updateRaspberryPiGPSHat", "arguments": {}}
    payload_str = json.dumps(payload_dict)
    if node.local_messenger != None:
        thisTopic = node.system['initial_topics'][0]
        node.local_messenger.publish(thisTopic, payload_str)


def getGPS(node, args):
    '''
    args = {
        'topic': mqtt topic to return data on
    }
    '''
    if 'topic' not in args:
        node.messenger.publish(PIBS_MQTT_DEFAULT_DEBUG_TOPIC,
                               payload='ERROR: tasks.locationing.getGPS requires the argument topic.')
    else:
        topic = args['topic']
        # get gps for checking location
        gps = node.sensors.getAnySensor('sensors.locationing')
        # get location
        lat, lon, alt = gps.getLocation()
        # send message back
        payload_dict = {key_latitude: lat, key_longitude: lon, key_altitude: alt}
        node.messenger.publish(topic, payload=json.dumps(payload_dict))