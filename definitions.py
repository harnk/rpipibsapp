'''
definitions.py

This file contains definitions used by all the python scripts.

- Scott Null, 08/23/2018
'''

SOFTWARE_VERSION = '0.0.0.0'
LOCAL_CONFIG_FILE = 'system.json'

PIBS_BROADCAST_IP = '10.2.1.255'
PIBS_BROADCAST_PORT = 5002
PIBS_WIFI_CHANNEL = 1
PIBS_WIFI_ESSID = 'PiAdHocNetwork'

PIBS_MQTT_BROADCAST_TOPIC = "pibs/clients/broadcast"
PIBS_MQTT_STATUS_TOPIC_BASE = 'pibs/clients/status/'
PIBS_MQTT_DATA_TOPIC_BASE = 'pibs/clients/data/'
PIBS_MQTT_CMD_TOPIC_BASE = 'pibs/clients/command/'
PIBS_MQTT_DEFAULT_DEBUG_TOPIC = 'pibs/debug'

# Heartbeat periodicity
LTE_HEARTBEAT_RATE = 40 # seconds
WIFI_HEARTBEAT_RATE = 42 # seconds
UPDATECONFIG_RATE = 60 # seconds

# GPS parameters
GPS_TOLERANCE = 10 # meters
GPS_UPDATE_RATE = 5 # seconds

# PIBS and task Key Names
key_task_name = 'task_name'
key_arguments = 'arguments'
key_message = 'message'
key_data = 'data'
key_topic = 'topic'
key_thread = 'thread'
key_start_time = 'start_time'
key_pibs_payload = 'pibs_payload'
key_source_id = 'source_id'
key_uav_class = 'uav_class'
key_current_position = 'current_position'
key_generation_time = 'generation_time'
key_heading = 'heading'
key_resolution_advisory_flag = 'resolution_advisory_flag'
key_emergency_flag = 'emergency_flag'
key_msg_num = 'msg_num'
key_wifi_sig = 'wifi_sig'

# Local Config File Key Names
key_broker_name = 'broker_name'
key_initial_topics = 'initial_topics'
key_ip_address = 'ip_address'
key_sensors = 'sensors'
key_type = 'type'
key_hardware_id = 'hardware_id'
key_longitude = 'longitude'
key_latitude = 'latitude'
key_altitude = 'altitude'
key_init_tasks = 'init_tasks'