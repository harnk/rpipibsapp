import sensors, tasks
import tools
import json
import paho.mqtt.client as mqtt
import Queue
import time
import threading
import socket
import uuid
from definitions import *
import copy

current_milli_time = lambda: int(round(time.time() * 1000))
wifiFilename = '/home/pi/pibs-wifilog.txt'
lteFilename = '/home/pi/pibs-ltelog.txt'

class Node(object):
    def __init__(self, system=None, mac_address=None,
                 broker_name=None, messenger=None, initial_topics=None,
                 node_sensors=None, background=None, group_name=None):
        self.system = system
        self.all_sensors = tools.getAllClassesDict(sensors)
        self.all_tasks = tools.getAllFunctionsDict(tasks)

        self.user_tasks = tools.getUserFunctionsDict(tasks)

        self.running_tasks = []
        self._looping_flag = 0
        self._logging_flag = 0
        self.wifi_msg_count = 0
        self.lte_msg_count = 0

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.last_lte_heartbeat = time.time()
        self.last_wifi_heartbeat = self.last_lte_heartbeat
        self.last_updateconfig = self.last_lte_heartbeat
        self.last_gps_update = self.last_lte_heartbeat

        if mac_address != None:
            self.mac_address = mac_address.replace(':', '')
        else:
            self.mac_address = tools.getMacAddress()

        if broker_name != None:
            self.broker_name = broker_name
        elif key_broker_name in system:
            self.broker_name = system[key_broker_name]
        else:
            self.broker_name = None


        if background != None:
            self.background = background
        else:
            self.background = AsyncUDPReceiver(5002)
            self.background.start()

        if messenger != None:
            self.messenger = messenger
        elif initial_topics != None:
            self.messenger = self.initMessenger(self.broker_name, initial_topics)
        elif key_initial_topics in system:
            self.messenger = self.initMessenger(self.broker_name, system[key_initial_topics])
        else:
            self.messenger = None

        if node_sensors != None:
            self.sensors = node_sensors
        elif key_sensors in system:
            self.sensors = self.initSensors(system[key_sensors])
        else:
            self.sensors = None

        # heartbeat information that we only need once
        self.initStaticConfigParameters()
        # first update of dynamic configuration parameters
        self.updateConfig()

        if key_init_tasks in system:
            for payload_dict in system[key_init_tasks]:
                payload_str = json.dumps(payload_dict)
                if self.messenger != None:
                    thisTopic = system[key_initial_topics][0]
                    self.messenger.publish(thisTopic, payload_str)
                else:
                    msg = 'Cannot execute initialization task because there is no messenger:'
                    s = tools.bcolors.WARNING + msg + tools.bcolors.ENDC
                    print s
                    print tools.bcolors.WARNING + payload_str + tools.bcolors.ENDC

        # check for Drone GPS sensor and if it is there, start task to update location
        if system != None:
            doInitTask = False
            for sensor in system[key_sensors]:
                if sensor[key_type] == "sensors.locationing.DroneGPS":
                    doInitTask = True
            if doInitTask:
                payload_dict = {key_task_name: "tasks.locationing.updateGps", "arguments": {}}
                payload_str = json.dumps(payload_dict)
                if self.messenger != None:
                    thisTopic = system['initial_topics'][0]
                    self.messenger.publish(thisTopic, payload_str)
                else:
                    msg = 'Cannot execute initialization task because there is no messenger:'
                    s = tools.bcolors.WARNING + msg + tools.bcolors.ENDC
                    print s
                    print tools.bcolors.WARNING + payload_str + tools.bcolors.ENDC

        # check for raspbery pi gps hat sensor and if it is there, start task to update location
        if system != None:
            doInitTask = False
            for sensor in system[key_sensors]:
                if sensor[key_type] == "sensors.locationing.RaspberryPiGPSHat":
                    doInitTask = True
            if doInitTask:
                payload_dict = {"task_name": "tasks.locationing.updateRaspberryPiGPSHat", "arguments": {}}
                payload_str = json.dumps(payload_dict)
                if self.messenger != None:
                    thisTopic = system['initial_topics'][0]
                    self.messenger.publish(thisTopic, payload_str)
                else:
                    msg = 'Cannot execute initialization task because there is no messenger:'
                    s = tools.bcolors.WARNING + msg + tools.bcolors.ENDC
                    print s
                    print tools.bcolors.WARNING + payload_str + tools.bcolors.ENDC

    def initMessenger(self, broker_name, initial_topics):
        # todo: add print statements detailing status of mqtt connection because it can hang for various reasons
        # and user won't know what the problem is
        messenger = Messenger()
        # before we connect, check for a network connection (and wait)
        while not tools.check_network_connection(broker_name):
            print("Checking network connectivity for " + broker_name + " ...")
            pass

        for topic in initial_topics:
            messenger.subscriptions.add(topic)
            # print 'MQTT: Subscribing to: %s' % topic
            # messenger.subscribe(topic)
        messenger.connect(broker_name)
        messenger.loop_start()

        time.sleep(1)
        # SCXTT - comment out this next line for now TBD
        # messenger.reconnect_delay_set(min_delay=1, max_delay=120)

        return messenger

    def initSensors(self, sensors):
        # builds the node's collection of sensors
        snsrs = NodeSensors()
        for i in range(len(sensors)):
            sensor_type = sensors[i].pop(key_type)
            sensor_args = sensors[i]
            if sensor_type in self.all_sensors:
                snsrs.add(self.all_sensors[sensor_type](**sensor_args))
            else:
                # todo: raise exception
                print 'Sensor type: %s not present in sensor definitions (sensor definitions are located in .sensors/...)' % sensor_type
            sensors[i]['type'] = sensor_type
        return snsrs

    # ####################################################################
    # Main Loop
    # Executes every 10 ms
    # ####################################################################
    def loop_start(self):
        self._looping_flag = 1
        while self._looping_flag == 1:

            # Check for MQTT or UDP received messages
            if self.messenger is not None and \
                    not self.messenger.msg_queue.empty():
                msg = self.messenger.msg_queue.get()
                print ('MQTT msg queue: '+msg)
                if self._logging_flag == 1:
                    with open(lteFilename, "a") as myfile:
                        myfile.write(msg + ',')
                self.processMessage(msg)

            # Send heartbeat
            if self.messenger is not None:
                self.heartbeat()
            self.manageTasks()

            # Check for UDP received messages
            if self.background is not None and \
                    not self.background.msg_queue.empty():
                msg = self.background.msg_queue.get()
                print "UDP msg queue: ",msg
                if self._logging_flag == 1:
                    with open(wifiFilename, "a") as myfile:
                        myfile.write(msg + ',')
                self.processMessage(msg)

            time.sleep(.01)

    def loop_stop(self):
        self._looping_flag = 0

    def logging_start(self):
        self._logging_flag = 1

    def logging_stop(self):
        self._logging_flag = 0

    def addRunningTask(self, task_name, arguments):
        # Verify that the requested task exists
        if task_name in self.all_tasks:
            self.running_tasks.append(
                {key_thread: threading.Thread(target=self.all_tasks[task_name],
                                              args=(self, arguments)),
                 key_task_name: task_name,
                 key_arguments: arguments
                 })

            self.running_tasks[-1][key_thread].start()
            now = time.time()
            self.running_tasks[-1][key_start_time] = now
        else:
            print 'Unrecognized task received: %s ... do nothing' % task_name

    def processMessage(self, json_msg):
        try:
            j = json.loads(json_msg)
        except Exception as err:
            # failed trying to load JSON
            print("core.processMessage: Unable to load JSON message: %s" % err)
        else:  # if no exception, do the following:
            if type(j) == dict:

                if 'task_name' in j:
                    task_name = j[key_task_name]
                    arguments = j[key_arguments]
                    self.addRunningTask(task_name, arguments)
                    if 'timeout' in j:
                        now = time.time()
                        self.running_tasks[-1]['end_time'] = now + j['timeout']

                elif 'pibs_payload' in j:
                    task_name = 'tasks.pibs.detectAndAvoid'
                    if key_pibs_payload in j:
                        arguments = j[key_pibs_payload]
                    else:
                        arguments = {}  # arguments may be empty
                    self.addRunningTask(task_name, arguments)
                    if 'timeout' in j:
                        now = time.time()
                        self.running_tasks[-1]['end_time'] = now + j['timeout']

                else:
                    print "Unrecognized message received: %s ... do nothing" % json_msg
                    pass

            else:
                print "Not valid JSON %s" % str(j)
                pass

    def heartbeat(self):
        # Information updated every LTE_HEARTBEAT_RATE seconds: gps location
        # Information updated every UPDATECONFIG_RATE seconds: IP address, disk used, disk free
        # Information set only once at beginning: everything else*
        # *Note: broker name, short name, group name can be changed at will with another task
        now = time.time()
        if (now - self.last_wifi_heartbeat) > WIFI_HEARTBEAT_RATE:
            self.last_wifi_heartbeat = now
            self.wifi_msg_count += 1
            # print 'wifi heartbeat at %s' % str(now)
            payload = json.dumps(self.heartbeatMessage(self.wifi_msg_count))
            self.sock.sendto(payload,('10.2.1.255', 5002))

        if (now - self.last_gps_update) > GPS_UPDATE_RATE:
            self.last_gps_update = now
            task_name = 'tasks.locationing.updateRaspberryPiGPSHat'
            arguments = {}  # arguments may be empty
            self.addRunningTask(task_name, arguments)

        if (now - self.last_lte_heartbeat) > LTE_HEARTBEAT_RATE:
            self.last_lte_heartbeat = now
            self.lte_msg_count += 1
            # print 'lte heartbeat at %s' % str(now)
            payload = self.heartbeatMessage(self.lte_msg_count)
            # self.messenger.publish(PIBS_MQTT_STATUS_TOPIC_BASE + self.mac_address, \
            #                        payload=json.dumps(payload))
            self.messenger.publish(PIBS_MQTT_STATUS_TOPIC_BASE , \
                               payload=json.dumps(payload))
        if (now - self.last_updateconfig) > UPDATECONFIG_RATE:
            self.last_updateconfig = now
            # print 'updated config at %s' % str(now)
            self.updateConfig()

    def heartbeatMessage(self, msgCnt):
        # get location
        gps = self.sensors.getAnySensor('sensors.locationing')
        latitude, longitude, altitude = gps.getLocation()
        # TODO: automate GPS

        generationTime = str(time.time())
        signalStrength = tools.get_wifi_signal_level()
        payload = {key_pibs_payload:{
            key_source_id: self.mac_address,
            # key_uav_class: "tbd",
            key_current_position:[latitude,longitude,altitude],
            key_generation_time: generationTime,
            # key_heading:[[41.7,-87.1,500],[41.8,-87.3,500]],
            # key_resolution_advisory_flag:False,
            # key_emergency_flag:False,
            key_wifi_sig: signalStrength,
            key_msg_num: msgCnt
        }}

        return payload

    def initStaticConfigParameters(self):
        try:
            self.hostname = tools.get_host_name()
        except:
            self.hostname = ''
        try:
            self.osVersion = tools.read_os_version()
        except:
            self.osVersion = ''
        try:
            self.hardwareVersion = tools.read_hardware_version()
        except:
            self.hardwareVersion = ''

    def updateConfig(self):
        # _, self.diskUsed, self.diskFree = tools.disk_usage('/')
        self.ipAddress = tools.getIPAddress()

    def manageTasks(self):
        for running_task in self.running_tasks:
            if not running_task[key_thread].isAlive():
                i = self.running_tasks.index(running_task)
                self.running_tasks.pop(i)
                # print self.running_tasks


