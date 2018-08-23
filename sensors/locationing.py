import numpy as np
import threading
import requests
from requests.packages.urllib3 import exceptions
import os, sys
import tools
import gps


###############################################################################
### Devices in gps domain
###############################################################################

class GPS(object):
    def __init__(self, hardware_id):
        self.hardware_id = hardware_id
        self.lock = threading.Lock()

    def setParameters(self):
        pass

    def getParameters(self, query):
        pass

    def getLocation(self):
        pass


class DroneGPS(GPS):
    def __init__(self, hardware_id, ip_address, latitude=0, longitude=0, altitude=0):
        GPS.__init__(self, hardware_id)
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

        # INITIALIZATION TO READ FROM DRONE GPS
        # T B D
        # start infinite task of updating location in init_tasks
        # I don't think this can be done because it requires passing a messenger... which can't be done.

    def setParameters(self, latitude=None, longitude=None, altitude=None):
        self.lock.acquire()
        if latitude is not None:
            self.latitude = latitude
        if longitude is not None:
            self.longitude = longitude
        if altitude is not None:
            self.altitude = altitude
        self.lock.release()

    def getParameters(self, query):
        if type(query) != list or type(query) != tuple:
            if query == 'latitude':
                return self.latitude
            elif query == 'longitude':
                return self.longitude
            elif query == 'altitude':
                return self.altitude
            else:
                # raise exception
                return []
        else:
            out = []
            for parameter_name in query:
                if parameter_name == 'latitude':
                    return self.latitude
                elif parameter_name == 'longitude':
                    return self.longitude
                elif parameter_name == 'altitude':
                    return self.altitude
                else:
                    # raise exception
                    pass
            return out

    def getLocation(self):
        self.lock.acquire()
        myLocation = np.array((self.latitude, self.longitude, self.altitude))
        self.lock.release()
        return myLocation


class DummyGPS(GPS):
    def __init__(self, hardware_id, latitude=0, longitude=0, altitude=0):
        GPS.__init__(self, hardware_id)
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    def setParameters(self, latitude=None, longitude=None, altitude=None):
        self.lock.acquire()
        if latitude is not None:
            self.latitude = latitude
        if longitude is not None:
            self.longitude = longitude
        if altitude is not None:
            self.altitude = altitude
        self.lock.release()

    def getLocation(self):
        self.lock.acquire()
        myLocation = np.array((self.latitude, self.longitude, self.altitude))
        self.lock.release()
        return myLocation

    def getParameters(self, query):
        if type(query) != list or type(query) != tuple:
            if query == 'latitude':
                return self.latitude
            elif query == 'longitude':
                return self.longitude
            elif query == 'altitude':
                return self.altitude
            else:
                # raise exception
                return []
        else:
            out = []
            for parameter_name in query:
                if parameter_name == 'latitude':
                    return self.latitude
                elif parameter_name == 'longitude':
                    return self.longitude
                elif parameter_name == 'altitude':
                    return self.altitude
                else:
                    # raise exception
                    pass
            return out


class RaspberryPiGPSHat(GPS):
    def __init__(self, hardware_id, latitude=0, longitude=0, altitude=0):
        GPS.__init__(self, hardware_id)
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.gpsd = gps.gps(mode=gps.WATCH_ENABLE)  # start the stream of info
        # INITIALIZATION TO READ FROM GPS HAT
        # disable warnings
        # requests.packages.urllib3.disable_warnings(exceptions.InsecureRequestWarning)
        # setup alias IP so that we can talk to the Persistent Systems management screen
        # os.system("sudo ifconfig eth0:1 172.26.1.1 netmask 255.255.255.0 up")
        # url to the Persistent Systems management screen associated with the GPS
        # self.url = "https://" + ip_address + "/management.cgi?command=gps_status.json&password-input=password"

        # start infinite task of updating location in init_tasks
        # I don't think this can be done because it requires passing a messenger... which can't be done.

    def setParameters(self, latitude=None, longitude=None, altitude=None):
        self.lock.acquire()
        if latitude is not None:
            self.latitude = latitude
        if longitude is not None:
            self.longitude = longitude
        if altitude is not None:
            self.altitude = altitude
        self.lock.release()

    def getLocation(self):
        self.lock.acquire()
        myLocation = np.array((self.latitude, self.longitude, self.altitude))
        self.lock.release()
        return myLocation

    def getParameters(self, query):
        if type(query) != list or type(query) != tuple:
            if query == 'latitude':
                return self.latitude
            elif query == 'longitude':
                return self.longitude
            elif query == 'altitude':
                return self.altitude
            else:
                # raise exception
                return []
        else:
            out = []
            for parameter_name in query:
                if parameter_name == 'latitude':
                    return self.latitude
                elif parameter_name == 'longitude':
                    return self.longitude
                elif parameter_name == 'altitude':
                    return self.altitude
                else:
                    # raise exception
                    pass
            return out

###############################################################################
### Tasks in gps domain
###############################################################################

def getLocation(gps):
    # data = gps.getLocation()
    # return data
    return np.array((4, 5, 6))

