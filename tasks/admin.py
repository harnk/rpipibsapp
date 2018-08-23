import json
import time
import sys
import tools
import os
import subprocess
import platform
from definitions import *
from tools import *

current_milli_time = lambda: int(round(time.time() * 1000))
TAG = 'tasks.admin.'


def stop_loop(node, args):
    node.loop_stop()


def request_task_list(node, args):
    print 'TASK: ' + TAG + sys._getframe().f_code.co_name + ' @time:', current_milli_time(), 'ms'

    """
    args =  {
                "topic":<mqtt reply topic>"
            }
    """
    try:
        payload = {'task_list':
                       map(lambda x: x, node.user_tasks)}
        node.messenger.publish(str(args[key_topic]), payload=json.dumps(payload))
    except Exception as err:
        # failed reading args, announce the error
        tools.announceError(node, TAG + sys._getframe().f_code.co_name, err)


def request_running_tasks(node, args):
    print 'TASK: ' + TAG + sys._getframe().f_code.co_name + ' @time:', current_milli_time(), 'ms'
    """
    args =  {
                "topic":<mqtt reply topic>"
            }
    """
    try:
        payload = {'running_tasks':
                       map(lambda x: x[key_task_name], node.running_tasks)}
        node.messenger.publish(str(args[key_topic]), payload=json.dumps(payload))
    except Exception as err:
        # failed reading args, announce the error
        tools.announceError(node, TAG + sys._getframe().f_code.co_name, err)


def request_status(node, args):
    print 'TASK: ' + TAG + sys._getframe().f_code.co_name + ' @time:', current_milli_time(), 'ms'
    """
    args =  {
                "topic":<mqtt reply topic>"
            }
    """
    try:
        payload = node.heartbeatMessage()
        payload[key_message] = 'STATUS'
        node.messenger.publish(str(args[key_topic]), payload=json.dumps(payload))
    except Exception as err:
        # failed reading args, announce the error
        tools.announceError(node, TAG + sys._getframe().f_code.co_name, err)


def reboot(node, args=None, topic=PIBS_MQTT_DEFAULT_DEBUG_TOPIC):
    '''
    reboot(node,args=None)
    Reboots the host.
    args = {'topic': mqtt topic for debug information}
    '''
    if args is not None:
        if 'topic' in args:
            topic = args['topic']

    # send feedback
    node.messenger.publish(topic,
                           payload='Rebooting node ' + node.mac_address + ' ... (Will give future message if failure.)')

    # check platform
    myOS = platform.system()
    # reboot based on platform
    if myOS == "Linux" or myOS == "Darwin":
        os.system("reboot")
    elif myOS == "Windows":
        os.system("shutdown -r -t 1")
    else:
        # send message back to GUI
        node.messenger.publish(topic, payload='Failed to reboot node ' + node.mac_address)


def gitPull(node, args=None, remote='mc', branch='master'):
    '''
    gitPull(node,args=None,remote='mc',branch='master')

    Performs the command "sudo -u pi git pull <remote> <branch>"

    args={
    'remote': 'mc' <str>
    'branch': 'dev' <str>
    }
    '''
    # update arguments based on args (if necessary)
    if args is not None:
        if 'remote' in args:
            remote = args['remote']
        if 'branch' in args:
            branch = args['branch']
    # stash local changes before pulling
    subprocess.call('sudo -u pi git stash', shell=True)
    # call "git pull <remote> <branch>"
    subprocess.call('sudo -u pi git pull ' + remote + ' ' + branch, shell=True)


def setTime(node, args=None, time=None, topic=PIBS_MQTT_DEFAULT_DEBUG_TOPIC):
    '''
    setTime(node,args=None,time=None)

    args = {"time": "Fri Mar 16 10:50:38 EDT 2018",
            "topic": mqtt_topic (debug)}
    '''
    if args is not None:
        if "time" in args:
            time = args["time"]
        if "topic" in args:
            topic = args["topic"]

    if time != None:
        myOS = platform.system()
        if myOS == "Linux" or myOS == "Darwin":
            print(time)
            os.system('sudo date -s "' + time + '"')
            node.messenger.publish(topic, payload="Reset time on " + node.mac_address)
        else:
            print("Failed to reset time.  Not a Linux box.")
            node.messenger.publish(topic, payload="Failed to reset time on " + \
                                                  node.mac_address + ". Not a Linux box.")

