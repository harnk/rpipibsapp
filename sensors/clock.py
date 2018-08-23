import numpy
import time
import datetime


###############################################################################
### Devices in clock domain
###############################################################################

class Clock(object):
    def __init__(self, hardware_id):
        self.hardware_id = hardware_id
        pass

    def setParameters(self):
        pass

    def getParameters(self, query):
        pass

    def getTime(self):
        pass

    def getTimestamp(self):
        pass


class RaspberryClock(Clock):
    def __init__(self, hardware_id):
        self.hardware_id = hardware_id
        pass

    def setParameters(self):
        pass

    def getParameters(self, query):
        pass

    def getTime(self):
        return time.time()

    def getTimestamp(self):
        return datetime.datetime.now()


###############################################################################
### Tasks in clock domain
###############################################################################

def getTime(clock):
    # data = receiver.capture()
    # return data
    return clock.getTime()