class Messenger(mqtt.Client):
    def __init__(self):
        super(Messenger, self).__init__()
        self.msg_queue = Queue.Queue()
        self.subscriptions = set()

    def on_connect(self, client, userdata, flags, rc):
        print('MQTT: Connected with result code ' + str(rc))
        self.loop_start()
        # hacky, fix later
        for s in self.subscriptions:
            self.subscribe(s)
        time.sleep(1)

    def on_message(self, client, userdata, msg):
        print 'MQTT: Message received @time: ', current_milli_time(), 'ms'
        # print str(msg.payload)[0:200] + ' ...'
        self.msg_queue.put(msg.payload)

    #    def on_disconnect(self, client, userdata, rc):
    #        print 'disconnected from MQTT broker, trying to reconnect'
    #        self.reconnect()
    #        print 'finished trying to reconnect not sure if worked'

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print('MQTT: Subscribed...')

    def on_unsubscribe(self, client, userdata, mid):
        print('MQTT: Unsubscribed...')


class NodeSensors(object):
    def __init__(self, sensor_list=None):
        self._list = []
        if sensor_list != None:
            for sensor in sensor_list:
                self.add(sensor)

    def add(self, sensor):
        self._list.append(sensor)

    def getAnySensor(self, domain):
        sensors_in_domain = filter(lambda x: x.__module__ == domain, self._list)
        return sensors_in_domain[0]

    def getSensorByType(self, sensor_type):
        # TODO: what to do if there are multiple sensors with the same type
        sensors_with_matching_type = filter(lambda x: tools.getObjPath(x.__class__) == sensor_type, self._list)
        return sensors_with_matching_type[0]

    def getSensorByHWID(self, HWID):
        # get sensor by hardware ID
        # TODO: what to do if there are multiple sensors with the same HWID
        sensors_with_matching_hw_id = filter(lambda x: x.hardware_id == str(HWID), self._list)
        return sensors_with_matching_hw_id[0]

    @property
    def domains(self):
        return map(lambda x: x.__module__, self._list)

    def __iter__(self):
        return iter(self._list)

    def __getitem__(self, i):
        return self._list[i]


class AsyncUDPReceiver(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.msg_queue = Queue.Queue()
        self.port = port

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        address = ('', self.port)
        sock.bind(address)
        print "Starting background UDP thread"
        while True:
            data, addr = sock.recvfrom(1024)
            print 'UDP: Message received @time: ', current_milli_time(), 'ms'
            self.msg_queue.put(data)
            # print data
            print addr


